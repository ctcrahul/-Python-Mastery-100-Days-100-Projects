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

def list_expenses(conn, limit=None, start_date=None, end_date=None, category=None):
    cur = conn.cursor()
    q = "SELECT id, date, amount, category, description FROM expenses WHERE 1=1"
    params = []
    if start_date:
        q += " AND date >= ?"
        params.append(start_date)
    if end_date:
        q += " AND date <= ?"
        params.append(end_date)
    if category:
        q += " AND category = ?"
        params.append(category)
    q += " ORDER BY date DESC"
    if limit:
        q += " LIMIT ?"
        params.append(limit)
    cur.execute(q, params)
    rows = cur.fetchall()
    if not rows:
        print("No expenses found.")
        return
    print(f"{'ID':>3}  {'Date':10}  {'Amount':>10}  {'Category':12}  Description")
    print("-" * 60)
    for r in rows:
        print(f"{r[0]:>3}  {r[1]:10}  {r[2]:10.2f}  {r[3]:12}  {r[4]}")
    print(f"\nTotal: {sum(r[2] for r in rows):.2f} over {len(rows)} record(s).")
def delete_expense(conn, expense_id):
    cur = conn.cursor()
    cur.execute("SELECT id, date, amount, category FROM expenses WHERE id = ?", (expense_id,))
    row = cur.fetchone()
    if not row:
        print("No such expense id.")
        return
    cur.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    print(f"Deleted expense id {expense_id}: {row[1]} {row[2]:.2f} {row[3]}")


def summary_month(conn, year, month):
    month_str = f"{year:04d}-{month:02d}"
    start = month_str + "-01"
    # naive end date: next month minus one; to keep simple we use YYYY-MM-31 and filter by prefix
    cur = conn.cursor()
    cur.execute(
        "SELECT category, SUM(amount) FROM expenses WHERE substr(date,1,7) = ? GROUP BY category ORDER BY SUM(amount) DESC",
        (month_str,),
    )
    rows = cur.fetchall()
    total = sum(r[1] for r in rows) if rows else 0.0
    print(f"Summary for {month_str}: total = {total:.2f}")
    for cat, amt in rows:
        print(f"  {cat:12}  {amt:10.2f}  ({(amt/total*100):5.1f}%)" if total else f"  {cat:12}  {amt:10.2f}")
    return rows, total

def export_csv(conn, filepath):
    cur = conn.cursor()
    cur.execute("SELECT id, date, amount, category, description FROM expenses ORDER BY date")
    rows = cur.fetchall()
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "date", "amount", "category", "description"])
        writer.writerows(rows)
    print(f"Exported {len(rows)} records to {filepath}")


def plot_category_breakdown(rows, total, outpng):
    if plt is None:
        print("matplotlib not available — cannot plot. Install matplotlib and try again.")
        return
    if not rows:
        print("No data to plot.")
        return
    categories = [r[0] for r in rows]
    amounts = [r[1] for r in rows]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(amounts, labels=categories, autopct=lambda p: f"{p:.1f}%\n({p/100*total:.0f})", startangle=90)
    ax.set_title("Category Breakdown")
    plt.tight_layout()
    fig.savefig(outpng)
    plt.close(fig)
    print(f"Saved category breakdown to {outpng}")
