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
