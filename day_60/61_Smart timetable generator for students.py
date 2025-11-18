"""                                                           Day = 61

                                                  Smart Timetable Generator for Students 
Features:
- Tkinter GUI to add subjects with:
    * name, sessions_per_week, session_length_minutes, priority (1-5),
    * preferred_days (Mon..Sun), preferred_time_range (start_hour-end_hour),
    * avoid_back_to_back (bool)
- Define global constraints:
    * days (Mon-Fri or Mon-Sun), day start/end hours, max hours per day
- Generates a weekly timetable (grid of slots) using a greedy + local-improvement algorithm:
    * breaks each day into fixed slots (30-minute resolution)
    * schedules required sessions per subject, respects preferences and constraints
    * tries to spread sessions across the week and avoid consecutive sessions when requested
- Simple optimizer (swap-based) to improve distribution and reduce conflicts
- Export timetable to CSV, Save/Load project (JSON)
- No external packages required

Run:
    python smart_timetable.py
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import csv
from datetime import datetime
import os
import math
import random

# ----------------------------
# Helper data structures
# ----------------------------
DAYS_FULL = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DEFAULT_DAYS = DAYS_FULL[:5]  # Mon-Fri

SLOT_MINUTES = 30  # resolution

# ----------------------------
# Timetable Engine
# ----------------------------
class Subject:
    def __init__(self, name, sessions_per_week, session_length_min, priority=3,
                 preferred_days=None, time_range=(8, 18), avoid_back_to_back=False):
        self.name = name.strip()
        self.sessions_per_week = int(sessions_per_week)
        self.session_length_min = int(session_length_min)
        self.priority = int(priority)
        self.preferred_days = preferred_days if preferred_days is not None else DEFAULT_DAYS.copy()
        self.time_range = time_range  # (start_hour, end_hour)
        self.avoid_back_to_back = bool(avoid_back_to_back)

    def to_dict(self):
        return {
            "name": self.name,
            "sessions_per_week": self.sessions_per_week,
            "session_length_min": self.session_length_min,
            "priority": self.priority,
            "preferred_days": self.preferred_days,
            "time_range": self.time_range,
            "avoid_back_to_back": self.avoid_back_to_back
        }

    @staticmethod
    def from_dict(d):
        return Subject(
            d["name"],
            d["sessions_per_week"],
            d["session_length_min"],
            d.get("priority", 3),
            d.get("preferred_days"),
            tuple(d.get("time_range", (8, 18))),
            d.get("avoid_back_to_back", False)
        )

class TimetableEngine:
    def __init__(self, days=DEFAULT_DAYS, day_start=8, day_end=18, max_hours_per_day=8):
        self.days = days[:]  # list of day names
        self.day_start = day_start
        self.day_end = day_end
        self.max_hours_per_day = float(max_hours_per_day)
        self.slot_minutes = SLOT_MINUTES
        self.slots_per_hour = 60 // self.slot_minutes
        self.subjects = []  # list of Subject
        self._build_grid()

    def _build_grid(self):
        self.num_slots_per_day = (self.day_end - self.day_start) * self.slots_per_hour
        # representation: timetable[day_index][slot_index] = None or (subject_name, length_slots)
        self.timetable = [[None for _ in range(self.num_slots_per_day)] for _ in self.days]

    def add_subject(self, subj: Subject):
        self.subjects.append(subj)

    def remove_subject(self, name):
        self.subjects = [s for s in self.subjects if s.name != name]

    def clear_subjects(self):
        self.subjects = []

    def reset_timetable(self):
        self._build_grid()

    # Utility: convert hour to slot index
    def hour_to_slot(self, hour_float):
        # hour_float like 9.5 -> 9:30
        return int(round((hour_float - self.day_start) * self.slots_per_hour))

    def slot_to_time(self, slot_idx):
        total_minutes = self.day_start * 60 + slot_idx * self.slot_minutes
        h = total_minutes // 60
        m = total_minutes % 60
        return f"{h:02d}:{m:02d}"

    # Core scheduling algorithm
    def generate(self):
        """
        Greedy scheduling:
        1) Create a list of session "tasks" from subjects: each session requires n slots.
        2) Sort tasks by priority and number of remaining possible placements (harder first).
        3) Place each session into best slot according to:
            - preferred days/time ranges
            - respecting max_hours_per_day
            - avoiding back-to-back if requested
        4) If fails to place some sessions, return partial timetable plus list of unplaced.
        """
        self.reset_timetable()
        tasks = []
        for subj in self.subjects:
            slots_needed = max(1, subj.session_length_min // self.slot_minutes)
            # create tasks
            for i in range(subj.sessions_per_week):
                tasks.append({
                    "subject": subj,
                    "slots_needed": slots_needed,
                    "id": f"{subj.name}#{i+1}"
                })

        # Shuffle tasks to introduce variety, then sort by priority descending and slots_needed desc
        random.shuffle(tasks)
        tasks.sort(key=lambda t: (-t["subject"].priority, -t["slots_needed"], t["subject"].name))

        unplaced = []
        # Track hours used per day
        used_slots_per_day = [0] * len(self.days)

        for task in tasks:
            subj = task["subject"]
            placed = self._place_task_greedy(subj, task["slots_needed"], used_slots_per_day)
            if not placed:
                unplaced.append(task)

        return unplaced

    def _place_task_greedy(self, subj, slots_needed, used_slots_per_day):
        """
        Evaluate potential placements and pick best:
        - Candidate slots are day, slot_start where contiguous slots are free
        - Score candidates by:
            * day preferred (1.0) vs not (0.6)
            * time within preferred range (1.0) vs outside (0.5)
            * lower used_slots_per_day favored (spread)
            * penalize if back-to-back violation would occur
        """
        candidates = []
        preferred_days_set = set(subj.preferred_days)
        start_slot_pref = self.hour_to_slot(subj.time_range[0])
        end_slot_pref = self.hour_to_slot(subj.time_range[1])

        for d_idx, day in enumerate(self.days):
            # Skip if day not preferred? We still allow but with lower score
            day_pref = 1.0 if day in preferred_days_set else 0.6

            for slot_start in range(0, self.num_slots_per_day - slots_needed + 1):
                # check contiguous slots free
                free = True
                for s in range(slot_start, slot_start + slots_needed):
                    if self.timetable[d_idx][s] is not None:
                        free = False
                        break
                if not free:
                    continue

                # check daily max constraint if we place here
                if (used_slots_per_day[d_idx] + slots_needed) * (self.slot_minutes / 60.0) > self.max_hours_per_day:
                    continue

                # time preference
                time_pref = 1.0 if (slot_start >= start_slot_pref and (slot_start + slots_needed) <= end_slot_pref) else 0.5

                # avoid back-to-back: check neighbor slots before and after
                back_to_back_penalty = 1.0
                if subj.avoid_back_to_back:
                    before = slot_start - 1
                    after = slot_start + slots_needed
                    if before >= 0 and self.timetable[d_idx][before] is not None:
                        back_to_back_penalty *= 0.3
                    if after < self.num_slots_per_day and self.timetable[d_idx][after] is not None:
                        back_to_back_penalty *= 0.3

                # spread score: prefer days with lower usage
                spread_score = 1.0 / (1.0 + used_slots_per_day[d_idx])

                # compactness: slight prefer midday over extremes
                mid = self.num_slots_per_day / 2
                dist = abs(slot_start + slots_needed/2 - mid)
                comp_score = 1.0 / (1.0 + dist/5.0)

                score = day_pref * time_pref * spread_score * back_to_back_penalty * comp_score

                candidates.append((score, d_idx, slot_start))

        if not candidates:
            return False

        # pick best candidate by score
        candidates.sort(key=lambda x: -x[0])
        best = candidates[0]
        _, d_idx, slot_start = best

        # place
        for s in range(slot_start, slot_start + slots_needed):
            self.timetable[d_idx][s] = (subj.name, slots_needed)  # store slots_needed for convenience

        used_slots_per_day[d_idx] += slots_needed
        return True

    # Simple optimizer: try random swaps between scheduled sessions to improve spread/score
    def optimize(self, iterations=500):
        """
        Attempt improving timetable by swapping two session placements.
        Evaluate using a heuristic "happiness" score: prefers:
            - sessions in preferred days/time
            - balanced load across days
            - respecting avoid_back_to_back
        """
        def hash_session_positions():
            sessions = {}
            for d_idx in range(len(self.days)):
                s = 0
                while s < self.num_slots_per_day:
                    cell = self.timetable[d_idx][s]
                    if cell is None:
                        s += 1
                        continue
                    subj_name, length = cell
                    # find session block start: ensure we only record once per block
                    # record position by name + start slot
                    if (s == 0) or (self.timetable[d_idx][s-1] is None):
                        sessions.setdefault(subj_name, []).append((d_idx, s, length))
                    s += length
            return sessions

        def score_timetable():
            score = 0.0
            used = [0]*len(self.days)
            for subj in self.subjects:
                # for all session placements of this subject
                positions = []
                for d_idx in range(len(self.days)):
                    s = 0
                    while s < self.num_slots_per_day:
                        c = self.timetable[d_idx][s]
                        if c and c[0] == subj.name and ((s==0) or (self.timetable[d_idx][s-1] is None)):
                            positions.append((d_idx, s, c[1]))
                            used[d_idx] += c[1]
                            s += c[1]
                        else:
                            s += 1
                # reward being placed on preferred days/time
                for (d_idx, s0, length) in positions:
                    day = self.days[d_idx]
                    if day in subj.preferred_days:
                        score += 2.0
                    start_pref = self.hour_to_slot(subj.time_range[0])
                    end_pref = self.hour_to_slot(subj.time_range[1])
                    if s0 >= start_pref and (s0+length) <= end_pref:
                        score += 2.0
                    # penalize back-to-back if requested
                    if subj.avoid_back_to_back:
                        before = s0 - 1
                        after = s0 + length
                        if before >= 0 and self.timetable[d_idx][before] is not None:
                            score -= 1.5
                        if after < self.num_slots_per_day and self.timetable[d_idx][after] is not None:
                            score -= 1.5
            # penalize unbalanced days
            avg_used = sum(used)/len(used) if used else 0.0
            var = sum((u - avg_used)**2 for u in used)
            score -= 0.1 * var
            return score

        best_score = score_timetable()
        best_state = [row[:] for row in self.timetable]

        # gather session blocks
        for it in range(iterations):
            # pick two random session starts and swap them if lengths match
            sessions = []
            for d_idx in range(len(self.days)):
                s = 0
                while s < self.num_slots_per_day:
                    c = self.timetable[d_idx][s]
                    if c:
                        name, length = c
                        # ensure start of block
                        if (s == 0) or (self.timetable[d_idx][s-1] is None):
                            sessions.append((d_idx, s, name, length))
                            s += length
                        else:
                            s += 1
                    else:
                        s += 1
            if len(sessions) < 2:
                break
            a, b = random.sample(sessions, 2)
            (d1, s1, name1, len1) = a
            (d2, s2, name2, len2) = b
            # only try swapping blocks with same length
            if len1 != len2:
                continue
            # perform swap
            # clear blocks
            for s in range(s1, s1+len1):
                self.timetable[d1][s] = None
            for s in range(s2, s2+len2):
                self.timetable[d2][s] = None
            # place swapped
            can_place = True
            for s in range(s2, s2+len2):
                if self.timetable[d1][s] is not None:
                    can_place = False
                    break
            for s in range(s1, s1+len1):
                if self.timetable[d2][s] is not None:
                    can_place = False
                    break
            if can_place:
                for s in range(s2, s2+len2):
                    self.timetable[d1][s] = (name2, len2)
                for s in range(s1, s1+len1):
                    self.timetable[d2][s] = (name1, len1)
                new_score = score_timetable()
                if new_score > best_score:
                    best_score = new_score
                    best_state = [row[:] for row in self.timetable]
                else:
                    # revert
                    for s in range(s1, s1+len1):
                        self.timetable[d2][s] = None
                    for s in range(s2, s2+len2):
                        self.timetable[d1][s] = None
                    for s in range(s1, s1+len1):
                        self.timetable[d1][s] = (name1, len1)
                    for s in range(s2, s2+len2):
                        self.timetable[d2][s] = (name2, len2)
            else:
                # revert clear
                for s in range(s1, s1+len1):
                    self.timetable[d1][s] = (name1, len1)
                for s in range(s2, s2+len2):
                    self.timetable[d2][s] = (name2, len2)
        # restore best
        self.timetable = [row[:] for row in best_state]
        return best_score

    def export_csv(self, path):
        """
        Export timetable to CSV: columns Day, Start, End, Subject
        """
        rows = []
        for d_idx, day in enumerate(self.days):
            s = 0
            while s < self.num_slots_per_day:
                c = self.timetable[d_idx][s]
                if c:
                    subj_name, length = c
                    start_time = self.slot_to_time(s)
                    end_time = self.slot_to_time(s + length)
                    rows.append([day, start_time, end_time, subj_name])
                    s += length
                else:
                    s += 1
        with open(path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Day", "Start", "End", "Subject"])
            writer.writerows(rows)

    def to_serializable(self):
        return {
            "days": self.days,
            "day_start": self.day_start,
            "day_end": self.day_end,
            "max_hours_per_day": self.max_hours_per_day,
            "subjects": [s.to_dict() for s in self.subjects],
            # timetable: list of placements
            "placements": [
                {
                    "day": self.days[d_idx],
                    "slot_start": s,
                    "length_slots": self.timetable[d_idx][s][1],
                    "subject": self.timetable[d_idx][s][0]
                } for d_idx in range(len(self.days)) for s in range(self.num_slots_per_day)
                if self.timetable[d_idx][s] is not None and (s == 0 or self.timetable[d_idx][s-1] is None)
            ]
        }

    def load_from_serializable(self, data):
        self.days = data.get("days", self.days)
        self.day_start = data.get("day_start", self.day_start)
        self.day_end = data.get("day_end", self.day_end)
        self.max_hours_per_day = data.get("max_hours_per_day", self.max_hours_per_day)
        self._build_grid()
        self.subjects = [Subject.from_dict(sd) for sd in data.get("subjects", [])]
        # place placements
        for p in data.get("placements", []):
            try:
                d_idx = self.days.index(p["day"])
                slot_start = int(p["slot_start"])
                length = int(p["length_slots"])
                subj_name = p["subject"]
                for s in range(slot_start, slot_start+length):
                    self.timetable[d_idx][s] = (subj_name, length)
            except Exception:
                continue

# ----------------------------
# Tkinter UI
# ----------------------------
class SmartTimetableUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Timetable Generator")
        self.engine = TimetableEngine()
        self._build_ui()
        self.refresh_subject_list()
        self.draw_timetable()

    def _build_ui(self):
        # left panel - subject form
        left = ttk.Frame(self.root, padding=8)
        left.pack(side="left", fill="y")

        ttk.Label(left, text="Add Subject", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(0,6))
        ttk.Label(left, text="Name").pack(anchor="w")
        self.name_entry = ttk.Entry(left, width=24)
        self.name_entry.pack(anchor="w", pady=2)

        ttk.Label(left, text="Sessions / week").pack(anchor="w")
        self.sessions_entry = ttk.Entry(left, width=10)
        self.sessions_entry.insert(0, "2")
        self.sessions_entry.pack(anchor="w", pady=2)

        ttk.Label(left, text="Session length (minutes)").pack(anchor="w")
        self.length_entry = ttk.Entry(left, width=10)
        self.length_entry.insert(0, "60")
        self.length_entry.pack(anchor="w", pady=2)

        ttk.Label(left, text="Priority (1 low - 5 high)").pack(anchor="w")
        self.priority_entry = ttk.Entry(left, width=6)
        self.priority_entry.insert(0, "3")
        self.priority_entry.pack(anchor="w", pady=2)

        ttk.Label(left, text="Preferred days (comma)").pack(anchor="w")
        self.pref_days_entry = ttk.Entry(left, width=24)
        self.pref_days_entry.insert(0, ",".join(DEFAULT_DAYS))
        self.pref_days_entry.pack(anchor="w", pady=2)

        ttk.Label(left, text="Preferred time range (start-end hour)").pack(anchor="w")
        self.time_range_entry = ttk.Entry(left, width=16)
        self.time_range_entry.insert(0, "8-18")
        self.time_range_entry.pack(anchor="w", pady=2)

        self.avoid_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left, text="Avoid back-to-back sessions", variable=self.avoid_var).pack(anchor="w", pady=6)

        ttk.Button(left, text="Add / Update Subject", command=self.add_subject).pack(anchor="w", pady=(4,2))
        ttk.Button(left, text="Remove Selected Subject", command=self.remove_subject).pack(anchor="w", pady=2)
        ttk.Button(left, text="Clear Subjects", command=self.clear_subjects).pack(anchor="w", pady=2)

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=8)

        # constraints
        ttk.Label(left, text="Global Constraints", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ttk.Label(left, text="Days (comma)").pack(anchor="w")
        self.days_entry = ttk.Entry(left, width=24)
        self.days_entry.insert(0, ",".join(self.engine.days))
        self.days_entry.pack(anchor="w", pady=2)

        ttk.Label(left, text="Day start hour").pack(anchor="w")
        self.start_entry = ttk.Entry(left, width=10)
        self.start_entry.insert(0, str(self.engine.day_start))
        self.start_entry.pack(anchor="w", pady=2)

        ttk.Label(left, text="Day end hour").pack(anchor="w")
        self.end_entry = ttk.Entry(left, width=10)
        self.end_entry.insert(0, str(self.engine.day_end))
        self.end_entry.pack(anchor="w", pady=2)

        ttk.Label(left, text="Max hours per day").pack(anchor="w")
        self.max_hours_entry = ttk.Entry(left, width=10)
        self.max_hours_entry.insert(0, str(self.engine.max_hours_per_day))
        self.max_hours_entry.pack(anchor="w", pady=2)

        ttk.Button(left, text="Apply Constraints", command=self.apply_constraints).pack(anchor="w", pady=6)

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(left, text="Project", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ttk.Button(left, text="Generate Timetable", command=self.generate_timetable).pack(anchor="w", pady=4)
        ttk.Button(left, text="Optimize Timetable", command=self.optimize_timetable).pack(anchor="w", pady=4)
        ttk.Button(left, text="Export CSV", command=self.export_csv).pack(anchor="w", pady=4)
        ttk.Button(left, text="Save Project", command=self.save_project).pack(anchor="w", pady=4)
        ttk.Button(left, text="Load Project", command=self.load_project).pack(anchor="w", pady=4)

        # middle panel - subject list & timetable grid
        middle = ttk.Frame(self.root, padding=8)
        middle.pack(side="left", fill="both", expand=True)

        ttk.Label(middle, text="Subjects", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.subject_listbox = tk.Listbox(middle, height=8)
        self.subject_listbox.pack(fill="x", pady=4)

        ttk.Separator(middle, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(middle, text="Timetable", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.canvas = tk.Canvas(middle, bg="#ffffff")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.draw_timetable())

        # right panel - info/log
        right = ttk.Frame(self.root, padding=8, width=240)
        right.pack(side="right", fill="y")
        ttk.Label(right, text="Info", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.info_text = tk.Text(right, height=20, width=36)
        self.info_text.pack(fill="y")

    # ----------------------------
    # Subject management
    # ----------------------------
    def add_subject(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input required", "Enter subject name.")
            return
        try:
            sessions = int(self.sessions_entry.get())
            length = int(self.length_entry.get())
            priority = int(self.priority_entry.get())
            pref_days_raw = [p.strip() for p in self.pref_days_entry.get().split(",") if p.strip()]
            time_parts = self.time_range_entry.get().strip().split("-")
            start = int(time_parts[0])
            end = int(time_parts[1]) if len(time_parts) > 1 else start + 1
            avoid = bool(self.avoid_var.get())
        except Exception:
            messagebox.showerror("Invalid input", "Check numeric fields and formats.")
            return
        subj = Subject(name, sessions, length, priority, pref_days_raw or DEFAULT_DAYS.copy(), (start, end), avoid)
        # if exists, update; else add
        for s in self.engine.subjects:
            if s.name == subj.name:
                s.sessions_per_week = subj.sessions_per_week
                s.session_length_min = subj.session_length_min
                s.priority = subj.priority
                s.preferred_days = subj.preferred_days
                s.time_range = subj.time_range
                s.avoid_back_to_back = subj.avoid_back_to_back
                self.refresh_subject_list()
                self.log(f"Updated subject {subj.name}")
                return
        self.engine.add_subject(subj)
        self.refresh_subject_list()
        self.log(f"Added subject {subj.name}")

    def remove_subject(self):
        sel = self.subject_listbox.curselection()
        if not sel:
            messagebox.showinfo("Select subject", "Select a subject to remove.")
            return
        name = self.subject_listbox.get(sel[0])
        self.engine.remove_subject(name)
        self.refresh_subject_list()
        self.log(f"Removed subject {name}")

    def clear_subjects(self):
        if messagebox.askyesno("Confirm", "Clear all subjects?"):
            self.engine.clear_subjects()
            self.refresh_subject_list()
            self.log("Cleared subjects")

    def refresh_subject_list(self):
        self.subject_listbox.delete(0, tk.END)
        for s in self.engine.subjects:
            self.subject_listbox.insert(tk.END, s.name)
        self.draw_timetable()

    # ----------------------------
    # Constraints / generate / optimize
    # ----------------------------
    def apply_constraints(self):
        try:
            days_raw = [d.strip() for d in self.days_entry.get().split(",") if d.strip()]
            start = int(self.start_entry.get())
            end = int(self.end_entry.get())
            maxh = float(self.max_hours_entry.get())
            if not days_raw:
                messagebox.showwarning("Input", "Provide at least one day.")
                return
            self.engine.days = days_raw
            self.engine.day_start = start
            self.engine.day_end = end
            self.engine.max_hours_per_day = maxh
            self.engine._build_grid()
            self.log("Applied constraints and rebuilt grid.")
            self.draw_timetable()
        except Exception:
            messagebox.showerror("Invalid input", "Check constraints inputs.")

    def generate_timetable(self):
        if not self.engine.subjects:
            messagebox.showwarning("No subjects", "Add subjects first.")
            return
        unplaced = self.engine.generate()
        self.draw_timetable()
        if not unplaced:
            self.log("All sessions placed successfully.")
            messagebox.showinfo("Done", "Timetable generated - all sessions placed.")
        else:
            names = ", ".join(task["subject"].name for task in unplaced)
            self.log(f"Could not place {len(unplaced)} sessions: {names}")
            messagebox.showwarning("Partial", f"Could not place {len(unplaced)} sessions. Check constraints or priorities.")

    def optimize_timetable(self):
        self.log("Optimizing timetable (this may take a moment)...")
        score = self.engine.optimize(iterations=800)
        self.draw_timetable()
        self.log(f"Optimization complete. Score: {score:.2f}")
        messagebox.showinfo("Optimized", f"Optimization finished. Score: {score:.2f}")

    # ----------------------------
    # Export / Save / Load
    # ----------------------------
    def export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        try:
            self.engine.export_csv(path)
            self.log(f"Exported timetable to {path}")
            messagebox.showinfo("Exported", f"Timetable exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export failed", str(e))

    def save_project(self):
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files","*.json")])
        if not path:
            return
        try:
            data = self.engine.to_serializable()
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.log(f"Saved project to {path}")
            messagebox.showinfo("Saved", f"Project saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Save failed", str(e))

    def load_project(self):
        path = filedialog.askopenfilename(filetypes=[("JSON files","*.json")])
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.engine.load_from_serializable(data)
            self.refresh_subject_list()
            self.days_entry.delete(0, tk.END)
            self.days_entry.insert(0, ",".join(self.engine.days))
            self.start_entry.delete(0, tk.END)
            self.start_entry.insert(0, str(self.engine.day_start))
            self.end_entry.delete(0, tk.END)
            self.end_entry.insert(0, str(self.engine.day_end))
            self.max_hours_entry.delete(0, tk.END)
            self.max_hours_entry.insert(0, str(self.engine.max_hours_per_day))
            self.draw_timetable()
            self.log(f"Loaded project from {path}")
        except Exception as e:
            messagebox.showerror("Load failed", str(e))

    # ----------------------------
    # UI drawing / helpers
    # ----------------------------
    def draw_timetable(self):
        # draw grid with day columns and time rows
        self.canvas.delete("all")
        w = max(600, self.canvas.winfo_width())
        h = max(320, self.canvas.winfo_height())
        days = self.engine.days
        n_days = len(days)
        cols = n_days
        rows = self.engine.num_slots_per_day

        if cols == 0 or rows == 0:
            return

        margin = 40
        header_h = 30
        cell_w = max(80, (w - margin) / cols)
        cell_h = max(18, (h - header_h - margin) / rows)

        # draw day headers
        for i, day in enumerate(days):
            x = margin + i * cell_w
            self.canvas.create_rectangle(x, 0, x + cell_w, header_h, fill="#f0f0f0")
            self.canvas.create_text(x + cell_w/2, header_h/2, text=day, font=("Segoe UI", 10, "bold"))

        # draw time labels and cells
        for r in range(rows):
            y = header_h + r * cell_h
            # time label for first column
            if r % self.engine.slots_per_hour == 0:
                time_label = self.engine.slot_to_time(r)
                self.canvas.create_text(10, y + cell_h/2, text=time_label, anchor="w", font=("Segoe UI", 9))
            for c in range(cols):
                x = margin + c * cell_w
                # cell background
                self.canvas.create_rectangle(x, y, x + cell_w, y + cell_h, outline="#ddd", fill="#fff")
                cell = self.engine.timetable[c][r] if c < len(self.engine.timetable) and r < len(self.engine.timetable[c]) else None
                if cell and ((r == 0) or (self.engine.timetable[c][r-1] is None)):
                    subj_name, length = cell
                    # draw multi-slot block
                    block_h = length * cell_h
                    self.canvas.create_rectangle(x+1, y+1, x+cell_w-1, y+block_h-1, fill="#cce5ff", outline="#4a90e2")
                    # label
                    self.canvas.create_text(x + 8, y + 12, text=subj_name, anchor="nw", font=("Segoe UI", 9, "bold"))
                    # end time
                    end_time = self.engine.slot_to_time(r + length)
                    self.canvas.create_text(x + 8, y + 28, text=f"{self.engine.slot_to_time(r)} - {end_time}", anchor="nw", font=("Segoe UI", 8))
        # done

    def log(self, text):
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.info_text.insert(tk.END, f"[{ts}] {text}\n")
        self.info_text.see(tk.END)

# ----------------------------
# Run
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = SmartTimetableUI(root)
    root.geometry("1150x700")
    root.mainloop()




#===========================================================================================================================================================================
                                                              Keep learning keep Exploring
#===========================================================================================================================================================================
