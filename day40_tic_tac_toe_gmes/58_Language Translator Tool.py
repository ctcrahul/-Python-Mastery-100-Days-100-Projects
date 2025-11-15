"""                                                            Day = 57

                                                        Language Translator Tool 

Dependencies (install as needed):
    pip install requests pyttsx3 pandas

Optional fallback (if LibreTranslate is unreachable):
    pip install googletrans==4.0.0rc1

Notes:
 - This uses the public LibreTranslate endpoint (https://libretranslate.com). Internet required.
 - If LibreTranslate fails, and googletrans is installed, the code will attempt googletrans as fallback.
 - The app provides detect, translate, swap languages, text-to-speech, and export history.

Run:
    python language_translator_tool.py
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import threading
import pyttsx3
import time
import csv
import os
import pandas as pd

# --- Configuration ---
LIBRE_ENDPOINT = "https://libretranslate.com"
TIMEOUT = 10  # seconds
DEFAULT_SRC = "auto"
DEFAULT_TGT = "en"
HISTORY_LIMIT = 500
# ----------------------

# Try optional googletrans if installed (used only if LibreTranslate fails)
try:
    from googletrans import Translator as GTTranslator
except Exception:
    GTTranslator = None

# Text-to-speech engine
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 160)

# Helper: fetch available languages from LibreTranslate (cached)
_lang_cache = None
def get_languages():
    global _lang_cache
    if _lang_cache:
        return _lang_cache
    try:
        resp = requests.get(f"{LIBRE_ENDPOINT}/languages", timeout=TIMEOUT)
        resp.raise_for_status()
        data = resp.json()
        # data is list of {"code":"en","name":"English"}
        lang_map = {entry["code"]: entry["name"] for entry in data}
        # include 'auto' option for detection
        lang_map = {"auto": "Auto-detect", **lang_map}
        _lang_cache = lang_map
        return lang_map
    except Exception:
        # fallback to a sensible minimal list
        fallback = {
            "auto": "Auto-detect",
            "en": "English", "es": "Spanish", "fr": "French",
            "de": "German", "hi": "Hindi", "zh": "Chinese",
            "ar": "Arabic", "ru": "Russian", "ja": "Japanese",
            "pt": "Portuguese", "bn": "Bengali", "ur": "Urdu",
        }
        _lang_cache = fallback
        return fallback

# Translate via LibreTranslate
def libre_translate(text, source, target):
    payload = {"q": text, "source": source if source != "auto" else "auto", "target": target, "format": "text"}
    try:
        r = requests.post(f"{LIBRE_ENDPOINT}/translate", data=payload, timeout=TIMEOUT)
        r.raise_for_status()
        return {"translatedText": r.json().get("translatedText")}
    except Exception as e:
        raise RuntimeError(f"LibreTranslate error: {e}")

# Detect language via LibreTranslate
def libre_detect(text):
    try:
        r = requests.post(f"{LIBRE_ENDPOINT}/detect", data={"q": text}, timeout=TIMEOUT)
        r.raise_for_status()
        # returns list of detections with 'language' and 'confidence'
        detections = r.json()
        if isinstance(detections, list) and detections:
            return detections[0].get("language"), detections[0].get("confidence", 0.0)
        return None, 0.0
    except Exception:
        return None, 0.0

# Fallback using googletrans if available
def google_translate(text, source, target):
    if GTTranslator is None:
        raise RuntimeError("googletrans not available")
    gt = GTTranslator()
    if source == "auto":
        res = gt.translate(text, dest=target)
    else:
        res = gt.translate(text, src=source, dest=target)
    return {"translatedText": res.text}

def google_detect(text):
    if GTTranslator is None:
        return None, 0.0
    gt = GTTranslator()
    res = gt.detect(text)
    if hasattr(res, "lang"):
        return res.lang, getattr(res, "confidence", 0.0)
    return None, 0.0

# High-level translate wrapper with graceful fallback
def translate_text(text, source, target):
    # try LibreTranslate first
    try:
        return libre_translate(text, source, target)
    except Exception:
        # fallback to googletrans if available
        if GTTranslator:
            try:
                return google_translate(text, source, target)
            except Exception as e:
                raise RuntimeError(f"No translation available: {e}")
        raise RuntimeError("Translation failed and no fallback available.")

def detect_language(text):
    # try Libre
    try:
        lang, conf = libre_detect(text)
        if lang:
            return lang, conf
    except Exception:
        pass
    # fallback
    if GTTranslator:
        try:
            return google_detect(text)
        except Exception:
            pass
    return None, 0.0

# ------------------------
# Tkinter UI
# ------------------------
class TranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Translator Tool")
        self.root.geometry("920x640")
        self.history = []  # list of dicts
        self.langs = get_languages()
        self.lang_codes = list(self.langs.keys())
        # UI variables
        self.src_var = tk.StringVar(value=DEFAULT_SRC)
        self.tgt_var = tk.StringVar(value=DEFAULT_TGT)
        self.status_var = tk.StringVar(value="Ready. Using LibreTranslate (if online).")
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ttk.Frame(self.root, padding=10)
        header.pack(fill="x")
        ttk.Label(header, text="Language Translator", font=("Segoe UI", 18, "bold")).pack(side="left")
        ttk.Button(header, text="Refresh Languages", command=self._refresh_languages).pack(side="right")

        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        # Input area
        input_frame = ttk.LabelFrame(main, text="Input", padding=10)
        input_frame.place(x=12, y=64, width=440, height=260)

        ttk.Label(input_frame, text="Source language:").grid(row=0, column=0, sticky="w")
        self.src_combo = ttk.Combobox(input_frame, textvariable=self.src_var, values=[f"{c} — {self.langs[c]}" for c in self.lang_codes], width=36)
        # combobox uses display text; manage selection mapping manually
        self.src_combo.grid(row=0, column=1, padx=6, pady=6)
        # set initial display value
        self._set_combo_value(self.src_combo, self.src_var.get())

        ttk.Label(input_frame, text="Target language:").grid(row=1, column=0, sticky="w")
        self.tgt_combo = ttk.Combobox(input_frame, textvariable=self.tgt_var, values=[f"{c} — {self.langs[c]}" for c in self.lang_codes], width=36)
        self.tgt_combo.grid(row=1, column=1, padx=6, pady=6)
        self._set_combo_value(self.tgt_combo, self.tgt_var.get())

        ttk.Button(input_frame, text="Detect Language", command=self._detect_button).grid(row=2, column=0, pady=6)
        ttk.Button(input_frame, text="Swap", command=self._swap_languages).grid(row=2, column=1, pady=6, sticky="e")

        ttk.Label(input_frame, text="Enter text to translate:").grid(row=3, column=0, columnspan=2, sticky="w", pady=(8,0))
        self.input_text = tk.Text(input_frame, wrap="word", height=8, width=52)
        self.input_text.grid(row=4, column=0, columnspan=2, pady=6)

        # Translate controls
        ttk.Button(main, text="Translate ▶", command=self._translate_button).place(x=480, y=160)
        ttk.Button(main, text="Speak Output 🔊", command=self._speak_output).place(x=600, y=160)

        # Output area
        output_frame = ttk.LabelFrame(main, text="Translation", padding=10)
        output_frame.place(x=12, y=340, width=896, height=240)
        self.output_text = tk.Text(output_frame, height=10, wrap="word")
        self.output_text.pack(fill="both", expand=True)

        # Bottom: history and controls
        bottom = ttk.Frame(self.root, padding=8)
        bottom.pack(side="bottom", fill="x")
        ttk.Button(bottom, text="Export History (CSV)", command=self._export_history).pack(side="left")
        ttk.Button(bottom, text="Clear History", command=self._clear_history).pack(side="left", padx=6)
        ttk.Button(bottom, text="Copy Translation", command=self._copy_translation).pack(side="left", padx=6)
        ttk.Label(bottom, textvariable=self.status_var).pack(side="right")

        # History list on the right
        history_frame = ttk.LabelFrame(main, text="Session History", padding=6)
        history_frame.place(x=480, y=12, width=428, height=136)
        self.history_list = tk.Listbox(history_frame, height=6)
        self.history_list.pack(side="left", fill="both", expand=True)
        hist_scroll = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_list.yview)
        self.history_list.configure(yscrollcommand=hist_scroll.set)
        hist_scroll.pack(side="right", fill="y")

        # Bind combobox selections: convert display string back to code
        self.src_combo.bind("<<ComboboxSelected>>", lambda e: self._on_combo_select(self.src_combo, self.src_var))
        self.tgt_combo.bind("<<ComboboxSelected>>", lambda e: self._on_combo_select(self.tgt_combo, self.tgt_var))

    # Helper to show code in combobox display
    def _set_combo_value(self, combo, code):
        display = f"{code} — {self.langs.get(code, code)}"
        combo.set(display)

    def _on_combo_select(self, combo, var):
        val = combo.get()
        # val format: "code — name"
        code = val.split("—")[0].strip() if "—" in val else val.strip()
        if code:
            var.set(code)

    def _refresh_languages(self):
        def job():
            self.status_var.set("Refreshing languages...")
            try:
                self.langs.clear()
                new = get_languages()
                self.langs.update(new)
                self.lang_codes[:] = list(self.langs.keys())
                # update combos
                vals = [f"{c} — {self.langs[c]}" for c in self.lang_codes]
                self.src_combo["values"] = vals
                self.tgt_combo["values"] = vals
                self._set_combo_value(self.src_combo, self.src_var.get())
                self._set_combo_value(self.tgt_combo, self.tgt_var.get())
                self.status_var.set("Languages refreshed.")
            except Exception as e:
                self.status_var.set("Failed to refresh languages.")
                messagebox.showwarning("Refresh failed", str(e))
        threading.Thread(target=job, daemon=True).start()

    def _detect_button(self):
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("Input required", "Enter text to detect language.")
            return
        def job():
            self.status_var.set("Detecting language...")
            lang, conf = detect_language(text)
            if lang:
                self.status_var.set(f"Detected: {lang} (confidence {conf:.2f})")
                # set source combobox to detected lang if present
                if lang in self.langs:
                    self.src_var.set(lang)
                    self._set_combo_value(self.src_combo, lang)
                else:
                    messagebox.showinfo("Detected", f"Detected language code: {lang} (not in list)")
            else:
                self.status_var.set("Language detection failed.")
                messagebox.showwarning("Detect failed", "Unable to detect language.")
        threading.Thread(target=job, daemon=True).start()

    def _swap_languages(self):
        a = self.src_var.get()
        b = self.tgt_var.get()
        self.src_var.set(b)
        self.tgt_var.set(a)
        self._set_combo_value(self.src_combo, b)
        self._set_combo_value(self.tgt_combo, a)

    def _translate_button(self):
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("Input required", "Enter text to translate.")
            return
        src = self.src_var.get() or "auto"
        tgt = self.tgt_var.get() or "en"
        # quick guard: if src==tgt, just copy
        if src == tgt and src != "auto":
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", text)
            self.status_var.set("Source and target are the same — copied input.")
            return

        def job():
            self.status_var.set("Translating...")
            try:
                res = translate_text(text, src, tgt)
                translated = res.get("translatedText") if isinstance(res, dict) else str(res)
                # update UI on main thread
                self.root.after(0, lambda: self._update_translation_ui(text, src, tgt, translated))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Translate failed", str(e)))
                self.root.after(0, lambda: self.status_var.set("Translate failed."))
        threading.Thread(target=job, daemon=True).start()

    def _update_translation_ui(self, source_text, src_code, tgt_code, translated_text):
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", translated_text)
        # record history
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        entry = {"time": ts, "source_lang": src_code, "target_lang": tgt_code, "source": source_text, "translation": translated_text}
        self.history.insert(0, entry)
        if len(self.history) > HISTORY_LIMIT:
            self.history = self.history[:HISTORY_LIMIT]
        self._refresh_history_list()
        self.status_var.set("Translation complete.")

    def _refresh_history_list(self):
        self.history_list.delete(0, tk.END)
        for h in self.history[:200]:
            disp = f"{h['time']} | {h['source_lang']}→{h['target_lang']} | {h['translation'][:48].replace(chr(10),' ')}"
            self.history_list.insert(tk.END, disp)

    def _speak_output(self):
        text = self.output_text.get("1.0", "end").strip()
        if not text:
            messagebox.showinfo("No output", "No translated text to speak.")
            return
        def job():
            try:
                tts_engine.say(text)
                tts_engine.runAndWait()
            except Exception as e:
                messagebox.showwarning("TTS failed", str(e))
        threading.Thread(target=job, daemon=True).start()

    def _export_history(self):
        if not self.history:
            messagebox.showinfo("No history", "No translations in this session to export.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile=f"translations_{int(time.time())}.csv")
        if not path:
            return
        try:
            df = pd.DataFrame(self.history)
            df.to_csv(path, index=False)
            messagebox.showinfo("Saved", f"History exported to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export failed", str(e))

    def _clear_history(self):
        if messagebox.askyesno("Confirm", "Clear session history?"):
            self.history.clear()
            self._refresh_history_list()
            self.status_var.set("History cleared.")

    def _copy_translation(self):
        text = self.output_text.get("1.0", "end").strip()
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Translation copied to clipboard.")

# Entry point
if __name__ == "__main__":
    # ensure cache directory exists (requests may not need it)
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = TranslatorApp(root)
    root.mainloop()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                      Thanks for visiting and keep supporting....
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

