"""
Project 73 — Personal Expense Tracker (single-file Python app)
Run: python expense_tracker.py
Requires: Python 3.8+, matplotlib (for plotting)
What it does:
 - Stores expenses in a local SQLite database
 - Add / list / delete expenses
 - Monthly/category summaries
 - Export CSV
 - Save a pie/bar chart PNG for category breakdown
"""

import sqlite3
import sys
import csv
import argparse
from datetime import datetime
from collections import defaultdict
import os

try:
    import matplotlib.pyplot as plt
except Exception:
    plt = None

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
def init_db(conn):
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,          -- ISO date YYYY-MM-DD
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT
        )
        """
    )
    conn.commit()


def connect():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    return conn


def add_expense(conn, date, amount, category, description=""):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO expenses (date, amount, category, description) VALUES (?, ?, ?, ?)",
        (date, float(amount), category.strip(), description.strip()),
    )
    conn.commit()
    print(f"Added: {date} | {amount:.2f} | {category} | {description}")

