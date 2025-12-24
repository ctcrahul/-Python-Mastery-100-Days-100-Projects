# Project 96: URL Shortener with Analytics
# Author: You

import string
import random
import json
from datetime import datetime

DATA_FILE = "urls.json"

# -----------------------------
# Load / Save Data
# -----------------------------
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)
