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
