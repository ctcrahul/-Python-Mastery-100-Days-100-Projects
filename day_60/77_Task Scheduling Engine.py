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
# ------------------------------
# RUNNER
# ------------------------------
def log_history(task_id, stdout, stderr, code):
    conn = sqlite3.connect(HISTORY_DB)
    c = conn.cursor()
    c.execute(
        "INSERT INTO history (task_id, timestamp, stdout, stderr, returncode) VALUES (?, ?, ?, ?, ?)",
        (task_id, datetime.now().isoformat(), stdout, stderr, code),
    )
    conn.commit()
    conn.close()


def run_task(task_id, command):
    try:
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = proc.communicate()
        out = out.decode("utf-8", "ignore")
        err = err.decode("utf-8", "ignore")

        log_history(task_id, out, err, proc.returncode)

    except Exception as e:
        log_history(task_id, "", str(e), -1)


def scheduler_loop():
    print("Scheduler started. Ctrl+C to stop.")

    while True:
        conn = sqlite3.connect(TASK_DB)
        c = conn.cursor()
        c.execute("SELECT id, command, interval, enabled, last_run FROM tasks WHERE enabled = 1")
        tasks = c.fetchall()
        conn.close()

        now = datetime.now()

        for task in tasks:
            tid, cmd, interval, enabled, last_run = task

            if last_run:
                last = datetime.fromisoformat(last_run)
                if (now - last).total_seconds() < interval:
                    continue

            # Run in background thread
            threading.Thread(target=run_task, args=(tid, cmd), daemon=True).start()

            # Update last_run timestamp
            conn = sqlite3.connect(TASK_DB)
            c = conn.cursor()
            c.execute("UPDATE tasks SET last_run = ? WHERE id = ?", (now.isoformat(), tid))
            conn.commit()
            conn.close()

        time.sleep(1)
# ------------------------------
# ARG PARSE
# ------------------------------
def parse_args():
    p = argparse.ArgumentParser(description="Mini Task Scheduler")
    p.add_argument("--add", help="Command to run")
    p.add_argument("--interval", type=int, help="Seconds between runs")
    p.add_argument("--list", action="store_true")
    p.add_argument("--enable", type=int)
    p.add_argument("--disable", type=int)
    p.add_argument("--run", action="store_true")
    return p.parse_args()


def main():
    init_task_db()
    init_history_db()

    args = parse_args()

    if args.add:
        if not args.interval:
            print("You must provide --interval with --add")
            return
        add_task(args.add, args.interval)
        return

    if args.list:
        list_tasks()
        return

    if args.enable is not None:
        enable_task(args.enable)
        return

    if args.disable is not None:
        disable_task(args.disable)
        return

    if args.run:
        scheduler_loop()
        return

    print("No action provided. Use --help.")


if __name__ == "__main__":
    main()
