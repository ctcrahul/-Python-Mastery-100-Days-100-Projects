"""                                                                  Day = 63

                                                             Photo Filter Marketplace Mock
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

        self.status_var = tk.StringVar(value="Load an image to begin.")
        ttk.Label(top, textvariable=self.status_var, foreground="#555555").pack(side="right")

        # Main layout: left thumbnails, right preview
        main = ttk.Frame(self.root, padding=8)
        main.pack(fill="both", expand=True)

        # Left: filter list / thumbnails
        left = ttk.Frame(main)
        left.pack(side="left", fill="y")

        ttk.Label(left, text="Filter Marketplace", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.filter_canvas = tk.Canvas(left, width=260, bg="#f7f7f7", highlightthickness=0)
        self.filter_scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.filter_canvas.yview)
        self.filter_canvas.configure(yscrollcommand=self.filter_scrollbar.set)

        self.filter_frame = ttk.Frame(self.filter_canvas)
        self.filter_canvas.create_window((0, 0), window=self.filter_frame, anchor="nw")

        self.filter_canvas.pack(side="left", fill="y", expand=False)
        self.filter_scrollbar.pack(side="left", fill="y")

        self.filter_frame.bind("<Configure>", lambda e: self.filter_canvas.configure(scrollregion=self.filter_canvas.bbox("all")))

        # Right: preview
        right = ttk.Frame(main)
        right.pack(side="right", fill="both", expand=True)

        ttk.Label(right, text="Preview", font=("Segoe UI", 12, "bold")).pack(anchor="w")

        self.preview_label = ttk.Label(right, anchor="center")
        self.preview_label.pack(fill="both", expand=True, padx=8, pady=8)

        self.market_info = tk.Text(right, height=10)
        self.market_info.pack(fill="x", padx=8, pady=4)
        self.market_info.insert("1.0", "Filter info will appear here.")
        self.market_info.config(state="disabled")

    # -----------------------------
    # Image loading and handling
    # -----------------------------
    def load_image(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                ("All files", "*.*"),
            ]
        )
        if not path:
            return
        try:
            img = Image.open(path).convert("RGB")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")
            return

        self.original_image = img
        self.display_image = self._resize_keep_aspect(self.original_image, self.preview_size)
        self.current_filter_name = "Original"
        self._update_preview()
        self._build_filter_thumbnails()
        self.status_var.set(f"Loaded image: {os.path.basename(path)}")

    def _resize_keep_aspect(self, img, max_size):
        w, h = img.size
        max_w, max_h = max_size
        scale = min(max_w / w, max_h / h)
        if scale > 1:
            scale = 1
        new_w = int(w * scale)
        new_h = int(h * scale)
        return img.resize((new_w, new_h), Image.LANCZOS)

    # -----------------------------
    # Thumbnails
    # -----------------------------
    def _build_filter_thumbnails(self):
        # Clear previous thumbnails
        for child in self.filter_frame.winfo_children():
            child.destroy()
        self.thumbnail_photoimages.clear()

        if self.display_image is None:
            return

        for idx, (name, func) in enumerate(FILTERS.items()):
            frame = ttk.Frame(self.filter_frame, padding=4)
            frame.pack(fill="x", padx=2, pady=2)

            thumb_img = self._resize_keep_aspect(self.display_image, self.thumbnail_size)
            try:
                filtered_thumb = func(thumb_img)
            except Exception:
                filtered_thumb = thumb_img.copy()

            tk_img = ImageTk.PhotoImage(filtered_thumb)
            self.thumbnail_photoimages[name] = tk_img  # keep ref

            img_label = tk.Label(frame, image=tk_img, bd=1, relief="solid", cursor="hand2")
            img_label.pack(side="left")
            img_label.bind("<Button-1>", lambda e, n=name: self.on_filter_click(n))

            info_frame = ttk.Frame(frame)
            info_frame.pack(side="left", fill="x", expand=True, padx=6)

            ttk.Label(info_frame, text=name, font=("Segoe UI", 10, "bold")).pack(anchor="w")
            ttk.Label(info_frame, text="Click to preview", foreground="#777777").pack(anchor="w")

    def on_filter_click(self, filter_name):
        if self.display_image is None:
            return
        self.current_filter_name = filter_name
        self._update_preview()
        self._update_market_info(filter_name)

    # -----------------------------
    # Preview + info
    # -----------------------------
    def _update_preview(self):
        if self.display_image is None:
            return
        func = FILTERS.get(self.current_filter_name, apply_original)
        try:
            filtered = func(self.display_image)
        except Exception:
            filtered = self.display_image.copy()

        self.current_filtered = filtered
        tk_img = ImageTk.PhotoImage(filtered)
        self.preview_label.img_ref = tk_img
        self.preview_label.configure(image=tk_img)

    def _update_market_info(self, filter_name):
        # Fake marketplace info
        desc = {
            "Original": "The unedited original image.",
            "Grayscale": "Classic black-and-white style. Great for dramatic moods.",
            "Sepia Classic": "Warm vintage tones, like old film photos.",
            "Warm Glow": "Adds a gentle warm tint. Good for sunsets and portraits.",
            "Cool Tone": "Cooler blue vibe. Good for city and tech aesthetics.",
            "High Contrast Pop": "Punchy colors and strong contrast. Eye-catching for social posts.",
            "Soft Pastel": "Soft, dreamy tones. Ideal for calm, minimal visuals.",
            "Vignette Mood": "Darkened edges to focus the subject in center.",
            "Film Fade": "Low contrast, faded film look. Great for nostalgic scenes.",
            "HDR Pop": "Sharper detail with boosted colors. Good for landscapes.",
            "Ink Sketch": "Rough sketch effect for artistic posters."
        }
        text = f"Filter: {filter_name}\n\n{desc.get(filter_name, 'A custom filter look.')}\n\nYou can save this as a preset or export the filtered image."
        self.market_info.config(state="normal")
        self.market_info.delete("1.0", "end")
        self.market_info.insert("1.0", text)
        self.market_info.config(state="disabled")

    # -----------------------------
    # Saving filtered image
    # -----------------------------
    def save_filtered(self):
        if self.original_image is None:
            messagebox.showinfo("No image", "Load an image first.")
            return
        # apply filter on full-res image
        func = FILTERS.get(self.current_filter_name, apply_original)
        try:
            filtered = func(self.original_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply filter: {e}")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All files", "*.*")],
            initialfile=f"{self.current_filter_name.replace(' ', '_').lower()}.jpg"
        )
        if not path:
            return
        try:
            filtered.save(path)
            messagebox.showinfo("Saved", f"Filtered image saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save image: {e}")

    # -----------------------------
    # Preset handling
    # -----------------------------
    def save_as_preset(self):
        if self.current_filter_name is None:
            messagebox.showinfo("No filter", "Select a filter first.")
            return
        name = simpledialog.askstring("Preset Name", "Enter a name for this preset:")
        if not name:
            return
        name = name.strip()
        if not name:
            return
        self.presets[name] = self.current_filter_name
        save_presets(self.presets)
        self.preset_combo["values"] = list(self.presets.keys())
        self.preset_combo.set(name)
        self.status_var.set(f"Saved preset '{name}' -> {self.current_filter_name}")

    def apply_preset(self):
        preset_name = self.preset_combo.get()
        if not preset_name:
            messagebox.showinfo("No preset", "Choose a preset from the list.")
            return
        filter_name = self.presets.get(preset_name)
        if not filter_name or filter_name not in FILTERS:
            messagebox.showerror("Error", "Preset refers to an unknown filter.")
            return
        if self.display_image is None:
            messagebox.showinfo("No image", "Load an image first.")
            return
        self.current_filter_name = filter_name
        self._update_preview()
        self._update_market_info(filter_name)
        self.status_var.set(f"Applied preset '{preset_name}' ({filter_name})")

    def delete_preset(self):
        preset_name = self.preset_combo.get()
        if not preset_name:
            messagebox.showinfo("No preset", "Select a preset to delete.")
            return
        if preset_name not in self.presets:
            return
        if not messagebox.askyesno("Delete Preset", f"Delete preset '{preset_name}'?"):
            return
        del self.presets[preset_name]
        save_presets(self.presets)
        vals = list(self.presets.keys())
        self.preset_combo["values"] = vals
        self.preset_combo.set(vals[0] if vals else "")
        self.status_var.set(f"Deleted preset '{preset_name}'")


# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = FilterMarketplaceApp(root)
    root.mainloop()



#===========================================================================================================================================================================
                                                                   Keep Learning Keep Exploring....
#===========================================================================================================================================================================


