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


