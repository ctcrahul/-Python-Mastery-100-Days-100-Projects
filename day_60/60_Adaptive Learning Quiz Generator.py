"""                                                            Day = 60 
               
                                                     Adaptive Learning Quiz Generator 

Features:
- Tkinter GUI (quiz mode, practice mode, dashboard)
- Embedded sample question bank (can import CSV with columns: id,question,choices (| separated),answer (index),topic,explanation)
- Tracks user performance per question and per topic using SQLite (persistence)
- Adaptive algorithm: questions sampled with higher probability if user got them wrong recently or low mastery
- Spaced repetition-style scheduling: next_due timestamp, ease factor for each question
- Session stats, history, export progress to CSV
- Works offline; single Python file

Dependencies:
- Python 3.8+
- tkinter (bundled)
- sqlite3 (bundled)
- pandas (optional, only for export convenience) -> pip install pandas

Run:
    python adaptive_quiz.py
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import random
import time
from datetime import datetime, timedelta
import csv
import os
import threading
try:
    import pandas as pd
except Exception:
    pd = None

DB_FILE = "adaptive_quiz.db"

# ---------------------------
# Embedded sample question bank
# ---------------------------
SAMPLE_QUESTIONS = [
    # id, question, choices (| separated), correct_index (0-based), topic, explanation
    (1, "What is the output of 1 + '1' in Python 3?", "TypeError|'2'|11|'1 1'", 0, "Python", "In Python 3, adding int and str raises TypeError."),
    (2, "Which data structure uses LIFO?", "Queue|Stack|Heap|Graph", 1, "Data Structures", "Stack follows Last-In-First-Out ordering."),
    (3, "What's the time complexity of binary search on a sorted list?", "O(n)|O(log n)|O(n log n)|O(1)", 1, "Algorithms", "Binary search halves the search space each step: O(log n)."),
    (4, "Which HTML tag is used for the largest heading?", "<h1>|<h6>|<header>|<head>", 0, "Web", "<h1> is the largest heading tag."),
    (5, "What does SQL stand for?", "Structured Query Language|Simple Query Language|Sequential Query Language|Standard Query Language", 0, "Databases", "SQL stands for Structured Query Language."),
    (6, "Which method adds an element to the end of a Python list?", "append()|add()|push()|insert_end()", 0, "Python", "list.append(x) adds x to the end of the list."),
    (7, "In machine learning, what is overfitting?", "Model performs well on train and test|Model underperforms on all data|Model performs well on train but poorly on unseen data|Model uses too few features", 2, "ML", "Overfitting occurs when a model fits training data too closely and fails on new data."),
    (8, "HTTP status code 404 means:", "OK|Moved Permanently|Not Found|Internal Server Error", 2, "Web", "404 indicates the resource was not found."),
    (9, "Which sorting algorithm is stable?", "Quick Sort|Heap Sort|Merge Sort|Selection Sort", 2, "Algorithms", "Merge sort is stable while quicksort and heapsort typically aren't."),
    (10, "What symbol is used to denote comments in SQL?", "-- | # | // | /* */", 0, "Databases", "SQL uses -- for single-line comments."),
]

# ---------------------------
# Database & Persistence
# ---------------------------
class DBManager:
    def __init__(self, db_path=DB_FILE):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()
        self.lock = threading.Lock()
        # seed sample questions if empty
        if not self.get_any_question():
            self.seed_sample_questions()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY,
            question TEXT NOT NULL,
            choices TEXT NOT NULL,
            answer_index INTEGER NOT NULL,
            topic TEXT,
            explanation TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS stats (
            qid INTEGER PRIMARY KEY,
            attempts INTEGER DEFAULT 0,
            correct INTEGER DEFAULT 0,
            last_seen TIMESTAMP,
            next_due TIMESTAMP,
            ease REAL DEFAULT 2.5,   -- SM-2 like ease factor
            interval INTEGER DEFAULT 1,
            FOREIGN KEY(qid) REFERENCES questions(id)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            qid INTEGER,
            timestamp TIMESTAMP,
            correct INTEGER,
            response_time REAL,
            FOREIGN KEY(qid) REFERENCES questions(id)
        )
        """)
        self.conn.commit()

    def seed_sample_questions(self):
        cur = self.conn.cursor()
        for q in SAMPLE_QUESTIONS:
            qid, question, choices, ans, topic, explan = q
            cur.execute("INSERT OR IGNORE INTO questions (id,question,choices,answer_index,topic,explanation) VALUES (?,?,?,?,?,?)",
                        (qid, question, choices, ans, topic, explan))
            cur.execute("INSERT OR IGNORE INTO stats (qid, attempts, correct, last_seen, next_due, ease, interval) VALUES (?,?,?,?,?,?,?)",
                        (qid, 0, 0, None, None, 2.5, 1))
        self.conn.commit()

    def get_any_question(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM questions LIMIT 1")
        return cur.fetchone()

    def import_questions_from_csv(self, path):
        cur = self.conn.cursor()
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    qid = int(row.get("id") or 0)
                except:
                    qid = None
                question = row.get("question") or row.get("text") or ""
                choices = row.get("choices") or "|".join([row.get(f"choice{i}") or "" for i in range(1,6) if row.get(f"choice{i}")])
                if not choices:
                    # try to split by ; or |
                    choices = row.get("options") or ""
                ans_raw = row.get("answer") or row.get("answer_index") or "0"
                try:
                    ans = int(ans_raw)
                except:
                    # if answer is text, find index
                    ans = 0
                    parts = choices.split("|")
                    for i, c in enumerate(parts):
                        if c.strip().lower() == ans_raw.strip().lower():
                            ans = i
                            break
                topic = row.get("topic") or "General"
                explanation = row.get("explanation") or ""
                if qid:
                    cur.execute("INSERT OR REPLACE INTO questions (id,question,choices,answer_index,topic,explanation) VALUES (?,?,?,?,?,?)",
                                (qid, question, choices, ans, topic, explanation))
                    cur.execute("INSERT OR IGNORE INTO stats (qid, attempts, correct, last_seen, next_due, ease, interval) VALUES (?,?,?,?,?,?,?)",
                                (qid, 0, 0, None, None, 2.5, 1))
                else:
                    cur.execute("INSERT INTO questions (question,choices,answer_index,topic,explanation) VALUES (?,?,?,?,?)",
                                (question, choices, ans, topic, explanation))
                    new_id = cur.lastrowid
                    cur.execute("INSERT OR IGNORE INTO stats (qid, attempts, correct, last_seen, next_due, ease, interval) VALUES (?,?,?,?,?,?,?)",
                                (new_id, 0, 0, None, None, 2.5, 1))
        self.conn.commit()

    def list_topics(self):
        cur = self.conn.cursor()
        cur.execute("SELECT DISTINCT topic FROM questions")
        return [r[0] for r in cur.fetchall()]

    def get_question(self, qid):
        cur = self.conn.cursor()
        cur.execute("SELECT id,question,choices,answer_index,topic,explanation FROM questions WHERE id=?", (qid,))
        r = cur.fetchone()
        if not r:
            return None
        return {"id": r[0], "question": r[1], "choices": r[2].split("|"), "answer_index": int(r[3]), "topic": r[4], "explanation": r[5]}

    def get_all_question_ids(self):
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM questions")
        return [r[0] for r in cur.fetchall()]

    def get_due_questions(self, topics=None):
        """
        Return list of qids that are due (next_due is None or <= now) optionally filtered by topics
        """
        cur = self.conn.cursor()
        now_ts = datetime.utcnow().isoformat()
        if topics:
            placeholders = ",".join("?" for _ in topics)
            sql = f"""
            SELECT q.id FROM questions q
            LEFT JOIN stats s ON s.qid=q.id
            WHERE (s.next_due IS NULL OR s.next_due <= ?) AND q.topic IN ({placeholders})
            """
            cur.execute(sql, (now_ts, *topics))
        else:
            cur.execute("SELECT q.id FROM questions q LEFT JOIN stats s ON s.qid=q.id WHERE (s.next_due IS NULL OR s.next_due <= ?)", (now_ts,))
        return [r[0] for r in cur.fetchall()]

    def get_stats(self, qid):
        cur = self.conn.cursor()
        cur.execute("SELECT attempts, correct, last_seen, next_due, ease, interval FROM stats WHERE qid=?", (qid,))
        r = cur.fetchone()
        if not r:
            return {"attempts": 0, "correct": 0, "last_seen": None, "next_due": None, "ease":2.5, "interval":1}
        return {"attempts": r[0], "correct": r[1], "last_seen": r[2], "next_due": r[3], "ease": r[4], "interval": r[5]}

    def record_result(self, qid, correct, response_time):
        """
        Update stats using a simplified SM-2 algorithm for spaced repetition.
        """
        with self.lock:
            cur = self.conn.cursor()
            st = self.get_stats(qid)
            attempts = st["attempts"] + 1
            corrects = st["correct"] + (1 if correct else 0)
            last_seen = datetime.utcnow().isoformat()

            # SM-2 simplified:
            ease = st["ease"]
            interval = st["interval"]
            if correct:
                # increase ease slightly
                ease = min(4.0, ease + 0.15)
                if interval == 1:
                    interval = 1
                # increase interval multiplicatively
                interval = max(1, int(round(interval * ease)))
                next_due_dt = datetime.utcnow() + timedelta(days=interval)
            else:
                # penalize ease
                ease = max(1.3, ease - 0.2)
                interval = 1
                next_due_dt = datetime.utcnow() + timedelta(days=1)  # retry tomorrow

            next_due = next_due_dt.isoformat()
            cur.execute("INSERT OR REPLACE INTO stats (qid, attempts, correct, last_seen, next_due, ease, interval) VALUES (?,?,?,?,?,?,?)",
                        (qid, attempts, corrects, last_seen, next_due, ease, interval))
            cur.execute("INSERT INTO history (qid,timestamp,correct,response_time) VALUES (?,?,?,?)",
                        (qid, last_seen, 1 if correct else 0, float(response_time)))
            self.conn.commit()

    def get_topic_mastery(self):
        """
        Return dict {topic: (attempts, correct, accuracy)}
        """
        cur = self.conn.cursor()
        cur.execute("""
        SELECT q.topic, SUM(s.attempts), SUM(s.correct)
        FROM questions q
        LEFT JOIN stats s ON s.qid=q.id
        GROUP BY q.topic
        """)
        result = {}
        for topic, attempts, correct in cur.fetchall():
            attempts = attempts or 0
            correct = correct or 0
            accuracy = (correct / attempts) if attempts else None
            result[topic] = {"attempts": attempts, "correct": correct, "accuracy": accuracy}
        return result

    def export_progress_csv(self, path):
        cur = self.conn.cursor()
        cur.execute("""
        SELECT q.id, q.topic, q.question, s.attempts, s.correct, s.last_seen, s.next_due, s.ease, s.interval
        FROM questions q LEFT JOIN stats s ON s.qid=q.id
        """)
        rows = cur.fetchall()
        header = ["id","topic","question","attempts","correct","last_seen","next_due","ease","interval"]
        with open(path, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            for r in rows:
                writer.writerow(r)

    def close(self):
        self.conn.close()

# ---------------------------
# Quiz Engine (Adaptive Sampling)
# ---------------------------
class QuizEngine:
    def __init__(self, db: DBManager):
        self.db = db

    def sample_questions(self, n=10, topics=None, mode="adaptive"):
        """
        modes:
         - "adaptive": weighted sampling prioritizing low accuracy and due items
         - "random": purely random
         - "weakness": focus on items with lowest correctness ratio
        """
        all_ids = self.db.get_all_question_ids()
        if not all_ids:
            return []

        # optionally restrict by topics
        if topics:
            cur = self.db.conn.cursor()
            placeholders = ",".join("?" for _ in topics)
            cur.execute(f"SELECT id FROM questions WHERE topic IN ({placeholders})", topics)
            ids = [r[0] for r in cur.fetchall()]
            if not ids:
                return []
        else:
            ids = all_ids

        # compute weights
        weights = []
        for qid in ids:
            st = self.db.get_stats(qid)
            attempts = st["attempts"] or 0
            correct = st["correct"] or 0
            accuracy = (correct / attempts) if attempts else None

            # base weight: due questions are higher priority
            next_due = st["next_due"]
            due_priority = 1.0
            if not next_due:
                due_priority = 1.2
            else:
                # if overdue (<= now)
                try:
                    ndt = datetime.fromisoformat(next_due)
                    if ndt <= datetime.utcnow():
                        due_priority = 2.0
                    else:
                        # upcoming due -> moderate
                        due_priority = 1.0
                except:
                    due_priority = 1.0

            # low accuracy -> higher weight
            if accuracy is None:
                acc_weight = 1.5  # never seen
            else:
                acc_weight = 1.0 + (1.0 - accuracy) * 3.0  # ranges 1 to 4

            # recency penalty: recently seen -> slightly lower weight
            recency_penalty = 1.0
            if st["last_seen"]:
                try:
                    last = datetime.fromisoformat(st["last_seen"])
                    delta = (datetime.utcnow() - last).total_seconds()
                    if delta < 3600:  # seen within last hour
                        recency_penalty = 0.6
                    elif delta < 86400:  # within day
                        recency_penalty = 0.9
                except:
                    recency_penalty = 1.0

            # final weight
            w = due_priority * acc_weight * recency_penalty
            weights.append(max(0.01, w))

        # sample without replacement using weights
        choices = []
        available = ids.copy()
        avail_weights = weights.copy()

        n = min(n, len(available))
        for _ in range(n):
            total = sum(avail_weights)
            if total <= 0:
                break
            pick = random.uniform(0, total)
            cum = 0
            for i, w in enumerate(avail_weights):
                cum += w
                if pick <= cum:
                    choices.append(available.pop(i))
                    avail_weights.pop(i)
                    break
        return choices

# ---------------------------
# GUI
# ---------------------------
class AdaptiveQuizGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Adaptive Learning Quiz Generator")
        self.root.geometry("980x680")

        self.db = DBManager()
        self.engine = QuizEngine(self.db)
        self.session_questions = []
        self.current_index = 0
        self.session_start_time = None
        self.question_start_time = None

        self.build_ui()
        self.refresh_topic_list()
        self.update_dashboard()

    def build_ui(self):
        # Top controls
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill="x")

        ttk.Button(top, text="New Adaptive Quiz", command=self.start_adaptive_quiz).pack(side="left", padx=6)
        ttk.Button(top, text="New Random Quiz", command=self.start_random_quiz).pack(side="left", padx=6)
        ttk.Button(top, text="Practice Weak Topics", command=self.start_weakness_quiz).pack(side="left", padx=6)
        ttk.Button(top, text="Import Questions (CSV)", command=self.import_csv).pack(side="left", padx=6)
        ttk.Button(top, text="Export Progress (CSV)", command=self.export_progress).pack(side="left", padx=6)
        ttk.Button(top, text="Reset Stats", command=self.reset_stats_prompt).pack(side="left", padx=6)

        # Left: topics and dashboard
        left = ttk.Frame(self.root)
        left.pack(side="left", fill="y", padx=8, pady=8)

        ttk.Label(left, text="Filter by Topics (multi-select):").pack(anchor="w")
        self.topic_listbox = tk.Listbox(left, selectmode="multiple", height=10, exportselection=False)
        self.topic_listbox.pack(fill="y", expand=False)
        ttk.Button(left, text="Refresh Topics", command=self.refresh_topic_list).pack(pady=6)

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(left, text="Session Controls:").pack(anchor="w", pady=(6,0))
        ttk.Label(left, text="Questions per quiz:").pack(anchor="w")
        self.num_q_var = tk.IntVar(value=10)
        ttk.Entry(left, textvariable=self.num_q_var, width=6).pack(anchor="w")

        ttk.Button(left, text="Show Dashboard", command=self.update_dashboard).pack(pady=6)

        # Center: quiz area
        center = ttk.Frame(self.root)
        center.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        # Question display
        self.q_text = tk.Text(center, height=6, wrap="word", font=("Segoe UI", 12))
        self.q_text.pack(fill="x", pady=(0,6))
        self.choices_vars = []
        self.choice_buttons = []
        for i in range(6):
            v = tk.StringVar(value="")
            btn = ttk.Radiobutton(center, textvariable=v, value=i, command=lambda idx=i: self.on_choice_selected(idx))
            btn.pack(anchor="w", pady=2)
            self.choices_vars.append(v)
            self.choice_buttons.append(btn)

        # Navigation and info
        nav = ttk.Frame(center)
        nav.pack(fill="x", pady=6)
        self.next_btn = ttk.Button(nav, text="Next", command=self.next_question, state="disabled")
        self.next_btn.pack(side="right", padx=6)
        self.show_expl_btn = ttk.Button(nav, text="Show Explanation", command=self.show_explanation, state="disabled")
        self.show_expl_btn.pack(side="right", padx=6)

        self.progress_var = tk.StringVar(value="No session.")
        ttk.Label(center, textvariable=self.progress_var).pack(anchor="w")

        # Right: dashboard graphs/stats and history
        right = ttk.Frame(self.root)
        right.pack(side="right", fill="y", padx=8, pady=8)

        ttk.Label(right, text="Topic Mastery:").pack(anchor="w")
        self.mastery_box = tk.Listbox(right, width=40, height=14)
        self.mastery_box.pack(fill="y")

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=6)
        ttk.Label(right, text="Recent History:").pack(anchor="w")
        self.history_box = tk.Listbox(right, width=40, height=10)
        self.history_box.pack(fill="y")
        ttk.Button(right, text="Refresh Dashboard", command=self.update_dashboard).pack(pady=6)

    # ---------------------------
    # Topic / import / export
    # ---------------------------
    def refresh_topic_list(self):
        topics = self.db.list_topics()
        self.topic_listbox.delete(0, tk.END)
        for t in topics:
            self.topic_listbox.insert(tk.END, t)

    def import_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files","*.csv")])
        if not path:
            return
        try:
            self.db.import_questions_from_csv(path)
            messagebox.showinfo("Import", "Imported questions. Refreshing topics.")
            self.refresh_topic_list()
            self.update_dashboard()
        except Exception as e:
            messagebox.showerror("Import failed", str(e))

    def export_progress(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile="progress.csv")
        if not path:
            return
        try:
            self.db.export_progress_csv(path)
            messagebox.showinfo("Export", f"Progress exported to {path}")
        except Exception as e:
            messagebox.showerror("Export failed", str(e))

    def reset_stats_prompt(self):
        if messagebox.askyesno("Reset", "Reset all stats and history? This cannot be undone."):
            cur = self.db.conn.cursor()
            cur.execute("DELETE FROM stats")
            cur.execute("DELETE FROM history")
            # reinitialize stats rows for existing questions
            qids = self.db.get_all_question_ids()
            for qid in qids:
                cur.execute("INSERT OR IGNORE INTO stats (qid, attempts, correct, last_seen, next_due, ease, interval) VALUES (?,?,?,?,?,?,?)",
                            (qid, 0, 0, None, None, 2.5, 1))
            self.db.conn.commit()
            messagebox.showinfo("Reset", "Stats cleared.")
            self.update_dashboard()

    # ---------------------------
    # Starting sessions
    # ---------------------------
    def _selected_topics(self):
        sel = self.topic_listbox.curselection()
        if not sel:
            return None
        topics = [self.topic_listbox.get(i) for i in sel]
        return topics

    def start_adaptive_quiz(self):
        topics = self._selected_topics()
        n = max(1, int(self.num_q_var.get()))
        self.session_questions = self.engine.sample_questions(n=n, topics=topics, mode="adaptive")
        if not self.session_questions:
            messagebox.showinfo("No questions", "No questions available for the chosen topics / due criteria.")
            return
        self.current_index = 0
        self.session_start_time = time.time()
        self.load_question(0)

    def start_random_quiz(self):
        topics = self._selected_topics()
        n = max(1, int(self.num_q_var.get()))
        all_ids = self.db.get_all_question_ids()
        if topics:
            # restrict
            cur = self.db.conn.cursor()
            placeholders = ",".join("?" for _ in topics)
            cur.execute(f"SELECT id FROM questions WHERE topic IN ({placeholders})", topics)
            candidates = [r[0] for r in cur.fetchall()]
        else:
            candidates = all_ids
        if not candidates:
            messagebox.showinfo("No questions", "No questions in selected topics.")
            return
        self.session_questions = random.sample(candidates, min(n, len(candidates)))
        self.current_index = 0
        self.session_start_time = time.time()
        self.load_question(0)

    def start_weakness_quiz(self):
        topics = self._selected_topics()
        n = max(1, int(self.num_q_var.get()))
        # score by accuracy ascending
        all_ids = self.db.get_all_question_ids()
        scored = []
        for qid in all_ids:
            st = self.db.get_stats(qid)
            attempts = st["attempts"] or 0
            correct = st["correct"] or 0
            acc = (correct/attempts) if attempts else 0.0
            if topics:
                q = self.db.get_question(qid)
                if q["topic"] not in topics:
                    continue
            scored.append((acc, qid))
        scored.sort(key=lambda x: x[0])
        self.session_questions = [qid for _, qid in scored[:n]]
        if not self.session_questions:
            messagebox.showinfo("No questions", "No questions selected.")
            return
        self.current_index = 0
        self.session_start_time = time.time()
        self.load_question(0)

    # ---------------------------
    # Question flow
    # ---------------------------
    def load_question(self, idx):
        if idx < 0 or idx >= len(self.session_questions):
            return
        qid = self.session_questions[idx]
        q = self.db.get_question(qid)
        if not q:
            return
        self.current_qid = qid
        self.q_text.delete("1.0", tk.END)
        self.q_text.insert(tk.END, f"Q{idx+1}. {q['question']}\n\nTopic: {q['topic']}")
        # populate choices; enable only used choices
        for i, v in enumerate(self.choices_vars):
            if i < len(q["choices"]):
                v.set(q["choices"][i])
                self.choice_buttons[i].configure(state="normal")
                self.choice_buttons[i].deselect()
                self.choice_buttons[i].pack(anchor="w", pady=2)
            else:
                v.set("")
                self.choice_buttons[i].configure(state="disabled")
                self.choice_buttons[i].pack_forget()
        self.selected_choice = None
        self.next_btn.configure(state="disabled")
        self.show_expl_btn.configure(state="disabled")
        self.progress_var.set(f"Question {idx+1} / {len(self.session_questions)}")
        self.question_start_time = time.time()

    def on_choice_selected(self, idx):
        self.selected_choice = idx
        # enable next
        self.next_btn.configure(state="normal")

    def next_question(self):
        if self.selected_choice is None:
            messagebox.showwarning("Select", "Choose an option first.")
            return
        qid = self.current_qid
        q = self.db.get_question(qid)
        correct_idx = q["answer_index"]
        correct = (self.selected_choice == correct_idx)
        response_time = time.time() - self.question_start_time if self.question_start_time else 0.0
        # record result
        self.db.record_result(qid, correct, response_time)
        # show feedback
        if correct:
            messagebox.showinfo("Correct", "Good job! That's correct.")
        else:
            messagebox.showinfo("Incorrect", f"Incorrect. Correct answer: {q['choices'][correct_idx]}")
        # enable explanation
        self.show_expl_btn.configure(state="normal")
        # move next
        self.current_index += 1
        if self.current_index >= len(self.session_questions):
            self.end_session()
        else:
            self.load_question(self.current_index)
            # auto-update dashboard stats on background
            self.update_dashboard()

    def show_explanation(self):
        q = self.db.get_question(self.current_qid)
        explanation = q.get("explanation") or "No explanation provided."
        messagebox.showinfo("Explanation", explanation)

    def end_session(self):
        duration = time.time() - self.session_start_time if self.session_start_time else 0.0
        correct_count = 0
        for qid in self.session_questions:
            st = self.db.get_stats(qid)
            correct_count += st["correct"]  # this counts cumulative corrects; rough
        messagebox.showinfo("Session complete", f"Session finished. Time: {int(duration)}s\nQuestions: {len(self.session_questions)}")
        self.session_questions = []
        self.current_index = 0
        self.progress_var.set("No active session.")
        self.update_dashboard()

    # ---------------------------
    # Dashboard / history
    # ---------------------------
    def update_dashboard(self):
        # topic mastery
        mastery = self.db.get_topic_mastery()
        self.mastery_box.delete(0, tk.END)
        for topic, data in mastery.items():
            acc = data["accuracy"]
            acc_str = f"{acc*100:.1f}%" if acc is not None else "N/A"
            self.mastery_box.insert(tk.END, f"{topic}: attempts={data['attempts']} correct={data['correct']} accuracy={acc_str}")

        # recent history (last 20)
        cur = self.db.conn.cursor()
        cur.execute("SELECT h.timestamp, q.question, h.correct FROM history h JOIN questions q ON q.id=h.qid ORDER BY h.timestamp DESC LIMIT 20")
        rows = cur.fetchall()
        self.history_box.delete(0, tk.END)
        for t, qtext, correct in rows:
            tstr = t.split("T")[0] if "T" in t else str(t)
            self.history_box.insert(tk.END, f"{tstr} | {'✓' if correct else '✗'} | {qtext[:60].strip()}")

    # ---------------------------
    # Cleanup
    # ---------------------------
    def close(self):
        self.db.close()

# ---------------------------
# Run App
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except:
        pass
    app = AdaptiveQuizGUI(root)
    def on_close():
        if messagebox.askyesno("Exit", "Exit the Adaptive Quiz app?"):
            app.close()
            root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()



#===========================================================================================================================================================================
                                                            Thanks For visting and keep supporting us.
#===========================================================================================================================================================================

