"""
Project 86 — Log Analyzer & Alert Engine

Run:
    python log_analyzer.py server.log

Features:
- Counts INFO / WARN / ERROR logs
- Finds error spikes in time windows
- Detects repeated error messages
- Prints a summary report
"""

import sys
from collections import defaultdict, Counter
from datetime import datetime, timedelta


TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
ERROR_SPIKE_THRESHOLD = 3        # errors
ERROR_WINDOW_SECONDS = 60        # time window


class LogAnalyzer:
    def __init__(self):
        self.level_count = Counter()
        self.errors = []
        self.error_messages = Counter()

    def parse_line(self, line):
        try:
            ts_str = line[:19]
            rest = line[20:].strip()
            level, message = rest.split(" ", 1)
            timestamp = datetime.strptime(ts_str, TIME_FORMAT)
            return timestamp, level, message
        except Exception:
            return None
