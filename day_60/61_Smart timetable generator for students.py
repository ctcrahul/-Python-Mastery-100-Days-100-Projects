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

