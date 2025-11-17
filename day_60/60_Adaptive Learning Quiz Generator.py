"""
Adaptive Learning Quiz Generator (single-file)

Features:
- Tkinter GUI (quiz mode, practice mode, dashboard)
- Embedded sample question bank (can import CSV with columns: id,question,choices (| separated),answer (index),topic,explanation)
- Tracks user performance per question and per topic using SQLite (persistence)
- Adaptive algorithm: questions sampled with higher probability if user got them wrong recently or low mastery
- Spaced repetition-style scheduling: next_due timestamp, ease factor for each question
- Session stats, history, export progress to CSV
- Works offline; single Python file

Dependencies:
- Python 3.8+
- tkinter (bundled)
- sqlite3 (bundled)
- pandas (optional, only for export convenience) -> pip install pandas

Run:
    python adaptive_quiz.py
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import random
import time
from datetime import datetime, timedelta
import csv
import os
import threading
try:
    import pandas as pd
except Exception:
    pd = None

DB_FILE = "adaptive_quiz.db"
