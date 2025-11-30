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
