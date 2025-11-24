"""
Project 67: Interactive Train Route Map (Toy)
--------------------------------------------

Features:
 - Schematic train/metro map rendered on a Tkinter Canvas
 - Click on stations to set "From" and "To"
 - Or choose "From" and "To" from dropdowns
 - Shows shortest route (by number of stops) using BFS
 - Highlights the route path and stations
 - Displays number of stops and list of stations in order

Everything is in-memory (no real data); you can edit STATIONS and LINES
to reflect your own city/network.

Run:
    python train_route_map.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque


# --------------------------
# Network Data (Toy Example)
# --------------------------

# Station coordinates are on a 0–100 grid (we’ll scale to canvas)
STATIONS = [
    {"id": "JP1", "name": "North Yard",     "x": 10, "y": 10, "line": "Blue"},
    {"id": "JP2", "name": "Civil Lines",    "x": 25, "y": 20, "line": "Blue"},
    {"id": "JP3", "name": "Old City",       "x": 40, "y": 30, "line": "Blue"},
    {"id": "JP4", "name": "Central Jn",     "x": 55, "y": 40, "line": "Blue"},
    {"id": "JP5", "name": "Tech Park",      "x": 70, "y": 50, "line": "Blue"},
    {"id": "JP6", "name": "Campus East",    "x": 85, "y": 60, "line": "Blue"},

    {"id": "GR1", "name": "Lake View",      "x": 15, "y": 45, "line": "Green"},
    {"id": "GR2", "name": "Museum",         "x": 30, "y": 50, "line": "Green"},
    {"id": "GR3", "name": "Central Jn",     "x": 55, "y": 40, "line": "Green"},  # shared ID with JP4
    {"id": "GR4", "name": "Market Square",  "x": 65, "y": 28, "line": "Green"},
    {"id": "GR5", "name": "Airport",        "x": 80, "y": 15, "line": "Green"},

    {"id": "RD1", "name": "West End",       "x": 5,  "y": 70, "line": "Red"},
    {"id": "RD2", "name": "Stadium",        "x": 25, "y": 70, "line": "Red"},
    {"id": "RD3", "name": "Central Jn",     "x": 55, "y": 40, "line": "Red"},
    {"id": "RD4", "name": "IT Hub",         "x": 78, "y": 70, "line": "Red"},
    {"id": "RD5", "name": "South Terminal", "x": 92, "y": 82, "line": "Red"},
]

# Shared node: we want "Central Jn" to be a single logical station with multiple line colors.
# To keep it simple we’ll merge any stations that share same name as "Central Jn"
# For adjacency, we define lines as ordered station names, not IDs.

LINES = {
    "Blue":  {
        "color": "#2196F3",
        "stations": ["North Yard", "Civil Lines", "Old City", "Central Jn", "Tech Park", "Campus East"],
    },
    "Green": {
        "color": "#4CAF50",
        "stations": ["Lake View", "Museum", "Central Jn", "Market Square", "Airport"],
    },
    "Red":   {
        "color": "#F44336",
        "stations": ["West End", "Stadium", "Central Jn", "IT Hub", "South Terminal"],
    },
}


# --------------------------
# Data Structures
# --------
