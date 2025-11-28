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
  {
        "name": "One-Pan Veg Cheesy Quesadilla",
        "cuisine": "Mexican",
        "veg": True,
        "time": 20,
        "difficulty": "Easy",
        "tags": ["cheesy", "fun", "handheld"],
        "ingredients": ["tortilla/roti", "cheese", "veggies"],
        "notes": "Ideal for movie night, not for dieting."
    },
    {
        "name": "Overnight Oats (Prep for Tomorrow)",
        "cuisine": "Western",
        "veg": True,
        "time": 10,
        "difficulty": "Very Easy",
        "tags": ["light", "prep-ahead", "healthy"],
        "ingredients": ["oats", "milk/curd", "fruits"],
        "notes": "Technically ‘cooking’, but zero gas stove involved."
    },
]

MOOD_TAGS = {
    "Comfort / Heavy": ["comfort", "cheesy", "heavy"],
    "Light / Healthy": ["light", "healthy", "prep-ahead"],
    "Spicy / Intense": ["spicy", "street-style"],
    "Experimental / Fun": ["fun", "handheld", "student"]
}


# ----------------------------
# Scoring logic
# ----------------------------
def score_recipe(recipe, prefs):
    """
    Higher score = better match.
    prefs = {
        'time_limit': int,
        'veg_pref': 'Any'|'Veg'|'Non-veg',
        'cuisine': 'Any' or string,
        'mood': key from MOOD_TAGS or 'Any'
    }
    """
    score = 0
    reasons = []

    # Time: penalize if over limit
    if prefs["time_limit"] is not None:
        if recipe["time"] <= prefs["time_limit"]:
            # closer to limit gets slightly less reward than very quick
            score += 3
            reasons.append(f"fits your time ({recipe['time']} min ≤ {prefs['time_limit']} min)")
        else:
            # soft penalty
            score -= 3
            reasons.append(f"takes longer than your time ({recipe['time']} min)")

    # Veg preference
    if prefs["veg_pref"] == "Veg" and not recipe["veg"]:
        score -= 100  # hard block
        reasons.append("non-veg but you chose veg")
    elif prefs["veg_pref"] == "Non-veg" and recipe["veg"]:
        score -= 15   # strong penalty but still possible
        reasons.append("veg dish but you selected non-veg")
    elif prefs["veg_pref"] != "Any":
        score += 1
    # Cuisine
    if prefs["cuisine"] != "Any":
        if recipe["cuisine"] == prefs["cuisine"]:
            score += 4
            reasons.append(f"matches cuisine: {recipe['cuisine']}")
        else:
            score -= 1

    # Mood
    if prefs["mood"] != "Any":
        desired_tags = MOOD_TAGS.get(prefs["mood"], [])
        matches = set(recipe["tags"]).intersection(desired_tags)
        if matches:
            score += 4 + len(matches)
            reasons.append(f"fits mood: {', '.join(matches)}")
        else:
            score -= 1

    # Small randomness so results aren't identical every time
    score += random.uniform(-0.5, 0.5)

    return score, reasons


def recommend_recipes(prefs, top_n=3):
    scored = []
    for r in RECIPES:
        s, reasons = score_recipe(r, prefs)
        scored.append((s, r, reasons))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top_n]

# ----------------------------
# GUI
# ----------------------------

class CookTonightApp:
    def __init__(self, root):
        self.root = root
        self.root.title('"What to cook tonight?" – Mini Recommender')
        self.root.geometry("900x600")
        self.root.minsize(850, 550)

        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        # Left: preferences
        left = ttk.Frame(main, width=260)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        ttk.Label(left, text='What to cook tonight?', font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

        ttk.Label(left, text="Time available (minutes)").pack(anchor="w")
        self.time_var = tk.StringVar(value="30")
        ttk.Entry(left, textvariable=self.time_var, width=10).pack(anchor="w", pady=(0, 8))

        ttk.Label(left, text="Veg / Non-veg").pack(anchor="w")
        self.veg_var = tk.StringVar(value="Any")
        ttk.Radiobutton(left, text="Any", value="Any", variable=self.veg_var).pack(anchor="w")
        ttk.Radiobutton(left, text="Veg only", value="Veg", variable=self.veg_var).pack(anchor="w")
        ttk.Radiobutton(left, text="Non-veg focus", value="Non-veg", variable=self.veg_var).pack(anchor="w")

        ttk.Label(left, text="Cuisine preference", padding=(0, 8, 0, 0)).pack(anchor="w")
        cuisines = ["Any"] + sorted({r["cuisine"] for r in RECIPES})
        self.cuisine_var = tk.StringVar(value="Any")
        ttk.Combobox(left, textvariable=self.cuisine_var, values=cuisines,
                     state="readonly", width=18).pack(anchor="w", pady=(0, 8))

        ttk.Label(left, text="Mood", padding=(0, 8, 0, 0)).pack(anchor="w")
        mood_opts = ["Any"] + list(MOOD_TAGS.keys())
        self.mood_var = tk.StringVar(value="Any")
        ttk.Combobox(left, textvariable=self.mood_var, values=mood_opts,
                     state="readonly", width=22).pack(anchor="w")

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=10)

        t
       ttk.Button(left, text="Recommend", command=self.on_recommend).pack(fill="x", pady=(0, 5))
        ttk.Button(left, text="Random Surprise", command=self.on_surprise).pack(fill="x")

        self.status_var = tk.StringVar(value="Set your mood and time, then click Recommend.")
        ttk.Label(left, textvariable=self.status_var, wraplength=230, foreground="#666").pack(anchor="w", pady=(10, 0))

        # Right: results
        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(right, text="Suggestions", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.results_text = tk.Text(right, wrap="word", font=("Consolas", 10))
        self.results_text.pack(fill="both", expand=True, pady=(4, 0))

        # configure tags for styling
        self.results_text.tag_configure("title", font=("Segoe UI", 11, "bold"))
        self.results_text.tag_configure("meta", foreground="#888")
        self.results_text.tag_configure("bullet", foreground="#333")
        self.results_text.tag_configure("reason", foreground="#1565C0")
        self.results_text.tag_configure("notes", foreground="#4E342E")

        # show initial hint
        self._show_intro_message()

    def _parse_time_limit(self):
        raw = self.time_var.get().strip()
        if not raw:
            return None
        try:
            val = int(raw)
            if val <= 0:
                return None
            return val
        except ValueError:
            return None

    def on_recommend(self):
        time_limit = self._parse_time_limit()
        prefs = {
            "time_limit": time_limit,
            "veg_pref": self.veg_var.get(),
            "cuisine": self.cuisine_var.get(),
            "mood": self.mood_var.get(),
        }

        results = recommend_recipes(prefs, top_n=3)
        self._display_results(results, prefs)

    def on_surprise(self):
        # Ignore most filters, just favour time and veg
        time_limit = self._parse_time_limit()
        prefs = {
            "time_limit": time_limit,
            "veg_pref": self.veg_var.get(),
            "cuisine": "Any",
            "mood": "Any",
        }
        results = recommend_recipes(prefs, top_n=1)
        self._display_results(results, prefs, surprise=True)
