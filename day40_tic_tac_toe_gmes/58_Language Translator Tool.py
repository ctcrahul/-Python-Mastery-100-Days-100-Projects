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
        # fallback to a sens
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

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                      Thanks for visiting and keep supporting..
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

