"""
Project 77 — Mini Task Scheduler
Run examples:
    python task_scheduler.py --add "echo hello" --interval 5
    python task_scheduler.py --list
    python task_scheduler.py --run
    python task_scheduler.py --disable 1
    python task_scheduler.py --enable 1

This scheduler:
- Stores tasks in tasks.db (SQLite)
- Runs tasks at fixed intervals (in seconds)
- Logs every execution in history.db
- Supports enabling/disabling tasks
- Runs tasks in background threads
"""

import sqlite3
import threading
import subprocess
import time
from datetime import datetime
import argparse
import os

TASK_DB = "tasks.db"
HISTORY_DB = "history.db"

# ------------------------------
# DB INIT
# ------------------------------
def init_task_db():
    conn = sqlite3.connect(TASK_DB)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            command TEXT NOT NULL,
            interval INTEGER NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            last_run TEXT
        );
        """
    )
    conn.commit()
    conn.close()


def init_history_db():
    conn = sqlite3.connect(HISTORY_DB)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id INTEGER,
            timestamp TEXT,
            stdout TEXT,
            stderr TEXT,
            returncode INTEGER
        );
        """
    )
    conn.commit()
    conn.close()

# ------------------------------
# TASK OPERATIONS
# ------------------------------
def add_task(command, interval):
    conn = sqlite3.connect(TASK_DB)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (command, interval) VALUES (?, ?)", (command, interval))
    conn.commit()
    conn.close()
    print("Task added.")


def list_tasks():
    conn = sqlite3.connect(TASK_DB)
    c = conn.cursor()
    c.execute("SELECT id, command, interval, enabled, last_run FROM tasks")
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("No tasks.")
        return

    for r in rows:
        print(
            f"[{r[0]}] every {r[2]}s | enabled={bool(r[3])} | last_run={r[4]} | {r[1]}"
        )


def enable_task(task_id):
    conn = sqlite3.connect(TASK_DB)
    c = conn.cursor()
    c.execute("UPDATE tasks SET enabled = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Task enabled.")


def disable_task(task_id):
    conn = sqlite3.connect(TASK_DB)
    c = conn.cursor()
    c.execute("UPDATE tasks SET enabled = 0 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    print("Task disabled.")
