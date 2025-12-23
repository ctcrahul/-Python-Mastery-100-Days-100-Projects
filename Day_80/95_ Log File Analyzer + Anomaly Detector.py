# Project 95: Log File Analyzer + Anomaly Detector


import re
import pandas as pd
from collections import Counter
from datetime import datetime

LOG_FILE = "server.log"

# -----------------------------
# Parse Log File
# Expected format:
# 2025-01-10 14:22:31 ERROR Database connection failed
# -----------------------------
def parse_logs(file_path):
    pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)"
    records = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            match = re.match(pattern, line.strip())
            if match:
                date, time, level, message = match.groups()
                records.append({
                    "Timestamp": datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M:%S"),
                    "Level": level,
                    "Message": message
                })

    return pd.DataFrame(records)

# -----------------------------
# Log Summary
# -----------------------------
def log_summary(df):
    print("\n--- Log Level Summary ---")
    print(df["Level"].value_counts())

# -----------------------------
# Frequent Error Messages
# -----------------------------
def frequent_errors(df, top_n=5):
    errors = df[df["Level"] == "ERROR"]["Message"]
    counter = Counter(errors)
    print(f"\n--- Top {top_n} Errors ---")
    for msg, count in counter.most_common(top_n):
        print(f"{count} times -> {msg}")

# -----------------------------
# Anomaly Detection (Spike in Errors)
# -----------------------------
def detect_anomalies(df, threshold=5):
    df["Hour"] = df["Timestamp"].dt.hour
    hourly_errors = df[df["Level"] == "ERROR"].groupby("Hour").size()

    print("\n--- Anomaly Detection ---")
    for hour, count in hourly_errors.items():
        if count >= threshold:
            print(f"⚠ High error count at hour {hour}: {count} errors")

# -----------------------------
# MAIN
# -----------------------------
def main():
    df = parse_logs(LOG_FILE)

    if df.empty:
        print("No valid log data found.")
        return

    log_summary(df)
    frequent_errors(df)
    detect_anomalies(df)

if __name__ == "__main__":
    main()
