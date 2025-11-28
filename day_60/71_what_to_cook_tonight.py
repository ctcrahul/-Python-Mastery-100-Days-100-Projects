"""
Project 71: "What to cook tonight?" – Mini Recommender
------------------------------------------------------

Single-file Python app that:
 - Lets you choose:
     * Time available
     * Veg / Non-veg
     * Cuisine preference
     * Mood (Comfort / Light / Spicy / Experimental)
 - Recommends top recipes from an in-memory "database"
 - Shows why each recipe was picked (matched tags)

No external dependencies – only tkinter.

Run:
    python what_to_cook_tonight.py
"""

import tkinter as tk
from tkinter import ttk
import random
import textwrap

# ----------------------------
# Recipe "database"
# ----------------------------
