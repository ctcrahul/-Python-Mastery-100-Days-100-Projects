"""                                                    Day 51

                                                  Currency Conveter
Currency Converter Desktop App
- Live rates from exchangerate.host (no API key)
- Caches latest rates locally (cache.json)
- Shows conversion, history, CSV export, and a small historical plot
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import json
import os
import time
from datetime import datetime, timedelta
import threading
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_BASE = "https://api.exchangerate.host"
CACHE_FILE = "rates_cache.json"
SYMBOLS_FILE = "symbols_cache.json"
CACHE_TTL = 60 * 60  # 1 hour TTL for cached latest rates

def fetch_symbols():
    """Fetch currency symbols from the API (cached)."""
    if os.path.exists(SYMBOLS_FILE):
        try:
            with open(SYMBOLS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # if cached recently, return it
                if data.get("_cached_at") and time.time() - data["_cached_at"] < 24*3600:
                    return data["symbols"]
        except Exception:
            pass
    try:
        r = requests.get(f"{API_BASE}/symbols", timeout=10)
        r.raise_for_status()
        payload = r.json()
        symbols = payload.get("symbols", {})
        # store simplified mapping code->description
        sym_map = {k: v.get("description", k) for k, v in symbols.items()}
        with open(SYMBOLS_FILE, "w", encoding="utf-8") as f:
            json.dump({"_cached_at": time.time(), "symbols": sym_map}, f, ensure_ascii=False, indent=2)
        return sym_map
    except Exception:
        # fallback to small builtin list if internet unavailable
        fallback = {
            "USD": "United States Dollar", "EUR": "Euro", "INR": "Indian Rupee",
            "GBP": "British Pound", "JPY": "Japanese Yen", "AUD": "Australian Dollar",
            "CAD": "Canadian Dollar", "SGD": "Singapore Dollar", "CNY": "Chinese Yuan"
        }
        return fallback

def fetch_latest(base="USD"):
    """Fetch latest rates for a base currency. Uses cache and returns dict {rates, base, date}"""
    # check cache
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
            key = f"latest_{base}"
            if key in cache:
                entry = cache[key]
                if time.time() - entry.get("_fetched_at", 0) < CACHE_TTL:
                    return entry
        except Exception:
            cache = {}
    else:
        cache = {}

    # fetch fresh
    try:
        r = requests.get(f"{API_BASE}/latest", params={"base": base}, timeout=10)
        r.raise_for_status()
        payload = r.json()
        payload["_fetched_at"] = time.time()
        # save to cache
        cache[f"latest_{base}"] = payload
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
        return payload
    except Exception as e:
        # if fetch fails, try returning any cached base
        key = f"latest_{base}"
        if key in cache:
            return cache[key]
        # attempt to return first available cached entry
        if cache:
            return next(iter(cache.values()))
        raise RuntimeError("Unable to fetch latest rates and no cache available.") from e

def convert_amount(amount, from_currency, to_currency):
    """Use convert endpoint for most accurate result (handles amount)."""
    try:
        r = requests.get(f"{API_BASE}/convert", params={"from": from_currency, "to": to_currency, "amount": amount}, timeout=10)
        r.raise_for_status()
        payload = r.json()
        # payload contains 'result' and 'info' with rate
        return payload
    except Exception:
        # fallback to using latest rates if convert endpoint fails
        latest = fetch_latest(base=from_currency)
        rate = latest["rates"].get(to_currency)
        if rate is None:
            raise RuntimeError("Rate not available for pair.")
        return {"query": {"from": from_currency, "to": to_currency, "amount": amount},
                "info": {"rate": rate},
                "result": amount * rate}

def fetch_timeseries(base, target, start_date, end_date):
    """Get timeseries of rates between start and end (YYYY-MM-DD)."""
    try:
        r = requests.get(f"{API_BASE}/timeseries", params={
            "start_date": start_date,
            "end_date": end_date,
            "base": base,
            "symbols": target
        }, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        raise RuntimeError("Unable to fetch historical timeseries.") from e

# ------------------------
# Tkinter App
# ------------------------
class CurrencyConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter — Live & Offline-ready")
        self.root.geometry("920x640")
        self.root.resizable(False, False)

        self.symbols = fetch_symbols()
        self.currency_codes = sorted(self.symbols.keys())

        self.history = []  # history of conversions in session

        self._build_ui()
        # load default latest rates in background
        threading.Thread(target=self._warm_cache, daemon=True).start()

    def _build_ui(self):
        # header
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill="x")
        ttk.Label(header, text="Currency Converter", font=("Segoe UI", 20, "bold")).pack(side="left")
        ttk.Button(header, text="Refresh Symbols & Rates", command=self.refresh_all).pack(side="right")

        # main frame
        main = ttk.Frame(self.root, padding=12)
        main.pack(fill="both", expand=True)

        # input frame
        input_fr = ttk.LabelFrame(main, text="Convert", padding=10)
        input_fr.place(x=12, y=72, width=896, height=160)

        ttk.Label(input_fr, text="Amount").grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.amount_var = tk.StringVar(value="1.00")
        ttk.Entry(input_fr, textvariable=self.amount_var, width=18).grid(row=0, column=1, padx=8, pady=6, sticky="w")

        ttk.Label(input_fr, text="From").grid(row=1, column=0, padx=8, pady=6, sticky="w")
        self.from_var = tk.StringVar(value="USD")
        self.from_menu = ttk.Combobox(input_fr, textvariable=self.from_var, values=self.currency_codes, width=16, state="readonly")
        self.from_menu.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        ttk.Label(input_fr, text="To").grid(row=1, column=2, padx=8, pady=6, sticky="w")
        self.to_var = tk.StringVar(value="INR")
        self.to_menu = ttk.Combobox(input_fr, textvariable=self.to_var, values=self.currency_codes, width=16, state="readonly")
        self.to_menu.grid(row=1, column=3, padx=8, pady=6, sticky="w")

        ttk.Button(input_fr, text="Swap", command=self.swap_currencies).grid(row=1, column=4, padx=8, pady=6)
        ttk.Button(input_fr, text="Convert", command=self.do_convert).grid(row=0, column=4, padx=8, pady=6)

        # result area
        result_fr = ttk.Frame(main, padding=8)
        result_fr.place(x=12, y=240, width=896, height=110)
        ttk.Label(result_fr, text="Result:", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, sticky="w")
        self.result_var = tk.StringVar(value="")
        ttk.Label(result_fr, textvariable=self.result_var, font=("Segoe UI", 14)).grid(row=1, column=0, columnspan=4, sticky="w")

        # history and export
        hist_fr = ttk.LabelFrame(main, text="Session History", padding=8)
        hist_fr.place(x=12, y=360, width=560, height=260)
        cols = ("time","from","to","amount","rate","result")
        self.tree = ttk.Treeview(hist_fr, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=80 if c!="result" else 120, anchor="w")
        self.tree.pack(side="left", fill="both", expand=True)
        vsb = ttk.Scrollbar(hist_fr, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=vsb.set)
        vsb.pack(side="right", fill="y")

        ttk.Button(main, text="Export History (CSV)", command=self.export_history).place(x=380, y=610)

        # historical plot frame
        plot_fr = ttk.LabelFrame(main, text="Historical Rate Plot", padding=8)
        plot_fr.place(x=588, y=360, width=320, height=260)
        ttk.Label(plot_fr, text="From date (YYYY-MM-DD)").pack(anchor="w")
        self.start_entry = ttk.Entry(plot_fr)
        self.start_entry.pack(fill="x", pady=4)
        ttk.Label(plot_fr, text="To date (YYYY-MM-DD)").pack(anchor="w")
        self.end_entry = ttk.Entry(plot_fr)
        self.end_entry.pack(fill="x", pady=4)
        ttk.Button(plot_fr, text="Plot Timeseries", command=self.plot_timeseries).pack(pady=6)

        # placeholder for plot
        self.plot_container = ttk.Frame(plot_fr)
        self.plot_container.pack(fill="both", expand=True)

        # small footer with status
        self.status_var = tk.StringVar(value="Ready — rates from exchangerate.host (live when online).")
        status = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status.pack(side="bottom", fill="x")

    def _warm_cache(self):
        # prefetch latest for default base to make first convert fast
        try:
            fetch_latest(self.from_var.get())
        except Exception:
            pass  # ignore warm errors

    def refresh_all(self):
        """Refresh symbols and rates cache in background."""
        def job():
            self.status_var.set("Refreshing symbols and rates...")
            try:
                self.symbols = fetch_symbols()
                self.currency_codes = sorted(self.symbols.keys())
                self.from_menu["values"] = self.currency_codes
                self.to_menu["values"] = self.currency_codes
                fetch_latest(self.from_var.get())
                self.status_var.set("Refreshed symbols & rates.")
            except Exception as e:
                self.status_var.set("Refresh failed (offline?).")
                messagebox.showwarning("Refresh", f"Unable to refresh: {e}")
        threading.Thread(target=job, daemon=True).start()

    def swap_currencies(self):
        a = self.from_var.get()
        b = self.to_var.get()
        self.from_var.set(b)
        self.to_var.set(a)

    def do_convert(self):
        """Perform conversion using convert endpoint; update UI and history."""
        try:
            amount = float(self.amount_var.get())
        except Exception:
            messagebox.showerror("Input", "Enter a numeric amount.")
            return
        from_c = self.from_var.get()
        to_c = self.to_var.get()
        if not from_c or not to_c:
            messagebox.showerror("Input", "Select both currencies.")
            return

        self.status_var.set("Converting...")
        def job():
            try:
                payload = convert_amount(amount, from_c, to_c)
                result = payload.get("result")
                rate = None
                # prefer info.rate if present
                info = payload.get("info") or {}
                rate = info.get("rate") or (result/amount if amount else None)
                ts = datetime.utcnow().isoformat()
                self.history.insert(0, {"time":ts, "from":from_c, "to":to_c, "amount":amount, "rate":rate, "result":result})
                # update UI on main thread
                self.root.after(0, lambda: self._update_after_convert(rate, result))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Convert failed", str(e)))
                self.root.after(0, lambda: self.status_var.set("Convert failed."))
        threading.Thread(target=job, daemon=True).start()

    def _update_after_convert(self, rate, result):
        self.result_var.set(f"{result:,.4f} (rate: {rate:.6f})")
        self._refresh_history_view()
        self.status_var.set("Conversion complete.")

    def _refresh_history_view(self):
        self.tree.delete(*self.tree.get_children())
        for row in self.history:
            self.tree.insert("", "end", values=(row["time"].split("T")[0], row["from"], row["to"], row["amount"], f"{row['rate']:.6f}" if row['rate'] else "", f"{row['result']:.4f}"))

    def export_history(self):
        if not self.history:
            messagebox.showinfo("No data", "No conversions to export.")
            return
        df = pd.DataFrame(self.history)
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile="conversion_history.csv")
        if not path:
            return
        df.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"History exported to {path}")

    def plot_timeseries(self):
        base = self.from_var.get()
        target = self.to_var.get()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        if not (base and target and start and end):
            messagebox.showerror("Input", "Set base, target and both dates (YYYY-MM-DD).")
            return
        # basic date validation
        try:
            datetime.fromisoformat(start)
            datetime.fromisoformat(end)
        except Exception:
            messagebox.showerror("Input", "Dates must be YYYY-MM-DD.")
            return

        self.status_var.set("Fetching timeseries...")
        def job():
            try:
                payload = fetch_timeseries(base, target, start, end)
                rates = payload.get("rates", {})
                dates = sorted(rates.keys())
                series = [rates[d].get(target) for d in dates]
                # draw plot on main thread
                self.root.after(0, lambda: self._draw_plot(dates, series, base, target))
                self.root.after(0, lambda: self.status_var.set("Timeseries plotted."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Timeseries failed", str(e)))
                self.root.after(0, lambda: self.status_var.set("Timeseries failed."))
        threading.Thread(target=job, daemon=True).start()

    def _draw_plot(self, dates, series, base, target):
        # clear previous
        for w in self.plot_container.winfo_children():
            w.destroy()
        fig = Figure(figsize=(3.2,2.8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, series, marker="o")
        ax.set_title(f"{base}/{target} rate")
        ax.set_xlabel("Date")
        ax.set_ylabel("Rate")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

# ------------------------
# Run
# ------------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    app = CurrencyConverterApp(root)
    root.mainloop()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------------
# Run
# ------------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    style.theme_use("clam")
    app = CurrencyConverterApp(root)
    root.mainloop()

    def _draw_plot(self, dates, series, base, target):
        # clear previous
        for w in self.plot_container.winfo_children():
            w.destroy()
        fig = Figure(figsize=(3.2,2.8), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(dates, series, marker="o")
        ax.set_title(f"{base}/{target} rate")
        ax.set_xlabel("Date")
        ax.set_ylabel("Rate")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

              try:
            datetime.fromisoformat(start)
            datetime.fromisoformat(end)
        except Exception:
            messagebox.showerror("Input", "Dates must be YYYY-MM-DD.")
            return
          
        def job():
          
    def plot_timeseries(self):
        base = self.from_var.get()
        target = self.to_var.get()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        if not (base and target and start and end):
            messagebox.showerror("Input", "Set base, target and both dates (YYYY-MM-DD).")
            return
          
            try:
                payload = fetch_timeseries(base, target, start, end)
                rates = payload.get("rates", {})
                dates = sorted(rates.keys())
                series = [rates[d].get(target) for d in dates]
                # draw plot on main thread
                self.root.after(0, lambda: self._draw_plot(dates, series, base, target))
                self.root.after(0, lambda: self.status_var.set("Timeseries plotted."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Timeseries failed", str(e)))
                self.root.after(0, lambda: self.status_var.set("Timeseries failed."))
        threading.Thread(target=job, daemon=True).start()
      

    def export_history(self):
        if not self.history:
            messagebox.showinfo("No data", "No conversions to export.")
            return
        df = pd.DataFrame(self.history)
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile="conversion_history.csv")
        if not path:
              def _update_after_convert(self, rate, result):
        self.result_var.set(f"{result:,.4f} (rate: {rate:.6f})")
        self._refresh_history_view()
        self.status_var.set("Conversion complete.")
      
            return
        df.to_csv(path, index=False)
        messagebox.showinfo("Saved", f"History exported to {path}")
      
