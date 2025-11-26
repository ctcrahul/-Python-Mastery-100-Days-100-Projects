import tkinter as tk
from tkinter import ttk, filedialog, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import random
import os

# --------------------------
# Neon Rendering Core
# --------------------------

def generate_neon_image(
    text,
    font_path,
    font_size,
    text_color,
    glow_color,
    bg_color,
    blur_radius,
    glow_layers,
    flicker=False
):
    """
    Creates a neon glowing text image.
    """
