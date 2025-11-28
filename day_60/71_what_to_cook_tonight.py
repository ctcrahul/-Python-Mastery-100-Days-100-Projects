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
RECIPES = [
    {
        "name": "Masala Maggi Upgrade",
        "cuisine": "Indian",
        "veg": True,
        "time": 15,
        "difficulty": "Easy",
        "tags": ["quick", "spicy", "comfort", "student", "cheap"],
        "ingredients": ["maggi", "onion", "tomato", "green chili", "masala"],
        "notes": "Your classic hostel hack, but slightly upgraded with veggies and extra spices."
    },
    {
        "name": "Simple Dal Tadka",
        "cuisine": "Indian",
        "veg": True,
        "time": 30,
        "difficulty": "Easy",
        "tags": ["comfort", "light", "home-style", "protein"],
        "ingredients": ["lentils", "ghee", "garlic", "onion", "tomato", "spices"],
        "notes": "Classic comfort bowl. Easy, filling, and safe choice on a tired day."
    },
    {
        "name": "Paneer Bhurji Wrap",
        "cuisine": "Indian",
        "veg": True,
        "time": 25,
        "difficulty": "Medium",
        "tags": ["protein", "spicy", "handheld", "fun"],
        "ingredients": ["paneer", "onion", "capsicum", "tortilla/roti"],
        "notes": "Takes bhurji and turns it into a portable wrap."
    },
    {
        "name": "Veg Fried Rice",
        "cuisine": "Asian",
        "veg": True,
        "time": 25,
        "difficulty": "Easy",
        "tags": ["quick", "one-pot", "light"],
        "ingredients": ["rice", "mixed veggies", "soy sauce", "garlic"],
        "notes": "Good way to use leftover rice. Light but satisfying."
    },
    {
        "name": "Garlic Butter Pasta",
        "cuisine": "Italian",
        "veg": True,
        "time": 20,
        "difficulty": "Easy",
        "tags": ["comfort", "creamy", "quick"],
        "ingredients": ["pasta", "garlic", "butter", "cheese"],
        "notes": "Minimal ingredients. Heavy on comfort, light on effort."
    },
    {
