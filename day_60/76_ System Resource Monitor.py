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
