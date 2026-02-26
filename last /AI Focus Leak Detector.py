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
        
except KeyboardInterrupt:
    print("Tracking stopped.")

df = pd.DataFrame(data)

def label(row):
    if row["cpu"] > 40:
        return "Focused"
    elif "youtube" in row["window"].lower():
        return "Distracted"
    else:
        return "Idle"

df["label"] = df.apply(label, axis=1)

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df["window_encoded"] = le.fit_transform(df["window"])
df["label_encoded"] = le.fit_transform(df["label"])

X = df[["window_encoded", "cpu", "hour"]]
y = df["label_encoded"]

model = RandomForestClassifier()
model.fit(X, y)

print("\nAI Training Complete")
