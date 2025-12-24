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
# -----------------------------
# Generate Short Code
# -----------------------------
def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))

# -----------------------------
# Shorten URL
# -----------------------------
def shorten_url(original_url):
    data = load_data()
    short_code = generate_code()

    while short_code in data:
        short_code = generate_code()

    data[short_code] = {
        "original_url": original_url,
        "created_at": datetime.now().isoformat(),
        "clicks": 0
    }

    save_data(data)
    return short_code
# -----------------------------
# Access URL
# -----------------------------
def access_url(short_code):
    data = load_data()

    if short_code not in data:
        print("Invalid short URL")
        return

    data[short_code]["clicks"] += 1
    save_data(data)

    print("Redirecting to:", data[short_code]["original_url"])
