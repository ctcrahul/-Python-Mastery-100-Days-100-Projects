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
