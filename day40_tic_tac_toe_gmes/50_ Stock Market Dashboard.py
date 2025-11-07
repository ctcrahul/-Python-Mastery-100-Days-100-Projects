"""
                                                                  Day = 50

                                                             Stock Market Dashboard
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
from datetime import datetime, date
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import os

DB_PATH = "finance.db"

# ---------------------------
# Database helper
# ---------------------------
class DB:
    def __init__(self, path=DB_PATH):
        self.conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self._create_tables()

    def _create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_date DATE NOT NULL,
            tx_type TEXT CHECK(tx_type IN ('income','expense')) NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            notes TEXT
        )""")
        cur.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month TEXT NOT NULL,  -- format YYYY-MM
            category TEXT NOT NULL,
            limit_amount REAL NOT NULL,
            UNIQUE(month, category)
        )""")
        self.conn.commit()

    def add_transaction(self, tx_date, tx_type, amount, category, notes):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO transactions (tx_date, tx_type, amount, category, notes) VALUES (?, ?, ?, ?, ?)",
                    (tx_date, tx_type, amount, category, notes))
        self.conn.commit()

    def query_transactions(self, start=None, end=None):
        cur = self.conn.cursor()
        sql = "SELECT id, tx_date, tx_type, amount, category, notes FROM transactions WHERE 1=1 "
        params = []
        if start:
            sql += "AND date(tx_date) >= date(?) "
            params.append(start)
        if end:
            sql += "AND date(tx_date) <= date(?) "
            params.append(end)
        sql += "ORDER BY tx_date DESC, id DESC"
        cur.execute(sql, params)
        rows = cur.fetchall()
        return rows

    def monthly_summary(self, year_month):
        # year_month like "2025-11"
        cur = self.conn.cursor()
        start = f"{year_month}-01"
        # compute month end by simple trick: next month 1 minus one day
        y, m = map(int, year_month.split("-"))
        if m == 12:
            next_month = f"{y+1}-01-01"
        else:
            next_month = f"{y}-{m+1:02d}-01"
        cur.execute("""
            SELECT tx_type, SUM(amount) FROM transactions
            WHERE date(tx_date) >= date(?) AND date(tx_date) < date(?)
            GROUP BY tx_type
        """, (start, next_month))
        data = dict(cur.fetchall())
        income = data.get('income', 0.0) or 0.0
        expense = data.get('expense', 0.0) or 0.0
        return float(income), float(expense)

    def category_breakdown(self, year_month):
        y, m = map(int, year_month.split("-"))
        start = f"{year_month}-01"
        if m == 12:
            next_month = f"{y+1}-01-01"
        else:
            next_month = f"{y}-{m+1:02d}-01"
        cur = self.conn.cursor()
        cur.execute("""
            SELECT category, SUM(amount) FROM transactions
            WHERE tx_type='expense' AND date(tx_date) >= date(?) AND date(tx_date) < date(?)
            GROUP BY category ORDER BY SUM(amount) DESC
        """, (start, next_month))
        return cur.fetchall()

    def monthly_totals_over_time(self, months_back=6):
        # returns list of (YYYY-MM, income, expense)
        cur = self.conn.cursor()
        data = []
        today = date.today()
        for i in range(months_back-1, -1, -1):
            year = today.year
            month = today.month - i
            while month <= 0:
                month += 12
                year -= 1
            ym = f"{year}-{month:02d}"
            inc, exp = self.monthly_summary(ym)
            data.append((ym, inc, exp))
        return data

    def set_budget(self, month, category, limit_amount):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO budgets (month, category, limit_amount) VALUES (?, ?, ?)
            ON CONFLICT(month, category) DO UPDATE SET limit_amount=excluded.limit_amount
        """, (month, category, limit_amount))
        self.conn.commit()

    def get_budgets(self, month):
        cur = self.conn.cursor()
        cur.execute("SELECT category, limit_amount FROM budgets WHERE month = ?", (month,))
        return dict(cur.fetchall())

    def close(self):
        self.conn.close()

# ---------------------------
# App UI
# ---------------------------
class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Dashboard")
        self.root.geometry("1050x650")
        self.db = DB()
        self._build_ui()
        self.refresh_transactions()

    def _build_ui(self):
        # Top frame: Add transaction
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Date (YYYY-MM-DD)").grid(row=0, column=0, padx=6, pady=6)
        self.date_var = tk.StringVar(value=str(date.today()))
        ttk.Entry(top, textvariable=self.date_var, width=14).grid(row=0, column=1, padx=6)

        ttk.Label(top, text="Type").grid(row=0, column=2, padx=6)
        self.type_var = tk.StringVar(value="expense")
        ttk.Combobox(top, textvariable=self.type_var, values=["expense", "income"], width=10, state="readonly").grid(row=0, column=3, padx=6)

        ttk.Label(top, text="Amount").grid(row=0, column=4, padx=6)
        self.amount_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.amount_var, width=12).grid(row=0, column=5, padx=6)

        ttk.Label(top, text="Category").grid(row=0, column=6, padx=6)
        self.category_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.category_var, width=16).grid(row=0, column=7, padx=6)

        ttk.Label(top, text="Notes").grid(row=0, column=8, padx=6)
        self.notes_var = tk.StringVar()
        ttk.Entry(top, textvariable=self.notes_var, width=20).grid(row=0, column=9, padx=6)

        ttk.Button(top, text="Add Transaction", command=self.add_transaction).grid(row=0, column=10, padx=8)

        # Middle: transactions table and summary
        mid = ttk.Frame(self.root, padding=10)
        mid.pack(fill="both", expand=True)

        # Left: table
        left = ttk.Frame(mid)
        left.pack(side="left", fill="both", expand=True)

        cols = ("id", "date", "type", "amount", "category", "notes")
        self.tree = ttk.Treeview(left, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            self.tree.heading(c, text=c.title())
            w = 80 if c in ("id","type") else 140
            if c == "notes": w = 220
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, side="left")
        scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Right: summary + charts
        right = ttk.Frame(mid, width=420)
        right.pack(side="right", fill="y")

        # Summary labels
        self.summary_label = ttk.Label(right, text="", font=("Segoe UI", 11, "bold"))
        self.summary_label.pack(pady=8)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=6)

        # Chart area
        self.chart_container = ttk.Frame(right)
        self.chart_container.pack(fill="both", expand=True)

        # Bottom: controls
        bottom = ttk.Frame(self.root, padding=10)
        bottom.pack(fill="x")

        ttk.Button(bottom, text="Refresh", command=self.refresh_transactions).pack(side="left", padx=6)
        ttk.Button(bottom, text="Export CSV", command=self.export_csv).pack(side="left", padx=6)
        ttk.Button(bottom, text="Set Budget for Month", command=self.open_budget_dialog).pack(side="left", padx=6)
        ttk.Button(bottom, text="Show Charts", command=self.show_charts).pack(side="left", padx=6)

    def add_transaction(self):
        tx_date = self.date_var.get().strip()
        try:
            # validate date
            datetime.fromisoformat(tx_date)
        except Exception:
            messagebox.showerror("Invalid date", "Please provide date as YYYY-MM-DD")
            return
        tx_type = self.type_var.get()
        try:
            amount = float(self.amount_var.get())
        except Exception:
            messagebox.showerror("Invalid amount", "Please provide a numeric amount.")
            return
        category = self.category_var.get().strip() or ("Income" if tx_type=="income" else "General")
        notes = self.notes_var.get().strip()
        self.db.add_transaction(tx_date, tx_type, abs(amount), category, notes)
        messagebox.showinfo("Saved", "Transaction added.")
        # clear amount/notes
        self.amount_var.set("")
        self.notes_var.set("")
        self.refresh_transactions()

    def refresh_transactions(self):
        rows = self.db.query_transactions()
        self.tree.delete(*self.tree.get_children())
        total_income = 0.0
        total_expense = 0.0
        for r in rows:
            self.tree.insert("", "end", values=r)
            if r[2] == "income":
                total_income += float(r[3])
            else:
                total_expense += float(r[3])
        balance = total_income - total_expense
        self.summary_label.config(text=f"Total Income: ₹{total_income:.2f}\nTotal Expense: ₹{total_expense:.2f}\nBalance: ₹{balance:.2f}")
        # show default charts
        self.show_charts()

    def export_csv(self):
        rows = self.db.query_transactions()
        if not rows:
            messagebox.showinfo("No data", "No transactions to export.")
            return
        df = pd.DataFrame(rows, columns=["id", "date", "type", "amount", "category", "notes"])
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile="transactions.csv")
        if not path:
            return
        df.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"Transactions exported to:\n{path}")

    def show_charts(self):
        # clear container
        for w in self.chart_container.winfo_children():
            w.destroy()

        # Pie chart: category breakdown for current month
        ym = f"{date.today().year}-{date.today().month:02d}"
        breakdown = self.db.category_breakdown(ym)
        cats = [b[0] for b in breakdown]
        vals = [b[1] for b in breakdown]
        fig = Figure(figsize=(4.2,3), dpi=100)
        ax = fig.add_subplot(111)
        if vals and sum(vals) > 0:
            ax.pie(vals, labels=cats, autopct="%1.1f%%", startangle=140)
            ax.set_title("This month's expenses by category")
        else:
            ax.text(0.5, 0.5, "No expense data this month", ha="center", va="center")
            ax.axis("off")

        canvas = FigureCanvasTkAgg(fig, master=self.chart_container)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, pady=6)

        # Line chart: last 6 months income vs expense
        trend = self.db.monthly_totals_over_time(6)
        months = [t[0] for t in trend]
        incomes = [t[1] for t in trend]
        expenses = [t[2] for t in trend]
        fig2 = Figure(figsize=(4.2,2.6), dpi=100)
        ax2 = fig2.add_subplot(111)
        ax2.plot(months, incomes, marker="o", label="Income")
        ax2.plot(months, expenses, marker="o", label="Expense")
        ax2.set_title("Last 6 months")
        ax2.legend()
        ax2.grid(True, linestyle="--", alpha=0.4)
        canvas2 = FigureCanvasTkAgg(fig2, master=self.chart_container)
        canvas2.draw()
        canvas2.get_tk_widget().pack(side="top", fill="both", expand=True, pady=6)

        # Check budgets and show simple warnings if exceeded or near limit
        budgets = self.db.get_budgets(ym)
        warn_text = ""
        if budgets:
            for cat, limit in budgets.items():
                spent = next((v for c,v in breakdown if c==cat), 0.0)
                if spent >= limit:
                    warn_text += f"Budget exceeded for {cat}: ₹{spent:.2f} / ₹{limit:.2f}\n"
                elif spent >= 0.8 * limit:
                    warn_text += f"Approaching budget for {cat}: ₹{spent:.2f} / ₹{limit:.2f}\n"
        if warn_text:
            lbl = ttk.Label(self.chart_container, text=warn_text, foreground="red", justify="left")
            lbl.pack(side="top", pady=6)

    def open_budget_dialog(self):
        # small dialog to set budgets for current month
        month = f"{date.today().year}-{date.today().month:02d}"
        dlg = tk.Toplevel(self.root)
        dlg.title("Set Budgets for " + month)
        ttk.Label(dlg, text="Category").grid(row=0, column=0, padx=6, pady=6)
        cat_var = tk.StringVar()
        ttk.Entry(dlg, textvariable=cat_var, width=20).grid(row=0, column=1, padx=6)

        ttk.Label(dlg, text="Limit (₹)").grid(row=1, column=0, padx=6, pady=6)
        limit_var = tk.StringVar()
        ttk.Entry(dlg, textvariable=limit_var, width=12).grid(row=1, column=1, padx=6)

        def save_budget():
            try:
                limit_amount = float(limit_var.get())
            except Exception:
                messagebox.showerror("Invalid", "Please enter numeric limit.")
                return
            category = cat_var.get().strip()
            if not category:
                messagebox.showerror("Invalid", "Provide category name.")
                return
            self.db.set_budget(month, category, limit_amount)
            messagebox.showinfo("Saved", f"Budget set: {category} → ₹{limit_amount:.2f} for {month}")
            dlg.destroy()
            self.show_charts()

        ttk.Button(dlg, text="Save", command=save_budget).grid(row=2, column=0, columnspan=2, pady=10)

    def close(self):
        self.db.close()
        self.root.destroy()

# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    root = tk.Tk()
    style = ttk.Style(root)
    # use default theme for cross-platform consistency; you can change it to 'clam' or others
    style.theme_use('default')
    app = FinanceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
  

#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
                                                 Thanks for visting and keep supporting us....
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------#


if __name__ == "__main__":
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    root = tk.Tk()
    style = ttk.Style(root)
    # use default theme for cross-platform consistency; you can change it to 'clam' or others
    style.theme_use('default')
    app = FinanceApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
