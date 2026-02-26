"""
AI Focus Leak Detector
Detects productivity vs distraction using behavior data
"""

import time
import psutil
import pandas as pd
import pygetwindow as gw
from sklearn.ensemble import RandomForestClassifier
from datetime import datetime

data = []

def get_active_window():
    try:
        return gw.getActiveWindow().title
    except:
        return "Unknown"

def get_idle_time():
    return psutil.cpu_percent(interval=1)

print("Tracking started... Press Ctrl+C to stop.")

try:
    while True:
        start = datetime.now()
        window = get_active_window()
        cpu = get_idle_time()
        duration = 5
        
        time.sleep(duration)
        
        data.append({
            "window": window,
            "cpu": cpu,
            "duration": duration,
            "hour": start.hour
        })
        
