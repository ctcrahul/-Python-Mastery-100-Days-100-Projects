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
   # Canvas size (dynamic based on text)
    padding = 80
    temp_img = Image.new("RGBA", (2000, 500), (0, 0, 0, 0))
    draw = ImageDraw.Draw(temp_img)

    font = ImageFont.truetype(font_path, font_size)

    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    img_w = w + padding * 2
    img_h = h + padding * 2

    img = Image.new("RGBA", (img_w, img_h), bg_color)
    draw = ImageDraw.Draw(img)

    x = padding
    y = padding

    # Glow layers
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    for i in range(glow_layers):
        offset = i * 2

        # Flicker effect
        if flicker:
            flicker_offset = random.randint(-2, 2)
        else:
            flicker_offset = 0

        glow_draw.text(
            (x + flicker_offset, y + flicker_offset),
            text,
            font=font,
            fill=glow_color
        )

        glow = glow.filter(ImageFilter.GaussianBlur(blur_radius))

    # Draw glow onto image
    img = Image.alpha_composite(img, glow)

    # Main text
    draw = ImageDraw.Draw(img)
    draw.text((x, y), text, font=font, fill=text_color)

    return img

# --------------------------
# GUI App
# --------------------------

class NeonGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Sign Text Generator")
        self.root.geometry("1100x650")

        self.font_path = self.get_default_font()
        self.text_color = "#ffffff"
        self.glow_color = "#ff00ff"
        self.bg_color = "#000000"

        self.setup_ui()

    def get_default_font(self):
        # Try common fonts gracefully
        possible_fonts = [
            "arial.ttf",
            "Arial.ttf",
            "C:\\Windows\\Fonts\\arial.ttf"
        ]
        for f in possible_fonts:
            if os.path.exists(f):
                return f
        return None


  def setup_ui(self):
        left = ttk.Frame(self.root, padding=10)
        left.pack(side="left", fill="y")

        right = ttk.Frame(self.root, padding=10)
        right.pack(side="right", fill="both", expand=True)

        # Title
        ttk.Label(left, text="Neon Sign Controls", font=("Segoe UI", 14, "bold")).pack(pady=5)

        # Text input
        ttk.Label(left, text="Your Text").pack(anchor="w")
        self.text_entry = tk.Entry(left, width=25)
        self.text_entry.insert(0, "HELLO WORLD")
        self.text_entry.pack(pady=5)

        # Font size
        ttk.Label(left, text="Font Size").pack(anchor="w")
        self.font_size = tk.IntVar(value=120)
        ttk.Scale(left, from_=40, to=200, variable=self.font_size, orient="horizontal").pack(fill="x")

        # Blur
        ttk.Label(left, text="Glow Blur").pack(anchor="w")
        self.blur_radius = tk.IntVar(value=25)
        ttk.Scale(left, from_=5, to=70, variable=self.blur_radius, orient="horizontal").pack(fill="x")

        # Glow strength
        ttk.Label(left, text="Glow Strength").pack(anchor="w")
        self.glow_layers = tk.IntVar(value=8)
        ttk.Scale(left, from_=2, to=15, variable=self.glow_layers, orient="horizontal").pack(fill="x")

        # Flicker option
        self.flicker_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(left, text="Enable Flicker Effect", variable=self.flicker_var).pack(pady=10)

        # Colors
        ttk.Button(left, text="Text Color", command=self.pick_text_color).pack(fill="x", pady=2)
        ttk.Button(left, text="Glow Color", command=self.pick_glow_color).pack(fill="x", pady=2)
        ttk.Button(left, text="Background Color", command=self.pick_bg_color).pack(fill="x", pady=2)

        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=10)

