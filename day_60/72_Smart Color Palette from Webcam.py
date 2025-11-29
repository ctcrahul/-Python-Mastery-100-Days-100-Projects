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
