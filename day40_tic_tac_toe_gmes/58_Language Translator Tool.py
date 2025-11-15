"""
Language Translator Tool (single-file)

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

