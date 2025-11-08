""                                                  Day = 51 
                         
                                             Currency Converter                                                                                                        ""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import sqlite3
import time
from datetime import datetime, date
import threading
import pandas as pd
import os
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

DB_PATH = "pomodoro.db"

# -------------------------
# Database helpers
# -------------------------
class DB:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                note TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                duration_minutes REAL,
                session_type TEXT, -- work / short_break / long_break
                FOREIGN KEY(task_id) REFERENCES tasks(id)
            )
        """)
        self.conn.commit()

    # Task operations
    def add_task(self, title, note=""):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO tasks (title, note) VALUES (?, ?)", (title.strip(), note.strip()))
        self.conn.commit()
        return cur.lastrowid

    def get_tasks(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id, title, note FROM tasks ORDER BY id DESC")
        return cur.fetchall()

    def delete_task(self, task_id):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        cur.execute("UPDATE sessions SET task_id=NULL WHERE task_id=?", (task_id,))
        self.conn.commit()

    # Session operations
    def log_session(self, task_id, start_time, end_time, duration_minutes, session_type):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO sessions (task_id, start_time, end_time, duration_minutes, session_type)
            VALUES (?, ?, ?, ?, ?)
        """, (task_id, start_time, end_time, duration_minutes, session_type))
        self.conn.commit()
        return cur.lastrowid

    def get_sessions(self, start_date=None, end_date=None):
        cur = self.conn.cursor()
        sql = "SELECT id, task_id, start_time, end_time, duration_minutes, session_type FROM sessions WHERE 1=1 "
        params = []
        if start_date:
            sql += "AND date(start_time) >= date(?) "
            params.append(start_date)
        if end_date:
            sql += "AND date(start_time) <= date(?) "
            params.append(end_date)
        sql += "ORDER BY start_time DESC"
        cur.execute(sql, params)
        return cur.fetchall()

    def close(self):
        self.conn.close()

# -------------------------
# Pomodoro Engine
# -------------------------
class PomodoroEngine:
    def __init__(self, work_min=25, short_break_min=5, long_break_min=15, long_break_after=4):
        self.work_min = work_min
        self.short_break_min = short_break_min
        self.long_break_min = long_break_min
        self.long_break_after = long_break_after

        self._running = False
        self._paused = False
        self._timer_thread = None

        self.current_seconds = 0
        self.current_mode = "idle"  # idle, work, short_break, long_break
        self.session_count = 0  # number of completed work sessions in cycle

        self._on_tick = None
        self._on_mode_change = None
        self._on_session_complete = None

    def set_callbacks(self, on_tick=None, on_mode_change=None, on_session_complete=None):
        self._on_tick = on_tick
        self._on_mode_change = on_mode_change
        self._on_session_complete = on_session_complete

    def start_work(self):
        self._start_mode("work", self.work_min * 60)

    def start_short_break(self):
        self._start_mode("short_break", self.short_break_min * 60)

    def start_long_break(self):
        self._start_mode("long_break", self.long_break_min * 60)

    def _start_mode(self, mode, seconds):
        if self._running:
            self.stop()
        self.current_mode = mode
        self.current_seconds = int(seconds)
        self._running = True
        self._paused = False
        if self._on_mode_change:
            self._on_mode_change(mode)
        # Start a thread for ticking each second
        self._timer_thread = threading.Thread(target=self._run_timer, daemon=True)
        self._timer_thread.start()

    def _run_timer(self):
        while self._running and self.current_seconds > 0:
            if self._paused:
                time.sleep(0.2)
                continue
            time.sleep(1)
            self.current_seconds -= 1
            if self._on_tick:
                self._on_tick(self.current_seconds)
        # If reached zero and not stopped explicitly
        if self._running and self.current_seconds == 0:
            # mark completion
            finished_mode = self.current_mode
            self._running = False
            # update session count if work finished
            if finished_mode == "work":
                self.session_count += 1
            if self._on_session_complete:
                self._on_session_complete(finished_mode)

    def pause(self):
        if self._running:
            self._paused = True

    def resume(self):
        if self._running and self._paused:
            self._paused = False

    def stop(self):
        # stop timer
        self._running = False
        self._paused = False
        self.current_seconds = 0
        self.current_mode = "idle"
        if self._on_mode_change:
            self._on_mode_change("idle")

    def is_running(self):
        return self._running and not self._paused

    def is_paused(self):
        return self._paused

# -------------------------
# UI App
# -------------------------
class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer & Productivity Tracker")
        self.root.geometry("1000x640")
        self.db = DB()

        # Engine with default durations; user can change in settings
        self.engine = PomodoroEngine()
        self.engine.set_callbacks(on_tick=self._on_tick,
                                  on_mode_change=self._on_mode_change,
                                  on_session_complete=self._on_session_complete)

        # Current session bookkeeping
        self.current_task_id = None
        self.session_start_time = None

        self._build_ui()
        self._refresh_tasks()
        self._refresh_history()
        self._update_timer_label(0)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # -------------------------
    # UI build
    # -------------------------
    def _build_ui(self):
        # Top frame: timer & controls
        top = ttk.Frame(self.root, padding=12)
        top.pack(fill="x")

        # Timer display
        timer_frame = ttk.Frame(top)
        timer_frame.pack(side="left", padx=8)

        self.mode_label = ttk.Label(timer_frame, text="Idle", font=("Segoe UI", 14, "bold"))
        self.mode_label.pack(anchor="w")
        self.time_label = ttk.Label(timer_frame, text="00:00", font=("Segoe UI", 48, "bold"))
        self.time_label.pack(pady=6)

        # Timer controls
        controls_frame = ttk.Frame(top)
        controls_frame.pack(side="left", padx=30)

        self.start_btn = ttk.Button(controls_frame, text="Start Work", command=self._start_work)
        self.start_btn.grid(row=0, column=0, padx=6, pady=6)

        self.pause_btn = ttk.Button(controls_frame, text="Pause", command=self._pause, state="disabled")
        self.pause_btn.grid(row=0, column=1, padx=6, pady=6)

        self.resume_btn = ttk.Button(controls_frame, text="Resume", command=self._resume, state="disabled")
        self.resume_btn.grid(row=0, column=2, padx=6, pady=6)

        self.reset_btn = ttk.Button(controls_frame, text="Reset", command=self._reset)
        self.reset_btn.grid(row=0, column=3, padx=6, pady=6)

        # Settings: durations
        settings_frame = ttk.Frame(top)
        settings_frame.pack(side="right", padx=8)

        ttk.Label(settings_frame, text="Work (min)").grid(row=0, column=0, padx=4)
        self.work_var = tk.IntVar(value=self.engine.work_min)
        ttk.Entry(settings_frame, textvariable=self.work_var, width=6).grid(row=0, column=1, padx=4)

        ttk.Label(settings_frame, text="Short Break (min)").grid(row=1, column=0, padx=4)
        self.short_var = tk.IntVar(value=self.engine.short_break_min)
        ttk.Entry(settings_frame, textvariable=self.short_var, width=6).grid(row=1, column=1, padx=4)

        ttk.Label(settings_frame, text="Long Break (min)").grid(row=2, column=0, padx=4)
        self.long_var = tk.IntVar(value=self.engine.long_break_min)
        ttk.Entry(settings_frame, textvariable=self.long_var, width=6).grid(row=2, column=1, padx=4)

        ttk.Label(settings_frame, text="Long after (work sessions)").grid(row=3, column=0, padx=4)
        self.long_after_var = tk.IntVar(value=self.engine.long_break_after)
        ttk.Entry(settings_frame, textvariable=self.long_after_var, width=6).grid(row=3, column=1, padx=4)

        ttk.Button(settings_frame, text="Apply", command=self._apply_settings).grid(row=4, column=0, columnspan=2, pady=6)

        # Middle: tasks & history
        middle = ttk.Frame(self.root, padding=8)
        middle.pack(fill="both", expand=True)

        # Left: tasks
        left = ttk.Frame(middle)
        left.pack(side="left", fill="y", padx=8)

        ttk.Label(left, text="Tasks", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.tasks_tree = ttk.Treeview(left, columns=("id", "title"), show="headings", height=10)
        self.tasks_tree.heading("id", text="ID")
        self.tasks_tree.heading("title", text="Title")
        self.tasks_tree.column("id", width=40, anchor="center")
        self.tasks_tree.column("title", width=240)
        self.tasks_tree.pack(fill="y", expand=True)

        task_btn_frame = ttk.Frame(left)
        task_btn_frame.pack(fill="x", pady=6)
        ttk.Button(task_btn_frame, text="Add Task", command=self._add_task).pack(side="left", padx=4)
        ttk.Button(task_btn_frame, text="Delete Task", command=self._delete_task).pack(side="left", padx=4)
        ttk.Button(task_btn_frame, text="Select Task", command=self._select_task).pack(side="left", padx=4)

        # Show selected task
        self.selected_task_label = ttk.Label(left, text="Selected: None", wraplength=260)
        self.selected_task_label.pack(anchor="w", pady=6)

        # Right: history and charts
        right = ttk.Frame(middle)
        right.pack(side="right", fill="both", expand=True, padx=8)

        top_right_controls = ttk.Frame(right)
        top_right_controls.pack(fill="x")
        ttk.Button(top_right_controls, text="Refresh History", command=self._refresh_history).pack(side="left", padx=4)
        ttk.Button(top_right_controls, text="Export CSV", command=self._export_csv).pack(side="left", padx=4)
        ttk.Button(top_right_controls, text="Clear Chart", command=self._clear_chart).pack(side="left", padx=4)

        ttk.Label(right, text="Session History", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(8,0))
        self.history_tree = ttk.Treeview(right, columns=("id","task","start","end","duration","type"), show="headings", height=8)
        for c, w in [("id",40), ("task",180), ("start",160), ("end",160), ("duration",80), ("type",100)]:
            self.history_tree.heading(c, text=c.title())
            self.history_tree.column(c, width=w, anchor="w")
        self.history_tree.pack(fill="both", expand=False, pady=6)

        # Chart area
        chart_holder = ttk.Frame(right)
        chart_holder.pack(fill="both", expand=True, pady=6)
        self.chart_container = chart_holder

    # -------------------------
    # Task actions
    # -------------------------
    def _add_task(self):
        title = simpledialog.askstring("New task", "Task title (required):", parent=self.root)
        if not title:
            return
        note = simpledialog.askstring("Task note (optional)", "Note or description:", parent=self.root)
        task_id = self.db.add_task(title, note or "")
        messagebox.showinfo("Task added", f"Task '{title}' added (id {task_id}).")
        self._refresh_tasks()

    def _delete_task(self):
        sel = self.tasks_tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Select a task to delete.")
            return
        item = self.tasks_tree.item(sel[0])
        task_id = item["values"][0]
        if messagebox.askyesno("Confirm", f"Delete task id {task_id}?"):
            self.db.delete_task(task_id)
            self._refresh_tasks()
            if self.current_task_id == task_id:
                self.current_task_id = None
                self.selected_task_label.config(text="Selected: None")

    def _select_task(self):
        sel = self.tasks_tree.selection()
        if not sel:
            messagebox.showinfo("Select", "Select a task first.")
            return
        item = self.tasks_tree.item(sel[0])
        self.current_task_id = item["values"][0]
        title = item["values"][1]
        self.selected_task_label.config(text=f"Selected: {title} (id {self.current_task_id})")

    def _refresh_tasks(self):
        self.tasks_tree.delete(*self.tasks_tree.get_children())
        for t in self.db.get_tasks():
            self.tasks_tree.insert("", "end", values=(t[0], t[1]))

    # -------------------------
    # Timer control handlers
    # -------------------------
    def _apply_settings(self):
        try:
            work = int(self.work_var.get())
            shortb = int(self.short_var.get())
            longb = int(self.long_var.get())
            long_after = int(self.long_after_var.get())
            if work <= 0 or shortb < 0 or longb < 0 or long_after <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid", "Enter valid positive integer settings.")
            return
        self.engine.work_min = work
        self.engine.short_break_min = shortb
        self.engine.long_break_min = longb
        self.engine.long_break_after = long_after
        messagebox.showinfo("Settings", "Pomodoro settings updated.")

    def _start_work(self):
        # require a selected task for logging work sessions
        if not self.current_task_id:
            if not messagebox.askyesno("No task", "No task selected. Start work without a task?"):
                return
        # set durations from UI
        self._apply_settings()
        self.engine.start_work()
        self.session_start_time = datetime.utcnow()
        self._update_buttons_on_start()

    def _pause(self):
        self.engine.pause()
        self.pause_btn.config(state="disabled")
        self.resume_btn.config(state="normal")

    def _resume(self):
        self.engine.resume()
        self.pause_btn.config(state="normal")
        self.resume_btn.config(state="disabled")

    def _reset(self):
        self.engine.stop()
        self._update_timer_label(0)
        self._update_buttons_on_reset()
        self.session_start_time = None

    def _update_buttons_on_start(self):
        self.start_btn.config(state="disabled")
        self.pause_btn.config(state="normal")
        self.resume_btn.config(state="disabled")
        self.reset_btn.config(state="normal")

    def _update_buttons_on_complete(self):
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.resume_btn.config(state="disabled")
        self.reset_btn.config(state="normal")

    def _update_buttons_on_reset(self):
        self.start_btn.config(state="normal")
        self.pause_btn.config(state="disabled")
        self.resume_btn.config(state="disabled")
        self.reset_btn.config(state="normal")

    # -------------------------
    # Engine callbacks
    # -------------------------
    def _on_tick(self, remaining_seconds):
        # update UI label (main thread)
        self.root.after(0, lambda: self._update_timer_label(remaining_seconds))

    def _on_mode_change(self, mode):
        # mode: work / short_break / long_break / idle
        label_map = {"work": "Work", "short_break": "Short Break", "long_break": "Long Break", "idle": "Idle"}
        self.root.after(0, lambda: self.mode_label.config(text=label_map.get(mode, mode.title())))

    def _on_session_complete(self, finished_mode):
        # If a work session finished, we log it
        end_time = datetime.utcnow()
        if finished_mode == "work":
            # compute duration from settings
            duration = self.engine.work_min
            start_time = self.session_start_time or (end_time - pd.Timedelta(minutes=duration))
            # log session to DB (task_id may be None)
            self.db.log_session(self.current_task_id, start_time.isoformat(), end_time.isoformat(), duration, "work")
            self.root.after(0, lambda: messagebox.showinfo("Session complete", "Work session completed and logged."))
            self.root.after(0, self._refresh_history)
            # decide next break: short or long
            if self.engine.session_count % self.engine.long_break_after == 0:
                # start long break automatically
                self.engine.start_long_break()
                # don't set session_start_time (breaks not logged to task)
            else:
                self.engine.start_short_break()
        else:
            # finished a break; log break too if you want (we'll log breaks as sessions too)
            duration_min = self.engine.short_break_min if finished_mode == "short_break" else self.engine.long_break_min
            # log break session (task_id None)
            self.db.log_session(None, (end_time - pd.Timedelta(minutes=duration_min)).isoformat(),
                                end_time.isoformat(), duration_min, finished_mode)
            self.root.after(0, self._refresh_history)

        # update buttons once a cycle step completes
        self.root.after(0, self._update_buttons_on_complete)

    # -------------------------
    # Timer UI helpers
    # -------------------------
    def _update_timer_label(self, remaining_seconds):
        mins = remaining_seconds // 60
        secs = remaining_seconds % 60
        self.time_label.config(text=f"{int(mins):02d}:{int(secs):02d}")

    # -------------------------
    # History & Charts
    # -------------------------
    def _refresh_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        sessions = self.db.get_sessions()
        for s in sessions:
            sid, task_id, start, end, duration, s_type = s
            task_title = self._task_title_by_id(task_id)
            start_str = start.split(".")[0] if isinstance(start, str) else str(start)
            end_str = end.split(".")[0] if isinstance(end, str) else str(end)
            self.history_tree.insert("", "end", values=(sid, task_title, start_str, end_str, f"{duration:.1f}", s_type))
        self._draw_charts()

    def _task_title_by_id(self, tid):
        if not tid:
            return "(none)"
        for t in self.db.get_tasks():
            if t[0] == tid:
                return t[1]
        return f"id:{tid}"

    def _draw_charts(self):
        # Clear container
        for w in self.chart_container.winfo_children():
            w.destroy()

        # Prepare data: sessions per day (work sessions only)
        sessions = self.db.get_sessions()
        if not sessions:
            lbl = ttk.Label(self.chart_container, text="No sessions yet — start a Pomodoro to build stats.")
            lbl.pack()
            return

        df = pd.DataFrame(sessions, columns=["id", "task_id", "start_time", "end_time", "duration_minutes", "session_type"])
        df["day"] = pd.to_datetime(df["start_time"]).dt.date
        work_df = df[df["session_type"] == "work"].copy()
        if work_df.empty:
            lbl = ttk.Label(self.chart_container, text="No work sessions yet.")
            lbl.pack()
            return

        counts = work_df.groupby("day").size().reset_index(name="count")
        minutes = work_df.groupby("day")["duration_minutes"].sum().reset_index(name="minutes")

        # Line chart: sessions per day
        fig = Figure(figsize=(6, 3), dpi=100)
        ax = fig.add_subplot(121)
        ax.plot(counts["day"].astype(str), counts["count"], marker="o")
        ax.set_title("Work sessions per day")
        ax.set_xlabel("Day")
        ax.set_ylabel("Sessions")
        ax.tick_params(axis='x', rotation=45)

        # Bar chart: minutes per day
        ax2 = fig.add_subplot(122)
        ax2.bar(minutes["day"].astype(str), minutes["minutes"])
        ax2.set_title("Minutes worked per day")
        ax2.set_xlabel("Day")
        ax2.set_ylabel("Minutes")
        ax2.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def _clear_chart(self):
        for w in self.chart_container.winfo_children():
            w.destroy()

    # -------------------------
    # Exports & utilities
    # -------------------------
    def _export_csv(self):
        sessions = self.db.get_sessions()
        if not sessions:
            messagebox.showinfo("No data", "No sessions to export.")
            return
        df = pd.DataFrame(sessions, columns=["id", "task_id", "start_time", "end_time", "duration_minutes", "session_type"])
        # add task title
        df["task_title"] = df["task_id"].apply(self._task_title_by_id)
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile=f"pomodoro_sessions_{int(time.time())}.csv")
        if not path:
            return
        df.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"Exported to {path}")

    # -------------------------
    # Cleanup
    # -------------------------
    def _on_close(self):
        if self.engine.is_running() or self.engine.is_paused():
            if not messagebox.askyesno("Exit", "Timer is running or paused. Exit anyway?"):
                return
        self.db.close()
        self.root.destroy()

# -------------------------
# Run app
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")  # nicer cross-platform default
    app = PomodoroApp(root)
    root.mainloop()
