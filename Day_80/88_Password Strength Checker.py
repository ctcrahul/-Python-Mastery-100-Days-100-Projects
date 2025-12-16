"""
Project 88 — Password Strength Checker

Run:
    python password_checker.py

Features:
- Strength score (0–100)
- Detects weak patterns
- Estimates brute-force crack time
- Flags common passwords
"""

import math
import re
import time

COMMON_PASSWORDS = {
    "password", "123456", "123456789", "qwerty",
    "abc123", "password1", "admin", "letmein",
    "welcome", "iloveyou"
}

CHARSETS = {
    "lower": 26,
    "upper": 26

CHARSETS = {
    "lower": 26,
    "upper": 26,
    "digits": 10,
    "symbols": 32
}


def analyze_charset(password):
    size = 0
    if re.search(r"[a-z]", password):
        size += CHARSETS["lower"]
    if re.search(r"[A-Z]", password):
        size += CHARSETS["upper"]
    if re.search(r"\d", password):
        size += CHARSETS["digits"]
    if re.search(r"[^\w]", password):
        size += CHARSETS["symbols"]
    return size


def entropy(password):
    charset_size = analyze_charset(password)
    if charset_size == 0:
        return 0
    return len(password) * math.log2(charset_size)


def crack_time(entropy_bits):
    guesses_per_sec = 1e9  # modern GPU
    seconds = (2 ** entropy_bits) / guesses_per_sec
    return seconds


def human_time(seconds):
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    if seconds < 3600:
        return f"{seconds / 60:.1f} minutes"
    if seconds < 86400:
        return f"{seconds / 3600:.1f} hours"
    if seconds < 31536000:
        return f"{seconds / 86400:.1f} days"
    return f"{seconds / 31536000:.1f} years"

