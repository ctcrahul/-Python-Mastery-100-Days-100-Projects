"""
AI TIME LEAK DETECTOR
---------------------
This system analyzes user work behavior patterns and detects:

- Focus quality
- Time waste
- Productivity patterns
- Burnout signals

HOW IT WORKS:
1. Simulates activity data (replace later with real tracking)
2. Calculates behavioral metrics
3. Uses ML to predict productivity
4. Detects time leaks via anomaly detection
5. Generates behavioral insights

This is behavioral AI, not just classification.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, IsolationForest
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ---------------------------
# STEP 1: SIMULATE ACTIVITY DATA
# ---------------------------

def generate_activity_data(days=7):
    """
    Generates simulated work activity data.
    Replace this later with real tracking data.
    """
    data = []

    start_time = datetime.now() - timedelta(days=days)

    for i in range(days * 24):
        hour = (start_time + timedelta(hours=i)).hour

        # simulate realistic behavior
        if 9 <= hour <= 12:
            typing = np.random.randint(200, 400)
            switches = np.random.randint(2, 5)
            idle = np.random.randint(5, 15)
        elif 14 <= hour <= 17:
            typing = np.random.randint(150, 300)
            switches = np.random.randint(3, 8)
            idle = np.random.randint(10, 25)
        elif 21 <= hour <= 23:
            typing = np.random.randint(50, 150)
            switches = np.random.randint(8, 15)
            idle = np.random.randint(25, 45)
        else:
            typing = np.random.randint(0, 80)
            switches = np.random.randint(1, 6)
            idle = np.random.randint(20, 60)
        session = np.random.randint(20, 60)

        data.append([
            hour,
            typing,
            switches,
            idle,
            session
        ])

    df = pd.DataFrame(data, columns=[
        "hour",
        "keystrokes",
        "app_switches",
        "idle_time",
        "session_length"
    ])

    return df

# ---------------------------
# STEP 2: CALCULATE FOCUS SCORE
# ---------------------------

def calculate_focus_score(df):
    """
    Calculates focus score based on behavior
    """
    df["focus_score"] = (
        (df["keystrokes"] / 400) * 0.4 +
        (1 - df["app_switches"] / 15) * 0.3 +
        (1 - df["idle_time"] / 60) * 0.3
    )

    df["focus_score"] = df["focus_score"].clip(0,1)
    return df

# ---------------------------
# STEP 3: PRODUCTIVITY MODEL
# ---------------------------

def train_productivity_model(df):
    """
    Train ML model to predict productivity
    """

    X = df[["keystrokes", "app_switches", "idle_time", "session_length"]]

    # synthetic productivity label
    y = (
        df["keystrokes"] * 0.3 -
        df["app_switches"] * 0.2 -
        df["idle_time"] * 0.3 +
        df["session_length"] * 0.2
    )

    model = RandomForestRegressor()
    model.fit(X, y)

    df["productivity_score"] = model.predict(X)

    return df, model

# ---------------------------
# STEP 4: TIME LEAK DETECTION
# ---------------------------

def detect_time_leaks(df):
    """
    Uses anomaly detection to detect wasteful sessions
    """

    X = df[["keystrokes", "app_switches", "idle_time"]]

    iso = IsolationForest(contamination=0.2)
    df["anomaly"] = iso.fit_predict(X)

    leaks = df[df["anomaly"] == -1]

    return leaks

# ---------------------------
# STEP 5: BURNOUT RISK
# ---------------------------

def burnout_risk(df):
    late_hours = df[df["hour"] >= 21]
    low_focus = late_hours[late_hours["focus_score"] < 0.4]

    risk = len(low_focus) / max(len(late_hours),1)

    if risk > 0.6:
        return "High"
    elif risk > 0.3:
        return "Moderate"
    else:
        return "Low"
