"""                                                                    Day = 59
                      
                                                                  Fake News Detector 
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
from datetime import datetime
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

        # Text input for prediction
        input_frame = ttk.LabelFrame(self.root, text="Single Prediction", padding=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        self.single_text = tk.Text(input_frame, height=6)
        self.single_text.pack(fill="x")

        ttk.Button(input_frame, text="Predict", command=self.predict_single).pack(pady=5)
        self.single_result = tk.StringVar(value="No prediction yet.")
        ttk.Label(input_frame, textvariable=self.single_result).pack()

        # Batch prediction
        batch_frame = ttk.LabelFrame(self.root, text="Batch Prediction", padding=10)
        batch_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(batch_frame, text="Classify CSV File", command=self.batch_predict).pack()

        # Metrics Panel
        metrics_frame = ttk.LabelFrame(self.root, text="Evaluation Metrics", padding=10)
        metrics_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.metrics_text = tk.Text(metrics_frame, height=12)
        self.metrics_text.pack(fill="both", expand=True)

        # Confusion Matrix
        self.cm_frame = ttk.LabelFrame(self.root, text="Confusion Matrix", padding=10)
        self.cm_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # --------------------------------------
    # Load dataset
    # --------------------------------------
    def load_data(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        
        try:
            self.dataset = load_dataset(path)
            self.status.set(f"Dataset loaded: {len(self.dataset)} samples")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # --------------------------------------
    # Train Model
    # --------------------------------------
    def train_model(self):
        if self.dataset is None:
            messagebox.showwarning("Error", "Load dataset first.")
            return

        X = self.dataset["text"]
        y = self.dataset["label"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        self.model = Pipeline([
            ("tfidf", TfidfVectorizer(stop_words="english", max_features=50000)),
            ("clf", LogisticRegression(max_iter=2000))
        ])

        self.model.fit(self.X_train, self.y_train)
        self.status.set("Model trained successfully.")

    # --------------------------------------
    # Evaluate Model
    # --------------------------------------
    def evaluate_model(self):
        if self.model is None:
            messagebox.showwarning("Error", "Train the model first.")
            return

        preds = self.model.predict(self.X_test)

        acc = accuracy_score(self.y_test, preds)
        prec = precision_score(self.y_test, preds)
        rec = recall_score(self.y_test, preds)
        f1 = f1_score(self.y_test, preds)

        cm = confusion_matrix(self.y_test, preds)

        self.metrics_text.delete("1.0", tk.END)
        self.metrics_text.insert(
            tk.END,
            f"Accuracy: {acc:.4f}\n"
            f"Precision: {prec:.4f}\n"
            f"Recall: {rec:.4f}\n"
            f"F1 Score: {f1:.4f}\n\n"
            + classification_report(self.y_test, preds)
        )

        self.plot_confusion_matrix(cm)

    # --------------------------------------
    # Confusion Matrix Plot
    # --------------------------------------
    def plot_confusion_matrix(self, cm):
        for widget in self.cm_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.imshow(cm, cmap="Blues")
        ax.set_xticks([0, 1])
        ax.set_yticks([0, 1])
        ax.set_xticklabels(["Real", "Fake"])
        ax.set_yticklabels(["Real", "Fake"])

        for i in range(2):
            for j in range(2):
                ax.text(j, i, cm[i, j], ha="center", va="center")

        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")

        canvas = FigureCanvasTkAgg(fig, master=self.cm_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # --------------------------------------
    # Single Text Prediction
    # --------------------------------------
    def predict_single(self):
        if self.model is None:
            messagebox.showwarning("Error", "Train model first.")
            return

        text = self.single_text.get("1.0", tk.END).strip()
        if not text:
            return

        pred = self.model.predict([text])[0]
        label = "FAKE NEWS" if pred == 1 else "REAL NEWS"

        self.single_result.set(f"Prediction: {label}")

    # --------------------------------------
    # Batch Prediction
    # --------------------------------------
    def batch_predict(self):
        if self.model is None:
            messagebox.showwarning("Error", "Train model first.")
            return

        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        
        df = pd.read_csv(path)
        text_col = df.columns[0]

        preds = self.model.predict(df[text_col].astype(str))

        df["predicted_label"] = ["fake" if p == 1 else "real" for p in preds]

        save_path = filedialog.asksaveasfilename(defaultextension=".csv")
        if save_path:
            df.to_csv(save_path, index=False)
            messagebox.showinfo("Success", f"Results saved to {save_path}")


# --------------------------------------
# Run App
# --------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = FakeNewsApp(root)
    root.mainloop()


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                         Thanks for visiting keep supporting us...
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
