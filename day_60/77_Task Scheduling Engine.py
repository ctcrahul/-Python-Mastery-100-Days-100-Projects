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

