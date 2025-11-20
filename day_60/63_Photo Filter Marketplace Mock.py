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

def apply_soft_pastel(img):
    img = ImageOps.autocontrast(img)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.7)
    img = img.filter(ImageFilter.GaussianBlur(radius=1))
    return img


def apply_vignette(img):
    w, h = img.size
    vignette = Image.new("L", (w, h), 0)
    for y in range(h):
        for x in range(w):
            dx = (x - w / 2) / (w / 2)
            dy = (y - h / 2) / (h / 2)
            d = (dx * dx + dy * dy) ** 0.5
            val = int(max(0, 255 * (1 - d)))
            vignette.putpixel((x, y), val)
    mask = vignette.filter(ImageFilter.GaussianBlur(radius=min(w, h) * 0.05))
    dark = Image.new("RGB", (w, h), "#000000")
    blended = Image.composite(img, dark, mask)
    return blended


def apply_film_fade(img):
    img = apply_grayscale(img)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(0.8)
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)
    return img


def apply_hdr_pop(img):
    img1 = ImageEnhance.Color(img).enhance(1.3)
    img2 = ImageEnhance.Sharpness(img1).enhance(1.5)
    return img2



def apply_ink_sketch(img):
    gray = ImageOps.grayscale(img)
    blurred = gray.filter(ImageFilter.GaussianBlur(radius=2))
    edges = ImageChalkEdge(gray, blurred)
    return edges


def ImageChalkEdge(gray, blurred):
    # simple pseudo-edge effect
    import numpy as np
    g = np.array(gray, dtype="int16")
    b = np.array(blurred, dtype="int16")
    e = abs(g - b)
    e = 255 - e * 3
    e = e.clip(0, 255).astype("uint8")
    return Image.fromarray(e).convert("RGB")


FILTERS = {
    "Original": apply_original,
    "Grayscale": apply_grayscale,
    "Sepia Classic": apply_sepia,
    "Warm Glow": apply_warm,
    "Cool Tone": apply_cool,
    "High Contrast Pop": apply_high_contrast,
    "Soft Pastel": apply_soft_pastel,
    "Vignette Mood": apply_vignette,
    "Film Fade": apply_film_fade,
    "HDR Pop": apply_hdr_pop,
    "Ink Sketch": apply_ink_sketch,
}


# -----------------------------
# Preset storage helpers
# -----------------------------
def load_presets():
    if not os.path.exists(PRESETS_FILE):
        return {}
    try:
        with open(PRESETS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_presets(presets):
    try:
        with open(PRESETS_FILE, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save presets: {e}")

# -----------------------------
# Main GUI App
# -----------------------------
class FilterMarketplaceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Filter Marketplace Mock")
        self.root.geometry("1200x700")

        self.original_image = None  # full-res PIL
        self.display_image = None   # PIL resized for preview
        self.current_filtered = None
        self.current_filter_name = "Original"

        self.thumbnail_size = (220, 220)
        self.preview_size = (480, 480)

      self.thumbnail_photoimages = {}  # keep references
        self.presets = load_presets()    # name -> filter_name

        self._build_ui()

    def _build_ui(self):
        # Top bar
        top = ttk.Frame(self.root, padding=8)
        top.pack(side="top", fill="x")

        ttk.Button(top, text="Load Image", command=self.load_image).pack(side="left", padx=4)
        ttk.Button(top, text="Save Current Filtered Image", command=self.save_filtered).pack(side="left", padx=4)

        ttk.Separator(top, orient="vertical").pack(side="left", fill="y", padx=8)

        ttk.Label(top, text="Presets:", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.preset_combo = ttk.Combobox(top, values=list(self.presets.keys()), state="readonly", width=20)
        self.preset_combo.pack(side="left", padx=4)
        ttk.Button(top, text="Apply Preset", command=self.apply_preset).pack(side="left", padx=4)
        ttk.Button(top, text="Save Current as Preset", command=self.save_as_preset).pack(side="left", padx=4)
        ttk.Button(top, text="Delete Preset", command=self.delete_preset).pack(side="left", padx=4)




