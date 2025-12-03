"""
Project 76 — System Resource Monitor
Run examples:
    python resource_monitor.py --interval 2 --duration 20 --metrics cpu ram net
    python resource_monitor.py --plot usage_log.csv

Tracks CPU, RAM, Disk, Network usage and logs values to a CSV file.
Can also generate a usage graph from the CSV.
"""

import psutil
import csv
import time
import argparse
import matplotlib.pyplot as plt
from datetime import datetime
import os


def collect_metrics(metric_list):
    data = {}
    if "cpu" in metric_list:
        data["cpu"] = psutil.cpu_percent(interval=0)
    if "ram" in metric_list:
        data["ram"] = psutil.virtual_memory().percent
    if "disk" in metric_list:
        data["disk"] = psutil.disk_usage("/").percent
    if "net" in metric_list:
        net = psutil.net_io_counters()
        data["net_sent"] = net.bytes_sent
        data["net_recv"] = net.bytes_recv
    return data
def monitor(interval, duration, metrics, logfile):
    fields = ["timestamp"] + metrics

    # Expand net into two fields if needed
    if "net" in metrics:
        fields.remove("net")
        fields.extend(["net_sent", "net_recv"])

    print(f"Logging metrics to {logfile}")
    print("Fields:", fields)

    start = time.time()

    with open(logfile, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(fields)

        while True:
            now = datetime.now().isoformat()
            data = collect_metrics(metrics)

            row = [now]
            for field in fields[1:]:
                row.append(data.get(field, ""))

            writer.writerow(row)
            f.flush()
            print("Logged:", row)

            if time.time() - start >= duration:
                break
            time.sleep(interval)

    print("Monitoring finished.")


def plot_csv(csvfile):
    if not os.path.exists(csvfile):
        print("CSV file not found.")
        return

    timestamps = []
    data = {}

    with open(csvfile, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        fields = next(reader)

        for field in fields:
            if field != "timestamp":
                data[field] = []

        for row in reader:
            timestamps.append(row[0])
            for i, field in enumerate(fields[1:], start=1):
                try:
                    data[field].append(float(row[i]))
                except:
                    data[field].append(0.0)
    plt.figure(figsize=(10, 6))
    for field, values in data.items():
        plt.plot(values, label=field)

    plt.title("System Resource Usage Over Time")
    plt.xlabel("Samples")
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()
    plt.show()


def parse_args():
    parser = argparse.ArgumentParser(description="System Resource Monitor")

    parser.add_argument("--interval", type=int, help="Seconds between samples")
    parser.add_argument("--duration", type=int, help="Total duration in seconds")
    parser.add_argument("--metrics", nargs="*", help="cpu ram disk net")
    parser.add_argument("--log", default="usage_log.csv", help="CSV log file name")
    parser.add_argument("--plot", help="Plot a CSV file")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.plot:
        plot_csv(args.plot)
        return

    if not args.interval or not args.duration or not args.metrics:
        print("Missing required args. Example:")
        print("python resource_monitor.py --interval 2 --duration 20 --metrics cpu ram net")
        return
