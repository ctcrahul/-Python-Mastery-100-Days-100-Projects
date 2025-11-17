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

# ---------------------------
# Embedded sample question bank
# ---------------------------
SAMPLE_QUESTIONS = [
    # id, question, choices (| separated), correct_index (0-based), topic, explanation
    (1, "What is the output of 1 + '1' in Python 3?", "TypeError|'2'|11|'1 1'", 0, "Python", "In Python 3, adding int and str raises TypeError."),
    (2, "Which data structure uses LIFO?", "Queue|Stack|Heap|Graph", 1, "Data Structures", "Stack follows Last-In-First-Out ordering."),
    (3, "What's the time complexity of binary search on a sorted list?", "O(n)|O(log n)|O(n log n)|O(1)", 1, "Algorithms", "Binary search halves the search space each step: O(log n)."),
    (4, "Which HTML tag is used for the largest heading?", "<h1>|<h6>|<header>|<head>", 0, "Web", "<h1> is the largest heading tag."),
    (5, "What does SQL stand for?", "Structured Query Language|Simple Query Language|Sequential Query Language|Standard Query Language", 0, "Databases", "SQL stands for Structured Query Language."),
    (6, "Which method adds an element to the end of a Python list?", "append()|add()|push()|insert_end()", 0, "Python", "list.append(x) adds x to the end of the list."),
    (7, "In machine learning, what is overfitting?", "Model performs well on train and test|Model underperforms on all data|Model performs well on train but poorly on unseen data|Model uses too few features", 2, "ML", "Overfitting occurs when a model fits training data too closely and fails on new data."),
    (8, "HTTP status code 404 means:", "OK|Moved Permanently|Not Found|Internal Server Error", 2, "Web", "404 indicates the resource was not found."),
    (9, "Which sorting algorithm is stable?", "Quick Sort|Heap Sort|Merge Sort|Selection Sort", 2, "Algorithms", "Merge sort is stable while quicksort and heapsort typically aren't."),
    (10, "What symbol is used to denote comments in SQL?", "-- | # | // | /* */", 0, "Databases", "SQL uses -- for single-line comments."),
]


# ---------------------------
# Database & Persistence
# ---------------------------
class DBManager:
    def __init__(self, db_path=DB_FILE):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()
        self.lock = threading.Lock()
        # seed sample questions if empty
        if not self.get_any_question():
            self.seed_sample_questions()
            
