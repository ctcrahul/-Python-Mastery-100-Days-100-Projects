"""
Project 63: Photo Filter Marketplace Mock
-----------------------------------------

A single-file Python app that:
- Lets you load a photo
- Shows multiple filter variants as thumbnails (like a mini filter marketplace)
- Lets you:
    * Click thumbnails to preview the filtered version
    * Save the filtered image
    * Save/load simple "presets" (favorite filters) to a JSON file

Dependencies:
    pip install pillow

Run:
    python photo_filter_marketplace.py
"""

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps

PRESETS_FILE = "filter_presets.json"
