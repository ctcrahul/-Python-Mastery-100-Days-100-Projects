
Animated Weather Widget
"""
Project 65: Animated Weather Widget (Mock Data)
----------------------------------------------

Single-file Python app with:
 - Modern Tkinter UI
 - Animated weather scene (sun, clouds, rain, snow, storm)
 - Mock 3-day forecast for a few cities
 - Smooth transitions when switching city/day

Dependencies:
    Only standard library (tkinter) – no extra installs.

Run:
    python animated_weather_widget.py
"""

import tkinter as tk
from tkinter import ttk
import random
import math
import time


# ------------------ Mock Weather Data ------------------ #
MOCK_FORECAST = [
    # city, day, condition, temp, high, low
    ("Jaipur", "Today",     "Sunny",   31, 33, 24),
    ("Jaipur", "Tomorrow",  "Cloudy",  29, 31, 23),
    ("Jaipur", "Day After", "Storm",   26, 28, 22),

    ("Bengaluru", "Today",     "Rainy",   24, 26, 20),
    ("Bengaluru", "Tomorrow",  "Cloudy",  25, 27, 21),
    ("Bengaluru", "Day After", "Sunny",   27, 29, 22),
