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
      # Generate + Save
        ttk.Button(left, text="Generate Neon", command=self.generate).pack(fill="x", pady=5)
        ttk.Button(left, text="Save Image", command=self.save_image).pack(fill="x", pady=5)

        # Preview area
        self.preview_label = tk.Label(right, bg="#000000")
        self.preview_label.pack(fill="both", expand=True)

        self.current_image = None
        self.tk_image = None

    def pick_text_color(self):
        color = colorchooser.askcolor(initialcolor=self.text_color)[1]
        if color:
            self.text_color = color

    def pick_glow_color(self):
        color = colorchooser.askcolor(initialcolor=self.glow_color)[1]
        if color:
            self.glow_color = color

    def pick_bg_color(self):
        color = colorchooser.askcolor(initialcolor=self.bg_color)[1]
        if color:
            self.bg_co


 def generate(self):
        if not self.font_path:
            tk.messagebox.showerror("Error", "Font not found on your system.")
            return

        text = self.text_entry.get()

        img = generate_neon_image(
            text=text,
            font_path=self.font_path,
            font_size=self.font_size.get(),
            text_color=self.text_color,
            glow_color=self.glow_color,
            bg_color=self.bg_color,
            blur_radius=self.blur_radius.get(),
            glow_layers=self.glow_layers.get(),
            flicker=self.flicker_var.get()
        )

        self.current_image = img

        # Resize for preview
        preview = img.copy()
        preview.thumbnail((700, 500))
        self.tk_image = tk.PhotoImage(preview.convert("RGB"))

        self.preview_label.config(image=self.tk_image)

    def save_image(self):
        if self.current_image is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )

        if file_path:
            self.current_image.save(file_path)


# --------------------------
# Run
# --------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = NeonGeneratorApp(root)
    root.mainloop()

