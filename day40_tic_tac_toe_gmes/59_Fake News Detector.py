"""
Fake News Detector (Single File)
--------------------------------
Features:
 - Load any CSV dataset with columns: "text" and "label"
 - Train TF-IDF + Logistic Regression model
 - Evaluate accuracy, precision, recall, F1
 - Predict single text or classify a full CSV
 - Export results to CSV
 - Tkinter GUI

Label format required:
 - "fake" or "real"
 - or 1 (fake) / 0 (real)

Run:
    python fake_news_detector.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import os
import time
from datetime 
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
from sklearn.pipeline import Pipeline

# --------------------------------------
# Helper for dataset loading
# --------------------------------------
def load_dataset(path):
    df = pd.read_csv(path)

    text_col = None
    label_col = None

    for col in df.columns:
        if col.lower() in ["text", "content", "headline"]:
            text_col = col
        if col.lower() in ["label", "output", "target", "y"]:
            label_col = col

    if text_col is None:
        text_col = df.columns[0]
    if label_col is None:
        label_col = df.columns[1]

    df = df[[text_col, label_col]].rename(columns={text_col: "text", label_col: "label"})

    df["label"] = df["label"].astype(str).str.lower().map(lambda x: 1 if x in ["fake", "1"] else 0)
    df["text"] = df["text"].astype(str).fillna("")

    return df

# --------------------------------------
# Main App
# --------------------------------------
class FakeNewsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fake News Detector")
        self.root.geometry("1000x700")

        self.model = None
        self.dataset = None

        self.build_ui()
    def build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Button(top, text="Load Dataset (CSV)", command=self.load_data).pack(side="left", padx=8)
        ttk.Button(top, text="Train Model", command=self.train_model).pack(side="left", padx=8)
        ttk.Button(top, text="Evaluate Model", command=self.evaluate_model).pack(side="left", padx=8)

        self.status = tk.StringVar(value="Load a dataset to begin.")
        ttk.Label(top, textvariable=self.status, foreground="blue").pack(side="right")
