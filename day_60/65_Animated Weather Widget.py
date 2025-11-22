
Animated Weather Widget
"""
Project 65: Animated Weather Widget (Mock Data)
----------------------------------------------

Single-file Python app with:
 - Modern Tkinter UI
 - Animated weather scene (sun, clouds, rain, snow, storm)
 - Mock 3-day forecast for a few cities
 - Smooth transitions when switching city/day

Dependencies # Small footer info
        self.info_label = ttk.Label(
            right,
            text="Mock data only.\nAnimations reflect each condition.",
            font=("Segoe UI", 8),
            foreground="#666666"
        )
        self.info_label.pack(anchor="w", pady=(4, 0))

    # ---------------- Logic helpers ---------------- #
    def _get_forecast_for(self, city):
        rows = [r for r in MOCK_FORECAST if r[0] == city]
        # ensure same order: Today, Tomorrow, Day After
        sorted_rows = sorted(rows, key=lambda r: self.day_names.index(r[1]) if r[1] in self.day_names else 99)
        return sorted_rows

    def _current_forecast_row(self):
        city = self.city_var.get()
        rows = self._get_forecast_for(city)
        if not rows:
            return None
        idx = min(self.current_day_index, len(rows)-1)
        return rows[idx]

    def _update_forecast_labels(self):
        row = self._current_forecast_row()
        if not row:
            self.temp_label.config(text="--°C")
            self.cond_label.config(text="")
            self.range_label.config(text="")
            return
        city, day, cond, temp, high, low = 
    Only standard library (tkinter) – no extra installs.

Run:
    python animated_weather_widget.py
        self._build_ui()
        self._update_forecast_labels()
        self._apply_scene_from_current_forecast()

    def _build_ui(self):
        # Layout: left = canvas, right = controls
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        # Left canvas
        canvas_frame
"""

import tkinter as tk
from tkinter import ttk
import random
import math
import time

        )
        self._draw_vertical_gradient(top_color, bottom_color)

        # horizon ground
        ground_h = int(self.height * 0.25)
        self.canvas.create_rectangle(
            0, self.height - ground_h,
    @staticmethod
    def _hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # ---------- Element creators ---------- #
    def _create_sun(self):
        if self.sun_item is not None:
            return

        r = min(self.width, self.height) * 0.08
        cx = int(self.width * 0.15)
        cy = int(self.height * 0.2)
        self.sun_item = self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="#FFD54F", outline="#FFB300", width=2
        )

    def _create_clouds(self, darker=False):
        color = "#ECEFF1" if not darker else "#B0BEC5"
        count = 4 if not darker else 3
        cloud_height = int(self.height * 0.25)
        for i in range(count):
            w = int(self.width * 0.25)
            h = int(self.height * 0.10)
            x = random.randint(0, max(1, self.width - w))
            y = random.randint(int(cloud_height * 0.2), int(cloud_height * 0.8))
            cloud = self._draw_cloud(x, y, w, h, color)
            self.cloud_items.append(cloud)

    def _draw_cloud(self, x, y, w, h, color):
        # simple cloud = group of ovals (return group tag)
        tag = f"cloud_{time.time()}_{random.randint(0,9999)}"
        for i in range(5):
            ox = x + int((i * w) / 5) + random.randint(-5, 5)
            oy = y + random.randint(-5, 5)
            rw = int(w * 0.35)
            rh = int(h * 0.75)
            self.canvas.create_oval(
                ox, oy, ox + rw, oy + rh,
                fill=color, outline=color, tags=tag
            )
        return tag

    def _create_rain(self, count=80):
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            length = random.randint(8, 18)
            drop = self.canvas.create_line(
                x, y, x, y + length,
                fill="#BBDEFB", width=2
            )
            self.rain_drops.append((drop, length))

    def _create_snow(self, count=60):
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            r = random.randint(2, 4)
            flake = self.canvas.create_oval(
                x-r, y-r, x+r, y+r,
                fill="#FFFFFF", outline=""
            )
            self.snow_flakes.append((flake, r))

    def _create_haze(self):
        layers = 5
        for i in range(layers):
            y1 = int(self.height * (0.3 + 0.1 * i))
            y2 = y1 + int(self.height * 0.1)
            alpha = int(80 + i*25)
            color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
            rect = self.canvas.create_rectangle(
                0, y1, self.width, y2,
                fill="#CFD8DC", outline=""
            )
            self.haze_rects.append(rect)

    # ---------- Animation loop ---------- #
    def animate(self):
        if not self.running:
            return

        self.t += 0.03
        if self.width <= 0 or self.height <= 0:
            self.canvas.after(50, self.animate)
            return

        # animate sun
        if self.sun_item is not None:
            self._animate_sun()

        # animate clouds
        if self.cloud_items:
            self._animate_clouds()

        # rain
        if self.rain_drops:
            self._animate_rain()

        # snow
        if self.snow_flakes:
            self._animate_snow()

        # storm lightning
        if self.current_condition == "Storm":
            self._animate_storm_lightning()

        self.canvas.after(40, self.animate)

    def _animate_sun(self):
        # sun gently bobs up and down in a small arc
        r = min(self.width, self.height) * 0.08
        cx_base = int(self.width * 0.15)
        cy_base = int(self.height * 0.18)
        dx = math.cos(self.t * 0.7) * 10
        dy = math.sin(self.t * 0.9) * 6
        cx = cx_base + dx
        cy = cy_base + dy
        self.canvas.coords(
            self.sun_item,
            cx - r, cy - r, cx + r, cy + r
        )

    def _animate_clouds(self):
        # slowly move clouds horizontally, wrap around
        for tag in self.cloud_items:
            self.canvas.move(tag, 0.8, 0)
            bbox = self.canvas.bbox(tag)
            if bbox and bbox[0] > self.width:
                # move cloud to left outside screen
                width = bbox[2] - bbox[0]
                dx = -bbox[0] - width
                self.canvas.move(tag, dx, 0)

    def _animate_rain(self):
        for i, (drop, length) in enumerate(self.rain_drops):
            self.canvas.move(drop, 0, 8)
            x1, y1, x2, y2 = self.canvas.coords(drop)
            if y1 > self.height:
                # reset to top
                new_x = random.randint(0, self.width)
                self.canvas.coords(drop, new_x, -length, new_x, 0)

    def _animate_snow(self):
        for flake, r in self.snow_flakes:
            dx = math.sin(self.t + flake) * 0.5
            self.canvas.move(flake, dx, 1.5)
            x1, y1, x2, y2 = self.canvas.coords(flake)
            if y1 > self.height:
                new_x = random.randint(0, self.width)
                self.canvas.coords(flake, new_x-r, -r, new_x+r, r)

    def _animate_storm_lightning(self):
        # occasionally flash screen with lightning
        if random.random() < 0.01:
            # draw a quick lightning flash rectangle
            if self.lightning_item is None:
                self.lightning_item = self.canvas.create_rectangle(
                    0, 0, self.width, self.height,
                    fill="#FFFFFF", outline=""
                )
                self.canvas.after(80, self._clear_lightning)

    def _clear_lightning(self):
        if self.lightning_item is not None:
            self.canvas.delete(self.lightning_item)
            self.lightning_item = None


# ------------------ Main App UI ------------------ #
class WeatherWidgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Weather Widget")
        self.root.geometry("1000x550")
        self.root.minsize(900, 500)

        self.current_city = "Jaipur"
        self.current_day_index = 0

        self._build_ui()
        self._update_forecast_labels()
        self._apply_scene_from_current_forecast()

    def _build_ui(self):
        # Layout: left = canvas, right = controls
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        # Left canvas
        canvas_frame = ttk.Frame(main)
        canvas_frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.scene = WeatherScene(self.canvas)

        # Right panel
        right = ttk.Frame(main, width=260)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        title = ttk.Label(right, text="Smart Weather Widget", font=("Segoe UI", 14, "bold"))
        title.pack(anchor="w", pady=(0, 10))

        # City selector
        ttk.Label(right, text="City").pack(anchor="w")
        self.city_var = tk.StringVar(value=self.current_city)
        cities = sorted({row[0] for row in MOCK_FORECAST})
        self.city_combo = ttk.Combobox(right, textvariable=self.city_var, values=cities, state="readonly")
        self.city_combo.pack(fill="x", pady=4)
        self.city_combo.bind("<<ComboboxSelected>>", lambda e: self._on_city_change())

        # Day selector
        ttk.Label(right, text="Day").pack(anchor="w", pady=(10, 0))
        self.day_buttons_frame = ttk.Frame(right)
        self.day_buttons_frame.pack(fill="x", pady=4)

        self.day_names = ["Today", "Tomorrow", "Day After"]
        self.day_btn_vars = []
        for i, name in enumerate(self.day_names):
            var = tk.StringVar(value=name)
            btn = ttk.Button(self.day_buttons_frame, text=name,
                             command=lambda idx=i: self._set_day_index(idx))
            btn.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
            self.day_buttons_frame.columnconfigure(i, weight=1)
            self.day_btn_vars.append(var)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=10)

        # Forecast labels
        self.temp_label = ttk.Label(right, text="--°C", font=("Segoe UI", 26, "bold"))
        self.temp_label.pack(anchor="w")

        self.cond_label = ttk.Label(right, text="", font=("Segoe UI", 12))
        self.cond_label.pack(anchor="w", pady=(2, 6))

        self.range_label = ttk.Label(right, text="", font=("Segoe UI", 10))
        self.range_label.pack(anchor="w")

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=10)

        # Mini next-days list
        ttk.Label(right, text="3-Day Snapshot", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        self.snapshot_box = tk.Text(right, height=6, width=30)
        self.snapshot_box.pack(fill="x", pady=4)
        self.snapshot_box.config(state="disabled")

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=10)

        # Small footer info
        self.info_label = ttk.Label(
            right,
            text="Mock data only.\nAnimations reflect each condition.",
            font=("Segoe UI", 8),
            foreground="#666666"
        )
        self.info_label.pack(anchor="w", pady=(4, 0))

    # ---------------- Logic helpers ---------------- #
    def _get_forecast_for(self, city):
        rows = [r for r in MOCK_FORECAST if r[0] == city]
        # ensure same order: Today, Tomorrow, Day After
        sorted_rows = sorted(rows, key=lambda r: self.day_names.index(r[1]) if r[1] in self.day_names else 99)
        return sorted_rows

    def _current_forecast_row(self):
        city = self.city_var.get()
        rows = self._get_forecast_for(city)
        if not rows:
            return None
        idx = min(self.current_day_index, len(rows)-1)
        return rows[idx]

    def _update_forecast_labels(self):
        row = self._current_forecast_row()
        if not row:
            self.temp_label.config(text="--°C")
            self.cond_label.config(text="")
            self.range_label.config(text="")
            return
        city, day, cond, temp, high, low = row
        self.temp_label.config(text=f"{temp}°C")
        cond_display = CONDITION_DISPLAY.get(cond, cond)
        self.cond_label.config(text=f"{day} · {cond_display}")
        self.range_label.config(text=f"High {high}°  •  Low {low}°")

        # Snapshot box
        forecast_rows = self._get_forecast_for(city)
        self.snapshot_box.config(state="normal")
        self.snapshot_box.delete("1.0", "end")
        for r in forecast_rows:
            _, d, c, t, hi, lo = r
            cd = CONDITION_DISPLAY.get(c, c)
            self.snapshot_box.insert("end", f"{d:<10} {t:>2}°  ({lo}°–{hi}°)  {cd}\n")
        self.snapshot_box.config(state="disabled")

        # highlight selected day button
        for i, child in enumerate(self.day_buttons_frame.winfo_children()):
            if i == self.current_day_index:
                child.configure(style="Selected.TButton")
            else:
                child.configure(style="TButton")

    def _apply_scene_from_current_forecast(self):
        row = self._current_forecast_row()
        if not row:
            return
        condition = row[2]
        # map some conditions to our scenes
        if condition == "Haze":
            scene_cond = "Haze"
        elif condition == "Storm":
            scene_cond = "Storm"
        elif condition == "Rainy":
            scene_cond = "Rainy"
        elif condition == "Cloudy":
            scene_cond = "Cloudy"
        elif condition == "Snow":
            scene_cond = "Snow"
        else:
            scene_cond = "Sunny"
        self.scene.set_condition(scene_cond)

    # ------------- Event handlers ------------- #
    def _set_day_index(self, idx):
        self.current_day_index = idx
        self._update_forecast_labels()
        self._apply_scene_from_current_forecast()

    def _on_city_change(self):
        self.current_day_index = 0
        self._update_forecast_labels()
        self._apply_scene_from_current_forecast()


# ------------------ Run app ------------------ #
if __name__ == "__main__":
    root = tk.Tk()

    # Slightly nicer button style
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("Selected.TButton", background="#1976D2", foreground="white")
    style.map("Selected.TButton",
              background=[("active", "#1565C0")],
              foreground=[("active", "white")])

    app = WeatherWidgetApp(root)
    root.mainloop()








            self.width, self.height,
            fill="#4CAF50", outline=""
        )

        # add basic elements by condition
        if self.current_co
# ------------------ Mock Weather Data ------------------ #
MOCK_FORECAST = [
    # city, day, condition, temp, high, low
    ("Jaipur", "Today",     "Sunny",   31, 33, 24),
    ("Jaipur", "Tomorrow",  "Cloudy",  29, 31, 23),
    ("Jaipur", "Day After", "Storm",   26, 28, 22),

    ("Bengaluru", "Today",     "Rainy",   24, 26, 20),
    ("Bengaluru", "Tomorrow",  "Cloudy",  25, 27, 21),
    ("Bengaluru", "Day After", "Sunny",   27, 29, 22),
    ("Delhi", "Today",     "Haze",    30, 32, 25),
    ("Delhi", "Tomorrow",  "Sunny",   32, 34, 26),
    ("Delhi", "Day After", "Storm",   28, 30, 24),

    ("Mumbai", "Today",     "Rainy",   28, 30, 25),
    ("Mumbai", "Tomorrow",  "Rainy",   27, 29, 24),
    ("Mumbai", "Day After", "Cloudy",  29, 31, 25),
]

CONDITIONS = ["Sunny", "Cloudy", "Rainy", "Storm", "Snow", "Haze"]

# Map condition to display text + emoji
CONDITION_DISPLAY = {
    "Sunny":  "Sunny ☀️",
    "Cloudy": "Cloudy ☁️",
    "Rainy":  "Rainy 🌧",        )
        self._draw_vertical_gradient(top_color, bottom_color)

        # horizon ground
        ground_h = int(self.height * 0.25)
        self.canvas.create_rectangle(
            0, self.height - ground_h,
            self.width, self.height,
            fill="#4CAF50", outline=""
        )

        # add basic elements by condition
        if self.current_co
    "Storm":  "Storm ⛈",
    "Snow":   "Snow ❄️",
    "Haze":   "Hazy 🌫",
}

# Nice gradients per condition (top_color, bottom_color)
CONDITION_GRADIENTS = {
    "Sunny":  ("#87CEFA", "#FFE082"),
    "Cloudy": ("#B0BEC5", "#ECEFF1"),
    "Rainy":  ("#546E7A", "#90A4AE"),
    "Storm":  ("#263238", "#455A64"),
    "Snow":   ("#B3E5FC", "#E1F5FE"),
    "Haze":   ("#CFD8DC", "#ECEFF1"),
}


# ------------------ Scene Animator ------------------ #
class WeatherScene:
    def __init__(self, canvas: tk.Canvas):
        self.canvas = canvas
        self.width = 0
        self.height = 0
        self.current_condition = "Sunny"

        # animation state
        self.t = 0
        self.sun_item = None
        self.cloud_items = []
        self.rain_drops = []
        self.snow_flakes = []
        self.lightning_item = None
        self.haze_rects = []

        self.running = True
        self._setup_bindings()
        self.animate()

    def _setup_bindings(self):
        # keep tracking size
        self.canvas.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self.width = event.width
        self.height = event.height
        # force redraw background & objects
        self._reset_scene_objects()

    def set_condition(self, condition: str):
        self.current_condition = condition
        self._reset_scene_objects()

    def _reset_scene_objects(self):
        self.canvas.delete("all")
        self.sun_item = None
        self.cloud_items = []
        self.rain_drops = []
        self.snow_flakes = []
        self.lightning_item = None
        self.haze_rects = []
        if self.width and self.height:
            self._create_static_elements()

    def _create_static_elements(self):
        # background gradient
        top_color, bottom_color = CONDITION_GRADIENTS.get(
            self.current_condition, CONDITION_GRADIENTS["Sunny"]
        )
        self._draw_vertical_gradient(top_color, bottom_color)

        # horizon ground
        ground_h = int(self.height * 0.25)
        self.canvas.create_rectangle(
            0, self.height - ground_h,
            self.width, self.height,
            fill="#4CAF50", outline=""
        )

        # add basic elements by condition
        if self.current_condition in ("Sunny", "Haze", "Cloudy"):
            self._create_sun()
        if self.current_condition in ("Cloudy", "Rainy", "Storm"):
            self._create_clouds()
        if self.current_condition == "Rainy":
            self._create_rain()
        if self.current_condition == "Snow":
            self._create_snow()
        if self.current_condition == "Storm":
            self._create_clouds(darker=True)
        if self.current_condition == "Haze":
            self._create_haze()

    def _draw_vertical_gradient(self, top_color, bottom_color, steps=40):
        self.canvas.delete("bg")
        # simple linear gradient with rectangles
        r1, g1, b1 = self._hex_to_rgb(top_color)
        r2, g2, b2 = self._hex_to_rgb(bottom_color)
        for i in range(steps):
            ratio = i / (steps - 1)
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y1 = int(self.height * (i / steps))
            y2 = int(self.height * ((i + 1) / steps))
            self.canvas.create_rectangle(
                0, y1, self.width, y2,
                outline="", fill=color, tags="bg"
            )

    @staticmethod
    def _hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    # ---------- Element creators ---------- #
    def _create_sun(self):
        if self.sun_item is not None:
            return
        r = min(self.width, self.height) * 0.08
        cx = int(self.width * 0.15)
        cy = int(self.height * 0.2)
        self.sun_item = self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            fill="#FFD54F", outline="#FFB300", width=2
        )

    def _create_clouds(self, darker=False):
        color = "#ECEFF1" if not darker else "#B0BEC5"
        count = 4 if not darker else 3
        cloud_height = int(self.height * 0.25)
        for i in range(count):
            w = int(self.width * 0.25)
            h = int(self.height * 0.10)
            x = random.randint(0, max(1, self.width - w))
            y = random.randint(int(cloud_height * 0.2), int(cloud_height * 0.8))
            cloud = self._draw_cloud(x, y, w, h, color)
            self.cloud_items.append(cloud)

    def _draw_cloud(self, x, y, w, h, color):
        # simple cloud = group of ovals (return group tag)
        tag = f"cloud_{time.time()}_{random.randint(0,9999)}"
        for i in range(5):
            ox = x + int((i * w) / 5) + random.randint(-5, 5)
            oy = y + random.randint(-5, 5)
            rw = int(w * 0.35)
            rh = int(h * 0.75)
            self.canvas.create_oval(
                ox, oy, ox + rw, oy + rh,
                fill=color, outline=color, tags=tag
            )
        return tag

    def _create_rain(self, count=80):
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            length = random.randint(8, 18)
            drop = self.canvas.create_line(
                x, y, x, y + length,
                fill="#BBDEFB", width=2
            )
            self.rain_drops.append((drop, length))

    def _create_snow(self, count=60):
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            r = random.randint(2, 4)
            flake = self.canvas.create_oval(
                x-r, y-r, x+r, y+r,
                fill="#FFFFFF", outline=""
            )
            self.snow_flakes.append((flake, r))

    def _create_haze(self):
        layers = 5
        for i in range(layers):
            y1 = int(self.height * (0.3 + 0.1 * i))
            y2 = y1 + int(self.height * 0.1)
            alpha = int(80 + i*25)
            color = f"#{alpha:02x}{alpha:02x}{alpha:02x}"
            rect = self.canvas.create_rectangle(
                0, y1, self.width, y2,
                fill="#CFD8DC", outline=""
            )
            self.haze_rects.append(rect)

    # ---------- Animation loop ---------- #
    def animate(self):
        if not self.running:
            return

        self.t += 0.03
        if self.width <= 0 or self.height <= 0:
            self.canvas.after(50, self.animate)
            return

        # animate sun
        if self.sun_item is not None:
            self._animate_sun()

        # animate clouds
        if self.cloud_items:
            self._animate_clouds()

        # rain
        if self.rain_drops:
            self._animate_rain()

        # snow
        if self.snow_flakes:
            self._animate_snow()

        # storm lightning
        if self.current_condition == "Storm":
            self._animate_storm_lightning()

        self.canvas.after(40, self.animate)

    def _animate_sun(self):
        # sun gently bobs up and down in a small arc
        r = min(self.width, self.height) * 0.08
        cx_base = int(self.width * 0.15)
        cy_base = int(self.height * 0.18)
        dx = math.cos(self.t * 0.7) * 10
        dy = math.sin(self.t * 0.9) * 6
        cx = cx_base + dx
        cy = cy_base + dy
        self.canvas.coords(
            self.sun_item,
            cx - r, cy - r, cx + r, cy + r
        )

    def _animate_clouds(self):
        # slowly move clouds horizontally, wrap around
        for tag in self.cloud_items:
            self.canvas.move(tag, 0.8, 0)
            bbox = self.canvas.bbox(tag)
            if bbox and bbox[0] > self.width:
                # move cloud to left outside screen
                width = bbox[2] - bbox[0]
                dx = -bbox[0] - width
                self.canvas.move(tag, dx, 0)

    def _animate_rain(self):
        for i, (drop, length) in enumerate(self.rain_drops):
            self.canvas.move(drop, 0, 8)
            x1, y1, x2, y2 = self.canvas.coords(drop)
            if y1 > self.height:
                # reset to top
                new_x = random.randint(0, self.width)
                self.canvas.coords(drop, new_x, -length, new_x, 0)

    def _animate_snow(self):
        for flake, r in self.snow_flakes:
            dx = math.sin(self.t + flake) * 0.5
            self.canvas.move(flake, dx, 1.5)
            x1, y1, x2, y2 = self.canvas.coords(flake)
            if y1 > self.height:
                new_x = random.randint(0, self.width)
                self.canvas.coords(flake, new_x-r, -r, new_x+r, r)

    def _animate_storm_lightning(self):
        # occasionally flash screen with lightning
        if random.random() < 0.01:
            # draw a quick lightning flash rectangle
            if self.lightning_item is None:
                self.lightning_item = self.canvas.create_rectangle(
                    0, 0, self.width, self.height,
                    fill="#FFFFFF", outline=""
                )
                self.canvas.after(80, self._clear_lightning)

    def _clear_lightning(self):
        if self.lightning_item is not None:
            self.canvas.delete(self.lightning_item)
            self.lightning_item = None


# ------------------ Main App UI ------------------ #
class WeatherWidgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Animated Weather Widget")
        self.root.geometry("1000x550")
        self.root.minsize(900, 500)

        self.current_city = "Jaipur"
        self.current_day_index = 0

        self._build_ui()
        self._update_forecast_labels()
        self._apply_scene_from_current_forecast()

    def _build_ui(self):
        # Layout: left = canvas, right = controls
        main = ttk.Frame(self.root, padding=10)
        main.pack(fill="both", expand=True)

        # Left canvas
        canvas_frame = ttk.Frame(main)
        canvas_frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg="#000000", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.scene = WeatherScene(self.canvas)

        # Right panel
        right = ttk.Frame(main, width=260)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        title = ttk.Label(right, text="Smart Weather Widget", font=("Segoe UI", 14, "bold"))
        title.pack(anchor="w", pady=(0, 10))

        # City selector
        ttk.Label(right, text="City").pack(anchor="w")
        self.city_var = tk.StringVar(value=self.current_city)
        cities = sorted({row[0] for row in MOCK_FORECAST})
        self.city_combo = ttk.Combobox(right, textvariable=self.city_var, values=cities, state="readonly")
        self.city_combo.pack(fill="x", pady=4)
        self.city_combo.bind("<<ComboboxSelected>>", lambda e: self._on_city_change())

        # Day selector
        ttk.Label(right, text="Day").pack(anchor="w", pady=(10, 0))
        self.day_buttons_frame = ttk.Frame(right)
        self.day_buttons_frame.pack(fill="x", pady=4)

        self.day_names = ["Today", "Tomorrow", "Day After"]
        self.day_btn_vars = []
        for i, name in enumerate(self.day_names):
            var = tk.StringVar(value=name)
            btn = ttk.Button(self.day_buttons_frame, text=name,
                             command=lambda idx=i: self._set_day_index(idx))
            btn.grid(row=0, column=i, padx=2, pady=2, sticky="ew")
            self.day_buttons_frame.columnconfigure(i, weight=1)
            self.day_btn_vars.append(var)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=10)

        # Forecast labels
        self.temp_label = ttk.Label(right, text="--°C", font=("Segoe UI", 26, "bold"))
        self.temp_label.pack(anchor="w")

        self.cond_label = ttk.Label(right, text="", font=("Segoe UI", 12))
        self.cond_label.pack(anchor="w", pady=(2, 6))

        self.range_label = ttk.Label(right, text="", font=("Segoe UI", 10))
        self.range_label.pack(anchor="w")

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=10)

        # Mini next-days list
        ttk.Label(right, text="3-Day Snapshot", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 4))
        self.snapshot_box = tk.Text(right, height=6, width=30)
        self.snapshot_box.pack(fill="x", pady=4)
        self.snapshot_box.config(state="disabled")

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=10)

        # Small footer info
        self.info_label = ttk.Label(
            right,
            text="Mock data only.\nAnimations reflect each condition.",
            font=("Segoe UI", 8),
            foreground="#666666"
        )
        self.info_label.pack(anchor="w", pady=(4, 0))

    # ---------------- Logic helpers ---------------- #
    def _get_forecast_for(self, city):
        rows = [r for r in MOCK_FORECAST if r[0] == city]
        # ensure same order: Today, Tomorrow, Day After
        sorted_rows = sorted(rows, key=lambda r: self.day_names.index(r[1]) if r[1] in self.day_names else 99)
        return sorted_rows

    def _current_forecast_row(self):
        city = self.city_var.get()
        rows = self._get_forecast_for(city)
        if not rows:
            return None
        idx = min(self.current_day_index, len(rows)-1)
        return rows[idx]

    def _update_forecast_labels(self):
        row = self._current_forecast_row()
        if not row:
            self.temp_label.config(text="--°C")
            self.cond_label.config(text="")
            self.range_label.config(text="")
            return
        city, day, cond, temp, high, low = row
        self.temp_label.config(text=f"{temp}°C")
        cond_display = CONDITION_DISPLAY.get(cond, cond)
        self.cond_label.config(text=f"{day} · {cond_display}")
        self.range_label.config(text=f"High {high}°  •  Low {low}°")

        # Snapshot box
        forecast_rows = self._get_forecast_for(city)
        self.snapshot_box.config(state="normal")
        self.snapshot_box.delete("1.0", "end")
        for r in forecast_rows:
            _, d, c, t, hi, lo = r
            cd = CONDITION_DISPLAY.get(c, c)
            self.snapshot_box.insert("end", f"{d:<10} {t:>2}°  ({lo}°–{hi}°)  {cd}\n")
        self.snapshot_box.config(state="disabled")

        # highlight selected day button
        for i, child in enumerate(self.day_buttons_frame.winfo_children()):
            if i == self.current_day_index:
                child.configure(style="Selected.TButton")
            else:
                child.configure(style="TButton")

    def _apply_scene_from_current_forecast(self):
        row = self._current_forecast_row()
        if not row:
            return
        condition = row[2]
        # map some conditions to our scenes
        if condition == "Haze":
            scene_cond = "Haze"
        elif condition == "Storm":
            scene_cond = "Storm"
        elif condition == "Rainy":
            scene_cond = "Rainy"
        elif condition == "Cloudy":
            scene_cond = "Cloudy"
        elif condition == "Snow":
            scene_cond = "Snow"
        else:
            scene_cond = "Sunny"
        self.scene.set_condition(scene_cond)

    # ------------- Event handlers ------------- #
    def _set_day_index(self, idx):
        self.current_day_index = idx
        self._update_forecast_labels()
        self._apply_scene_from_current_forecast()

    def _on_city_change(self):
        self.current_day_index = 0
        self._update_forecast_labels()
        self._apply_scene_from_current_forecast()


# ------------------ Run app ------------------ #
if __name__ == "__main__":
    root = tk.Tk()

    # Slightly nicer button style
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    style.configure("Selected.TButton", background="#1976D2", foreground="white")
    style.map("Selected.TButton",
              background=[("active", "#1565C0")],
              foreground=[("active", "white")])

    app = WeatherWidgetApp(root)
    root.mainloop()







