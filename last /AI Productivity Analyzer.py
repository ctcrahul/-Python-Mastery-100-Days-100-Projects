import time
import win32gui
import pandas as pd
from datetime import datetime
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from flask import Flask, render_template_string

log_file = "activity_log.csv"

# ---------- LOG ACTIVITY ----------
def log_activity(duration=60):
    print("Tracking started... Press CTRL+C to stop")
    
    data = []
    
    try:
        while True:
            title = get_active_window()
            timestamp = datetime.now()
            data.append([timestamp, title])
            print(timestamp, title)
            time.sleep(duration)
    except KeyboardInterrupt:
        df = pd.DataFrame(data, columns=["Time", "Window"])
        df.to_csv(log_file, mode='a', header=False, index=False)
        print("Tracking saved!")

# ---------- LABEL DATA ----------
def label_data(df):
    productive = ["code", "github", "jupyter", "pycharm", "stack overflow"]
    distracting = ["youtube", "instagram", "reels", "netflix", "whatsapp"]
    
    labels = []
    
    for w in df['Window']:
        w = str(w).lower()
        if any(p in w for p in productive):
            labels.append("Productive")
        elif any(d in w for d in distracting):
            labels.append("Distracting")
        else:
            labels.append("Neutral")
    
    df['Label'] = labels
    return df
# ---------- AI CLASSIFIER ----------
def train_ai(df):
    le = LabelEncoder()
    df['Encoded'] = le.fit_transform(df['Label'])
    
    df['Window'] = df['Window'].astype(str)
    df['Length'] = df['Window'].apply(len)
    
    X = df[['Length']]
    y = df['Encoded']
    
    model = DecisionTreeClassifier()
    model.fit(X, y)
    
    return model, le

# ---------- PRODUCTIVITY SCORE ----------
def productivity_score(df):
    total = len(df)
    productive = len(df[df['Label']=="Productive"])
    score = (productive/total)*100
    return round(score,2)
