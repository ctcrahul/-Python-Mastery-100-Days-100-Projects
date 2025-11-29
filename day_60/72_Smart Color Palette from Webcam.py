import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import cv2
import numpy as np
from sklearn.cluster import KMeans
from PIL import Image, ImageDraw
import threading
import time
import colorsys
import io

# --------------------------
# Helpers
# --------------------------
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def resize_for_kmeans(img, max_pixels=10000):
    h, w = img.shape[:2]
    scale = (max_pixels / (w * h)) ** 0.5 if (w*h) > max_pixels else 1.0
    if scale < 1.0:
        new_w = max(1, int(w * scale))
        new_h = max(1, int(h * scale))
        return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return img

def extract_palette(img_bgr, n_colors=5, sample_pixels=8000, random_state=42):
    # img_bgr is OpenCV BGR image
    img = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    small = resize_for_kmeans(img, max_pixels=sample_pixels)
    pixels = small.reshape(-1, 3).astype(float)

    # KMeans
    km = KMeans(n_clusters=n_colors, random_state=random_state, n_init=10)
    labels = 
  centers = km.cluster_centers_.astype(int)

    # compute percentages
    _, counts = np.unique(labels, return_counts=True)
    total = counts.sum()
    percents = counts / total
    # sort by percentage desc
    order = np.argsort(-percents)
    sorted_centers = centers[order]
    sorted_percents = percents[order]
    hexes = [rgb_to_hex(c) for c in sorted_centers]
    return list(zip(sorted_centers.tolist(), sorted_percents.tolist(), hexes))

def make_palette_image(colors, sw=120, sh=120, rows=1, padding=8):
    # colors: list of (rgb, percent, hex)
    cols = len(colors)
    width = cols * sw + (cols + 1) * padding
    height = sh + 2 * padding
    img = Image.new("RGB", (width, height), (30,30,30))
    draw = ImageDraw.Draw(img)
    for i, (rgb, pct, hx) in enumerate(colors):
        x = padding + i * (sw + padding)
        y = padding
        draw.rectangle([x, y, x + sw, y + sh], fill=tuple(rgb))
        # hex text
        text = f"{hx}\n{int(pct*100)}%"
        # choose text color based on brightness
        r, g, b = rgb
        lum = (0.299*r + 0.587*g + 0.114*b)
        text_color = (255,255,255) if lum < 140 else (20,20,20)
        draw.text((x+6, y+6), text, fill=text_color)
    return img

# --------------------------
# GUI + Webcam Thread
# --------------------------
class PaletteApp:
    def __init__(self, root):
        self.root = root
        root.title("Smart Palette from Webcam")
        root.geometry("920x560")
        self.running = True
