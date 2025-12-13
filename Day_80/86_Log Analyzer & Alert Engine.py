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
    def process(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                parsed = self.parse_line(line.strip())
                if not parsed:
                    continue

                ts, level, message = parsed
                self.level_count[level] += 1

                if level == "ERROR":
                    self.errors.append(ts)
                    self.error_messages[message] += 1

    def detect_error_spikes(self):
        spikes = []
        self.errors.sort()

        for i in range(len(self.errors)):
            window_start = self.errors[i]
            window_end = window_start + timedelta(seconds=ERROR_WINDOW_SECONDS)
            count = 0

            for j in range(i, len(self.errors)):
                if self.errors[j] <= window_end:
                    count += 1
                else:
                    break
            if count >= ERROR_SPIKE_THRESHOLD:
                spikes.append((window_start, count))

        return spikes

    def report(self):
        print("\n--- LOG ANALYSIS REPORT ---\n")

        print("Log Levels:")
        for level, count in self.level_count.items():
            print(f"  {level}: {count}")

        print("\nMost Common Errors:")
        for msg, count in self.error_messages.most_common(5):
            print(f"  {count}x {msg}")

        spikes = self.detect_error_spikes()
        if spikes:
            print("\n⚠ ERROR SPIKES DETECTED:")
            for ts, count in spikes:
                print(f"  {count} errors starting at {ts}")
        else:
            print("\nNo error spikes detected.")

        print("\n--- END REPORT ---\n")
