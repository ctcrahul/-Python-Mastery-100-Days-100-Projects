"""
Smart Timetable Generator for Students (single-file)

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
       



