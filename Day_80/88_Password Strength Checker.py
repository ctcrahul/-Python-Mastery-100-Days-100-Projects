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


def score_password(password):
    score = 0

    if len(password) >= 12:
        score += 30
    elif len(password) >= 8:
        score += 15

    if re.search(r"[A-Z]", password):
        score += 15
    if re.search(r"[a-z]", password):
        score += 15
    if re.search(r"\d", password):
        score += 15
    if re.search(r"[^\w]", password):
        score += 10

    if password.lower() in COMMON_PASSWORDS:
        score = 0

    return min(score, 100)


def analyze(password):
    print("\n--- PASSWORD ANALYSIS ---")

    ent = entropy(password)
    sec = crack_time(ent)
    score = score_password(password)

    print(f"Length       : {len(password)}")
    print(f"Entropy      : {ent:.2f} bits")
    print(f"Crack Time   : {human_time(sec)}")
    print(f"Strength     : {score}/100")

    if password.lower() in COMMON_PASSWORDS:
        print("⚠ WARNING: Common leaked password")

    if score < 40:
        print("❌ Weak password")
    elif score < 70:
        print("⚠ Medium strength")
    else:
        print("✅ Strong password")


def main():
    pw = input("Enter password to check: ")
    analyze(pw)


if __name__ == "__main__":
    main()
