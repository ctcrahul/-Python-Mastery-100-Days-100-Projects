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

# -----------------------------
# Filter definitions
# -----------------------------
def apply_original(img):
    return img.copy()


def apply_grayscale(img):
    return ImageOps.grayscale(img).convert("RGB")


def apply_sepia(img):
    gray = ImageOps.grayscale(img)
    sepia = ImageOps.colorize(gray, "#704214", "#FFDCB8")
    return sepia

def apply_warm(img):
    r, g, b = img.split()
    r = r.point(lambda i: min(255, int(i * 1.1)))
    b = b.point(lambda i: int(i * 0.9))
    return Image.merge("RGB", (r, g, b))


def apply_cool(img):
    r, g, b = img.split()
    r = r.point(lambda i: int(i * 0.9))
    b = b.point(lambda i: min(255, int(i * 1.1)))
    return Image.merge("RGB", (r, g, b))


def apply_high_contrast(img):
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.8)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.3)
    return img



