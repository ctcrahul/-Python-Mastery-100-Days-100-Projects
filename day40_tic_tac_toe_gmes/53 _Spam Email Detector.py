"""                                                 Day = 53
                           
                                   Spam Email Detector — Desktop App (Tkinter)
Features:
- Load CSV dataset with columns: 'text' and 'label' (spam/ham or 1/0)
- Train TF-IDF + MultinomialNB classifier, show evaluation metrics
- Predict single email text or classify a CSV file of emails
- Save/Load trained model (joblib)
- Export classification results to CSV
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import threading
import time
from datetime import datetime
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import joblib
import numpy as np

# -----------------------
# Helper ML functions
# -----------------------
def build_pipeline():
    # TF-IDF + MultinomialNB
    vect = TfidfVectorizer(
        lowercase=True,
        stop_words="english",  # use sklearn built-in stop words
        ngram_range=(1,2),
        max_df=0.95,
        min_df=2
    )
    clf = MultinomialNB()
    pipe = Pipeline([("tfidf", vect), ("nb", clf)])
    return pipe

def safe_load_dataset(path):
    df = pd.read_csv(path)
    # Attempt to find columns named like text / label
    text_col = None
    label_col = None
    for c in df.columns:
        if c.lower() in ("text", "message", "body", "email"):
            text_col = c
        if c.lower() in ("label","target","class"):
            label_col = c
    if text_col is None:
        # fallback to first column
        text_col = df.columns[0]
    if label_col is None:
        # fallback to second column if exists
        if len(df.columns) > 1:
            label_col = df.columns[1]
        else:
            raise ValueError("No label column found in CSV. Provide a label column (spam/ham or 1/0).")
    # Standardize labels to binary: spam=1 ham=0
    labels = df[label_col].astype(str).str.lower().map(lambda x: 1 if x in ("spam","1","true","t","yes") else 0)
    df = df[[text_col]].assign(label=labels)
    df = df.rename(columns={text_col: "text"})
    return df

# -----------------------
# Tkinter App
# -----------------------
class SpamDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Spam Email Detector")
        self.root.geometry("1000x700")
        self.model = None
        self.pipeline = build_pipeline()
        self.dataset = None
        self.history = []  # store session history for exports

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Spam Email Detector", font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Button(top, text="Load CSV Dataset", command=self.load_dataset).pack(side="right", padx=6)
        ttk.Button(top, text="Load Model", command=self.load_model).pack(side="right", padx=6)

        # Middle: controls and training
        mid = ttk.Frame(self.root, padding=10)
        mid.pack(fill="x")

        # Dataset info
        self.ds_info = tk.StringVar(value="No dataset loaded.")
        ttk.Label(mid, textvariable=self.ds_info).grid(row=0, column=0, columnspan=4, sticky="w")

        ttk.Label(mid, text="Test size (0-1)").grid(row=1, column=0, sticky="w", pady=6)
        self.test_size_var = tk.DoubleVar(value=0.2)
        ttk.Entry(mid, textvariable=self.test_size_var, width=8).grid(row=1, column=1, sticky="w")

        ttk.Label(mid, text="CV folds").grid(row=1, column=2, sticky="w")
        self.cv_var = tk.IntVar(value=5)
        ttk.Entry(mid, textvariable=self.cv_var, width=6).grid(row=1, column=3, sticky="w")

        ttk.Button(mid, text="Train Model", command=self.train_model).grid(row=2, column=0, pady=8)
        ttk.Button(mid, text="Save Model", command=self.save_model).grid(row=2, column=1, pady=8)
        ttk.Button(mid, text="Evaluate On Dataset", command=self.evaluate_on_dataset).grid(row=2, column=2, pady=8)
        ttk.Button(mid, text="Export Session History", command=self.export_history).grid(row=2, column=3, pady=8)

        # Visual: metrics and confusion matrix
        metrics_fr = ttk.LabelFrame(self.root, text="Evaluation Metrics", padding=10)
        metrics_fr.pack(fill="x", padx=10, pady=8)

        self.metrics_text = tk.Text(metrics_fr, height=6)
        self.metrics_text.pack(fill="x")

        cm_fr = ttk.LabelFrame(self.root, text="Confusion Matrix", padding=10)
        cm_fr.pack(fill="both", expand=False, padx=10, pady=8, ipadx=4, ipady=4)
        self.cm_container = ttk.Frame(cm_fr)
        self.cm_container.pack(fill="both", expand=True)

        # Lower: single prediction and batch prediction
        lower = ttk.Frame(self.root, padding=10)
        lower.pack(fill="both", expand=True)

        left = ttk.LabelFrame(lower, text="Single Email Test", padding=10)
        left.pack(side="left", fill="both", expand=True, padx=8, pady=6)

        ttk.Label(left, text="Enter email text below:").pack(anchor="w")
        self.single_text = tk.Text(left, height=10)
        self.single_text.pack(fill="both", expand=True, pady=6)
        ttk.Button(left, text="Predict", command=self.predict_single).pack(pady=6)
        self.single_result_var = tk.StringVar(value="No prediction yet.")
        ttk.Label(left, textvariable=self.single_result_var, font=("Segoe UI", 11, "bold")).pack()

        right = ttk.LabelFrame(lower, text="Batch: Classify CSV", padding=10)
        right.pack(side="right", fill="both", expand=True, padx=8, pady=6)

        ttk.Label(right, text="CSV should have a column with text (first or named 'text').").pack(anchor="w")
        ttk.Button(right, text="Classify CSV", command=self.classify_csv).pack(pady=6)
        ttk.Label(right, text="Last batch result:").pack(anchor="w", pady=(6,0))
        self.batch_result_var = tk.StringVar(value="No batch run yet.")
        ttk.Label(right, textvariable=self.batch_result_var).pack(anchor="w")

        # status bar
        self.status_var = tk.StringVar(value="Ready.")
        status = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status.pack(side="bottom", fill="x")

    # -----------------------
    # Actions
    # -----------------------
    def load_dataset(self):
        path = filedialog.askopenfilename(title="Select CSV dataset", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        try:
            df = safe_load_dataset(path)
            self.dataset = df
            self.ds_info.set(f"Loaded dataset: {os.path.basename(path)} — {len(df)} rows.")
            self.status_var.set("Dataset loaded.")
        except Exception as e:
            messagebox.showerror("Load failed", str(e))
            self.status_var.set("Failed to load dataset.")

    def train_model(self):
        if self.dataset is None:
            messagebox.showwarning("No data", "Load a dataset first.")
            return

        test_size = float(self.test_size_var.get())
        cv = int(self.cv_var.get())
        self.status_var.set("Training model...")
        def job():
            try:
                X = self.dataset["text"].fillna("").astype(str)
                y = self.dataset["label"].astype(int)
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)
                pipe = build_pipeline()
                pipe.fit(X_train, y_train)
                # cross val
                cv_scores = cross_val_score(pipe, X_train, y_train, cv=cv, scoring="f1", n_jobs=-1)
                # evaluate on holdout
                preds = pipe.predict(X_test)
                acc = accuracy_score(y_test, preds)
                prec = precision_score(y_test, preds, zero_division=0)
                rec = recall_score(y_test, preds, zero_division=0)
                f1 = f1_score(y_test, preds, zero_division=0)
                cm = confusion_matrix(y_test, preds)
                # set trained model
                self.model = pipe
                # save to history
                timestamp = datetime.utcnow().isoformat()
                self.history.append({"time":timestamp, "action":"train", "rows":len(self.dataset), "test_size":test_size,
                                     "cv_mean_f1": float(np.mean(cv_scores)), "acc": float(acc), "f1": float(f1)})
                # update UI
                self.root.after(0, lambda: self._update_after_train(acc, prec, rec, f1, cm, cv_scores))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Train failed", str(e)))
                self.root.after(0, lambda: self.status_var.set("Training failed."))
        threading.Thread(target=job, daemon=True).start()

    def _update_after_train(self, acc, prec, rec, f1, cm, cv_scores):
        self.metrics_text.delete("1.0", tk.END)
        s = f"Accuracy: {acc:.4f}\nPrecision: {prec:.4f}\nRecall: {rec:.4f}\nF1: {f1:.4f}\n"
        s += f"CV F1 scores: {np.array2string(cv_scores, precision=3, separator=', ')}\n"
        self.metrics_text.insert(tk.END, s)
        self.status_var.set("Model trained.")
        self._plot_confusion_matrix(cm)

    def _plot_confusion_matrix(self, cm):
        # clear
        for w in self.cm_container.winfo_children():
            w.destroy()
        fig = Figure(figsize=(4,3), dpi=100)
        ax = fig.add_subplot(111)
        im = ax.imshow(cm, interpolation="nearest", cmap=matplotlib.cm.Blues)
        ax.set_title("Confusion Matrix")
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        tick_marks = [0,1]
        ax.set_xticks(tick_marks)
        ax.set_yticks(tick_marks)
        ax.set_xticklabels(["ham","spam"])
        ax.set_yticklabels(["ham","spam"])

        thresh = cm.max() / 2.0 if cm.max() else 0
        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(j, i, format(cm[i, j], 'd'),
                        ha="center", va="center",
                        color="white" if cm[i, j] > thresh else "black")
        fig.colorbar(im, ax=ax)
        canvas = FigureCanvasTkAgg(fig, master=self.cm_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def evaluate_on_dataset(self):
        if self.dataset is None:
            messagebox.showwarning("No data", "Load a dataset first.")
            return
        if self.model is None:
            messagebox.showwarning("No model", "Train or load a model first.")
            return
        # evaluate across entire dataset
        X = self.dataset["text"].fillna("").astype(str)
        y = self.dataset["label"].astype(int)
        preds = self.model.predict(X)
        acc = accuracy_score(y, preds)
        prec = precision_score(y, preds, zero_division=0)
        rec = recall_score(y, preds, zero_division=0)
        f1 = f1_score(y, preds, zero_division=0)
        cm = confusion_matrix(y, preds)
        self.metrics_text.delete("1.0", tk.END)
        s = f"Full dataset evaluation\nAccuracy: {acc:.4f}\nPrecision: {prec:.4f}\nRecall: {rec:.4f}\nF1: {f1:.4f}\n\n"
        s += classification_report(y, preds, zero_division=0)
        self.metrics_text.insert(tk.END, s)
        self._plot_confusion_matrix(cm)
        self.status_var.set("Evaluation complete.")
        # history
        timestamp = datetime.utcnow().isoformat()
        self.history.append({"time":timestamp, "action":"evaluate_full", "rows":len(self.dataset), "acc":float(acc), "f1":float(f1)})

    def predict_single(self):
        text = self.single_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input", "Enter email text to classify.")
            return
        if self.model is None:
            messagebox.showwarning("No model", "Train or load a model first.")
            return
        pred = self.model.predict([text])[0]
        prob = None
        if hasattr(self.model, "predict_proba"):
            prob = self.model.predict_proba([text])[0].max()
        label = "SPAM" if int(pred)==1 else "HAM"
        self.single_result_var.set(f"{label}" + (f" (confidence {prob:.2f})" if prob is not None else ""))
        self.status_var.set("Single prediction done.")
        # history
        timestamp = datetime.utcnow().isoformat()
        self.history.append({"time":timestamp, "action":"predict_single", "pred":int(pred), "confidence": float(prob) if prob is not None else None})

    def classify_csv(self):
        path = filedialog.askopenfilename(title="Select CSV to classify", filetypes=[("CSV files","*.csv")])
        if not path:
            return
        if self.model is None:
            messagebox.showwarning("No model", "Train or load a model first.")
            return
        try:
            df = pd.read_csv(path)
            # guess text column
            text_col = None
            for c in df.columns:
                if c.lower() in ("text","message","body","email"):
                    text_col = c
                    break
            if text_col is None:
                text_col = df.columns[0]
            texts = df[text_col].fillna("").astype(str).tolist()
            preds = self.model.predict(texts)
            probs = None
            if hasattr(self.model, "predict_proba"):
                probs = self.model.predict_proba(texts).max(axis=1)
            df_out = df.copy()
            df_out["predicted_label"] = preds
            if probs is not None:
                df_out["confidence"] = probs
            # ask where to save
            out_path = filedialog.asksaveasfilename(title="Save classified CSV as", defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile=f"classified_{os.path.basename(path)}")
            if not out_path:
                self.status_var.set("Batch classification canceled (no save).")
                return
            df_out.to_csv(out_path, index=False)
            self.batch_result_var.set(f"Saved: {os.path.basename(out_path)} ({len(df_out)} rows)")
            self.status_var.set("Batch classification complete.")
            # add to history
            timestamp = datetime.utcnow().isoformat()
            self.history.append({"time":timestamp, "action":"batch_classify", "input":os.path.basename(path), "output":os.path.basename(out_path), "rows":len(df_out)})
            messagebox.showinfo("Done", f"Classified CSV saved to:\n{out_path}")
        except Exception as e:
            messagebox.showerror("Batch failed", str(e))
            self.status_var.set("Batch classification failed.")

    def save_model(self):
        if self.model is None:
            messagebox.showwarning("No model", "Train a model first.")
            return
        path = filedialog.asksaveasfilename(title="Save model", defaultextension=".joblib", filetypes=[("Joblib files","*.joblib")], initialfile=f"spam_model_{int(time.time())}.joblib")
        if not path:
            return
        joblib.dump(self.model, path)
        self.status_var.set(f"Model saved: {os.path.basename(path)}")
        self.history.append({"time":datetime.utcnow().isoformat(), "action":"save_model", "path":os.path.basename(path)})

    def load_model(self):
        path = filedialog.askopenfilename(title="Load model", filetypes=[("Joblib files","*.joblib")])
        if not path:
            return
        try:
            m = joblib.load(path)
            # basic sanity: must have predict
            if not hasattr(m, "predict"):
                raise ValueError("Selected file is not a valid sklearn model.")
            self.model = m
            self.status_var.set(f"Model loaded: {os.path.basename(path)}")
            self.history.append({"time":datetime.utcnow().isoformat(), "action":"load_model", "path":os.path.basename(path)})
        except Exception as e:
            messagebox.showerror("Load failed", str(e))

    def export_history(self):
        if not self.history:
            messagebox.showinfo("No history", "No actions to export during this session.")
            return
        path = filedialog.asksaveasfilename(title="Export session history", defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile=f"spam_session_history_{int(time.time())}.csv")
        if not path:
            return
        pd.DataFrame(self.history).to_csv(path, index=False)
        messagebox.showinfo("Saved", f"Session history exported:\n{path}")
        self.status_var.set("History exported.")

# -----------------------
# Run the app
# -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = SpamDetectorApp(root)
    root.mainloop()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                                                       Thanks
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

  def export_history(self):
        if not self.history:
            messagebox.showinfo("No history", "No actions to export during this session.")
            return
        path = filedialog.asksaveasfilename(title="Export session history", defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile=f"spam_session_history_{int(time.time())}.csv")
        if not path:
            return
        pd.DataFrame(self.history).to_csv(path, index=False)
        messagebox.showinfo("Saved", f"Session history exported:\n{path}")
        self.status_var.set("History exported.")

        try:
            m = joblib.load(path)
            # basic sanity: must have predict
            if not hasattr(m, "predict"):
                raise ValueError("Selected file is not a valid sklearn model.")
            self.model = m
            self.status_var.set(f"Model loaded: {os.path.basename(path)}")
            self.history.append({"time":datetime.utcnow().isoformat(), "action":"load_model", "path":os.path.basename(path)})
        except Exception as e:
            messagebox.showerror("Load failed", str(e))
          
