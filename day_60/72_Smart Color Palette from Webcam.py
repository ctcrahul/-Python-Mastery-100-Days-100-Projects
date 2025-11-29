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
       # Webcam
        self.cap = None
        self.cam_thread = None
        self.frame = None
        self.lock = threading.Lock()

        # UI state
        self.n_colors = tk.IntVar(value=5)
        self.sample_pixels = tk.IntVar(value=8000)
        self.last_palette = None

        self._build_ui()
        self._start_camera()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True)

        right = ttk.Frame(main, width=340)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        # Video panel (left)
        self.video_label = tk.Label(left, bg="black")
        self.video_label.pack(fill="both", expand=True, padx=6, pady=6)

        control_frame = ttk.Frame(left)
        control_frame.pack(fill="x", pady=(4,0))

        ttk.Label(control_frame, text="Colors:").pack(side="left")
        ttk.Spinbox(control_frame, from_=2, to=12, width=4, textvariable=self.n_colors).pack(side="left", padx=6)

        ttk.Label(control_frame, text="Sample pixels:").pack(side="left", padx=(12,4))
        ttk.Spinbox(control_frame, from_=1000, to=20000, increment=1000, width=6, textvariable=self.sample_pixels).pack(side="left")

        ttk.Button(control_frame, text="Capture Palette", command=self.on_capture).pack(side="right", padx=6)
        ttk.Button(control_frame, text="Freeze Frame", command=self.on_freeze).pack(side="right")

        # Right panel controls
        ttk.Label(right, text="Palette", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(6,4), padx=8)

        self.palette_canvas = tk.Canvas(right, width=320, height=220, bg="#222", highlightthickness=0)
        self.palette_canvas.pack(padx=8, pady=6)
       ttk.Label(right, text="Hex Codes (click to copy):", font=("Segoe UI", 10)).pack(anchor="w", padx=8, pady=(8,0))
        self.hex_frame = ttk.Frame(right)
        self.hex_frame.pack(fill="x", padx=8, pady=6)

        ttk.Button(right, text="Save Palette Image", command=self.on_save_palette).pack(fill="x", padx=8, pady=(8,0))
        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=8, padx=8)
        ttk.Label(right, text="Tips:", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=8)
        tips = (
            "• Move the camera closer for richer colors.\n"
            "• Use more sample pixels for smoother clustering.\n"
            "• Click a hex code to copy it to clipboard.\n"
            "• Save palette as PNG for sharing."
        )
        ttk.Label(right, text=tips, wraplength=300, foreground="#666").pack(anchor="w", padx=8, pady=6)

    def _start_camera(self):
        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap or not self.cap.isOpened():
                raise RuntimeError("Could not open webcam")
        except Exception as e:
            messagebox.showerror("Camera error", f"Failed to open webcam: {e}")
            return

        self.cam_thread = threading.Thread(target=self._camera_loop, daemon=True)
        self.cam_thread.start()
        # schedule UI update
        self.root.after(30, self._update_video_label)

    def _camera_loop(self):
        while True:
            if not self.cap or not self.cap.isOpened():
                break
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue
            with self.lock:
                self.frame = frame.copy()
            time.sleep(0.02)  # throttle slightly
  def _update_video_label(self):
        with self.lock:
            frame = None if self.frame is None else self.frame.copy()
        if frame is not None:
            # convert BGR->RGB and to PhotoImage via PIL
            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w = img_rgb.shape[:2]
            # keep aspect to fit label size
            label_w = self.video_label.winfo_width() or 640
            label_h = self.video_label.winfo_height() or 360
            scale = min(label_w / w, label_h / h)
            new_w = int(w * scale)
            new_h = int(h * scale)
            resized = cv2.resize(img_rgb, (new_w, new_h), interpolation=cv2.INTER_AREA)
            # convert to PGM-like bytes for Tk PhotoImage (PIL would be nicer but avoids extra conversion steps)
            from PIL import Image, ImageTk
            pil = Image.fromarray(resized)
            tkimg = ImageTk.PhotoImage(image=pil)
            self.video_label.imgtk = tkimg
            self.video_label.config(image=tkimg)
        if self.running:
            self.root.after(30, self._update_video_label)

    def on_freeze(self):
        # toggles freeze: when frozen, camera still runs but frame shown is last captured
        # We'll capture current frame into self.frame and stop updating preview until next unfreeze
        with self.lock:
            if self.frame is None:
                return
            frozen = getattr(self, "_frozen", False)
            if not frozen:
                self._frozen_frame = self.frame.copy()
                pil = Image.fromarray(cv2.cvtColor(self._frozen_frame, cv2.COLOR_BGR2RGB))
                from PIL import ImageTk
                tkimg = ImageTk.PhotoImage(image=pil.resize((self.video_label.winfo_width() or 640, self.video_label.winfo_height() or 360), resample=Image.BILINEAR))
                self.video_label.imgtk = tkimg
                self.video_label.config(image=tkimg)
                self._frozen = True
            else:
                self._frozen = False
