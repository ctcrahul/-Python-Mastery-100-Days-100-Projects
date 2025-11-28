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
    {   "name": "Spicy Schezwan Noodles",
        "cuisine": "Asian",
        "veg": True,
        "time": 25,
        "difficulty": "Medium",
        "tags": ["spicy", "street-style", "fun"],
        "ingredients": ["noodles", "schezwan sauce", "veggies"],
        "notes": "Pretty loud on flavour. Not for a ‘light’ mood."
    },
    {
        "name": "Grilled Chicken Bowl",
        "cuisine": "Fusion",
        "veg": False,
        "time": 35,
        "difficulty": "Medium",
        "tags": ["protein", "light", "healthy"],
        "ingredients": ["chicken", "rice", "veggies", "yogurt"],
        "notes": "High protein, low nonsense. Good if you pretend to be disciplined."
    },
    {
        "name": "Egg Bhurji with Toast",
        "cuisine": "Indian",
        "veg": False,
        "time": 15,
        "difficulty": "Easy",
        "tags": ["quick", "protein", "comfort", "breakfast-for-dinner"],
        "ingredients": ["eggs", "onion", "tomato", "bread"],
        "notes": "Lazy, fast, and secretly pretty high in protein."
    },
    {
        "name": "Chole Rice Bowl",
        "cuisine": "Indian",
        "veg": True,
        "time": 40,
        "difficulty": "Medium",
        "tags": ["comfort", "heavy", "spicy", "weekend"],
        "ingredients": ["chickpeas", "onion", "tomato", "spices", "rice"],
        "notes": "Not ideal for late-night if you want to sleep, but great comfort food."
    },
    {
        "name": "Tomato Basil Soup with Toast",
        "cuisine": "Italian",
        "veg": True,
        "time": 30,
        "difficulty": "Easy",
        "tags": ["light", "comfort", "evening"],
        "ingredients": ["tomatoes", "onion", "garlic", "basil", "bread"],
        "notes": "For when you want to feel like you have your life together."
    },
    {
        "name": "Curd Rice with Tempering",
        "cuisine": "South Indian",
        "veg": True,
        "time": 20,
        "difficulty": "Easy",
        "tags": ["light", "comfort", "summer"],
        "ingredients": ["rice", "curd", "mustard seeds", "chilies"],
        "notes": "Ideal when your stomach is done with your bad decisions."
    },
    {
        "name": "Tandoori Chicken (Oven / Airfryer)",
        "cuisine": "Indian",
        "veg": False,
        "time": 45,
        "difficulty": "Medium",
        "tags": ["spicy", "protein", "weekend", "party"],
        "ingredients": ["chicken", "yogurt", "spices"],
        "notes": "Takes time to marinate & cook, but feels like a reward."
    },
