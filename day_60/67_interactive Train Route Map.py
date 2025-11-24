"""
Project 67: Interactive Train Route Map (Toy)
--------------------------------------------

Features:
 - Schematic train/metro map rendered on a Tkinter Canvas
 - Click on stations to set "From" and "To"
 - Or choose "From" and "To" from dropdowns
 - Shows shortest route (by number of stops) using BFS
 - Highlights the route path and stations
 - Displays number of stops and list of stations in order

Everything is in-memory (no real data); you can edit STATIONS and LINES
to reflect your own city/network.

Run:
    python train_route_map.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque


# --------------------------
# Network Data (Toy Example)
# --------------------------

# Station coordinates are on a 0–100 grid (we’ll scale to canvas)
STATIONS = [
    {"id": "JP1", "name": "North Yard",     "x": 10, "y": 10, "line": "Blue"},
    {"id": "JP2", "name": "Civil Lines",    "x": 25, "y": 20, "line": "Blue"},
    {"id": "JP3", "name": "Old City",       "x": 40, "y": 30, "line": "Blue"},
    {"id": "JP4", "name": "Central Jn",     "x": 55, "y": 40, "line": "Blue"},
    {"id": "JP5", "name": "Tech Park",      "x": 70, "y": 50, "line": "Blue"},
    {"id": "JP6", "name": "Campus East",    "x": 85, "y": 60, "line": "Blue"},

    {"id": "GR1", "name": "Lake View",      "x": 15, "y": 45, "line": "Green"},
    {"id": "GR2", "name": "Museum",         "x": 30, "y": 50, "line": "Green"},
    {"id": "GR3", "name": "Central Jn",     "x": 55, "y": 40, "line": "Green"},  # shared ID with JP4
    {"id": "GR4", "name": "Market Square",  "x": 65, "y": 28, "line": "Green"},
    {"id": "GR5", "name": "Airport",        "x": 80, "y": 15, "line": "Green"},

    {"id": "RD1", "name": "West End",       "x": 5,  "y": 70, "line": "Red"},
    {"id": "RD2", "name": "Stadium",        "x": 25, "y": 70, "line": "Red"},
    {"id": "RD3", "name": "Central Jn",     "x": 55, "y": 40, "line": "Red"},
    {"id": "RD4", "name": "IT Hub",         "x": 78, "y": 70, "line": "Red"},
    {"id": "RD5", "name": "South Terminal", "x": 92, "y": 82, "line": "Red"},
]

# Shared node: we want "Central Jn" to be a single logical station with multiple line colors.
# To keep it simple we’ll merge any stations that share same name as "Central Jn"
# For adjacency, we define lines as ordered station names, not IDs.

LINES = {
    "Blue":  {
        "color": "#2196F3",
        "stations": ["North Yard", "Civil Lines", "Old City", "Central Jn", "Tech Park", "Campus East"],
    },
    "Green": {
        "color": "#4CAF50",
        "stations": ["Lake View", "Museum", "Central Jn", "Market Square", "Airport"],
    },
    "Red":   {
        "color": "#F44336",
        "stations": ["West End", "Stadium", "Central Jn", "IT Hub", "South Terminal"],
    },
}


# --------------------------
# Data Structures
# --------------------------

class TrainNetwork:
    def __init__(self, stations, lines):
        # Merge by station name so shared interchanges are one logical node
        self.stations_by_name = {}
        for s in stations:
            name = s["name"]
            if name not in self.stations_by_name:
                self.stations_by_name[name] = {
                    "name": name,
                    "x": s["x"],
                    "y": s["y"],
                    "lines": {s["line"]},
                }
            else:
                # merge line info, keep average position (for simplicity)
                existing = self.stations_by_name[name]
                existing["x"] = (existing["x"] + s["x"]) / 2
                existing["y"] = (existing["y"] + s["y"]) / 2
                existing["lines"].add(s["line"])

        self.lines = lines
        self.adj = self._build_graph()

    def _build_graph(self):
        adj = {name: set() for name in self.stations_by_name.keys()}
        for line_name, line_info in self.lines.items():
            sts = line_info["stations"]
            for i in range(len(sts) - 1):
                a, b = sts[i], sts[i + 1]
                if a in adj and b in adj:
                    adj[a].add(b)
                    adj[b].add(a)
        return adj

    def all_station_names(self):
        return sorted(self.stations_by_name.keys())

    def neighbors(self, station_name):
        return self.adj.get(station_name, set())

    def shortest_path(self, start, end):
        if start not in self.adj or end not in self.adj:
            return None
        if start == end:
            return [start]
        visited = set()
        queue = deque([(start, [start])])
        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            if node in visited:
                continue
            visited.add(node)
            for nb in self.adj[node]:
                if nb not in visited:
                    queue.append((nb, path + [nb]))
        return None


# --------------------------
# GUI Application
# --------------------------

class TrainRouteMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Train Route Map (Toy)")
        self.root.geometry("1100x650")

        self.network = TrainNetwork(STATIONS, LINES)
        self.station_positions = self._build_positions()

        # selection state
        self.from_station = None
        self.to_station = None
        self.current_path = None

        # canvas drawing helpers
        self.canvas_margin = 40
        self.station_radius = 8
        self.canvas_station_items = {}  # station_name -> (circle_id, text_id)

        self._build_ui()
        self._draw_map()

    def _build_positions(self):
        # Map station_name -> (x_norm, y_norm) in [0, 100]
        pos = {}
        for name, data in self.network.stations_by_name.items():
            pos[name] = (data["x"], data["y"])
        return pos

    # ------------- UI Layout ------------- #
    def _build_ui(self):
        main = ttk.Frame(self.root, padding=8)
        main.pack(fill="both", expand=True)

        # left: canvas
        left = ttk.Frame(main)
        left.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(left, bg="#10151f", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<Motion>", self._on_canvas_hover)

        # right: controls
        right = ttk.Frame(main, width=320)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        ttk.Label(right, text="Train Route Planner", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

        # From / To selectors
        stations = self.network.all_station_names()

        ttk.Label(right, text="From").pack(anchor="w")
        self.from_var = tk.StringVar()
        self.from_combo = ttk.Combobox(right, values=stations, textvariable=self.from_var, state="readonly")
        self.from_combo.pack(fill="x", pady=2)

        ttk.Label(right, text="To").pack(anchor="w", pady=(6, 0))
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(right, values=stations, textvariable=self.to_var, state="readonly")
        self.to_combo.pack(fill="x", pady=2)

        btn_frame = ttk.Frame(right)
        btn_frame.pack(fill="x", pady=8)

        ttk.Button(btn_frame, text="Find Route", command=self._find_route).pack(side="left", expand=True, fill="x", padx=(0, 4))
        ttk.Button(btn_frame, text="Clear", command=self._clear_route).pack(side="left", expand=True, fill="x", padx=(4, 0))

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=8)

        # Route summary
        self.summary_label = ttk.Label(right, text="No route selected.", wraplength=280, justify="left")
        self.summary_label.pack(anchor="w", pady=4)

        ttk.Label(right, text="Route Stations:", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(8, 2))

        self.route_listbox = tk.Listbox(right, height=12)
        self.route_listbox.pack(fill="both", expand=True)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=8)

        self.hover_label = ttk.Label(right, text="Hint: Click stations on the map to set From/To.", foreground="#888")
        self.hover_label.pack(anchor="w", pady=(0, 4))

        self.status_label = ttk.Label(right, text="", foreground="#4CAF50")
        self.status_label.pack(anchor="w")

        # redraw on resize
        self.canvas.bind("<Configure>", lambda e: self._draw_map())

    # ------------- Map Drawing ------------- #
    def _draw_map(self):
        self.canvas.delete("all")
        self.canvas_station_items.clear()

        w = max(self.canvas.winfo_width(), 200)
        h = max(self.canvas.winfo_height(), 200)
        margin = self.canvas_margin
        usable_w = w - 2 * margin
        usable_h = h - 2 * margin

        # helper to scale positions
        def scale_pos(x_norm, y_norm):
            x = margin + (x_norm / 100.0) * usable_w
            y = margin + (y_norm / 100.0) * usable_h
            return x, y

        # draw grid (optional, faint)
        step = 20
        for i in range(0, 101, step):
            x1, y1 = scale_pos(i, 0)
            x2, y2 = scale_pos(i, 100)
            self.canvas.create_line(x1, y1, x2, y2, fill="#1b2333", width=1)
            x1, y1 = scale_pos(0, i)
            x2, y2 = scale_pos(100, i)
            self.canvas.create_line(x1, y1, x2, y2, fill="#1b2333", width=1)

        # draw lines (routes)
        for line_name, info in LINES.items():
            color = info["color"]
            sts = info["stations"]
            # build polyline
            points = []
            for name in sts:
                if name in self.station_positions:
                    x_norm, y_norm = self.station_positions[name]
                    x, y = scale_pos(x_norm, y_norm)
                    points.append((x, y))
            # draw line segments
            for i in range(len(points) - 1):
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=5, capstyle="round")

        # if route, overlay highlighted polyline
        if self.current_path and len(self.current_path) > 1:
            route_points = []
            for name in self.current_path:
                x_norm, y_norm = self.station_positions[name]
                x, y = scale_pos(x_norm, y_norm)
                route_points.append((x, y))
            for i in range(len(route_points) - 1):
                x1, y1 = route_points[i]
                x2, y2 = route_points[i + 1]
                self.canvas.create_line(x1, y1, x2, y2, fill="#FFEB3B", width=7, capstyle="round")

        # draw stations
        for name, (x_norm, y_norm) in self.station_positions.items():
            x, y = scale_pos(x_norm, y_norm)

            # highlight start/end differently
            fill = "#FFFFFF"
            outline = "#263238"
            r = self.station_radius
            if name == self.from_station:
                fill = "#4CAF50"
                outline = "#1B5E20"
                r = self.station_radius + 2
            elif name == self.to_station:
                fill = "#F44336"
                outline = "#B71C1C"
                r = self.station_radius + 2
            elif self.current_path and name in self.current_path:
                fill = "#FFEB3B"
                outline = "#FBC02D"

            circle_id = self.canvas.create_oval(
                x - r, y - r, x + r, y + r,
                fill=fill, outline=outline, width=2
            )
            text_id = self.canvas.create_text(
                x + 12, y - 10,
                text=name,
                anchor="w",
                fill="#CFD8DC",
                font=("Segoe UI", 9, "bold")
            )
            self.canvas_station_items[name] = (circle_id, text_id)

    # ------------- Event Handlers ------------- #
    def _find_route(self):
        start = self.from_var.get().strip()
        end = self.to_var.get().strip()
        if not start or not end:
            messagebox.showinfo("Select stations", "Please select both From and To stations.")
            return
        if start == end:
            messagebox.showinfo("Same station", "From and To are the same.")
            return
        path = self.network.shortest_path(start, end)
        if not path:
            messagebox.showwarning("No route", f"No route found between {start} and {end}.")
            return
        self.from_station = start
        self.to_station = end
        self.current_path = path
        self._update_route_display()

    def _clear_route(self):
        self.from_station = None
        self.to_station = None
        self.current_path = None
        self.from_var.set("")
        self.to_var.set("")
        self.route_listbox.delete(0, tk.END)
        self.summary_label.config(text="No route selected.")
        self.status_label.config(text="")
        self._draw_map()

    def _update_route_display(self):
        path = self.current_path
        if not path:
            return
        hops = len(path) - 1
        self.summary_label.config(
            text=f"Route from {path[0]} to {path[-1]}: {hops} stop(s)."
        )
        self.route_listbox.delete(0, tk.END)
        for i, st in enumerate(path):
            prefix = "▶ " if i == 0 else ("■ " if i == len(path) - 1 else "• ")
            self.route_listbox.insert(tk.END, f"{prefix}{st}")
        self.status_label.config(text="Route highlighted on map.")
        self._draw_map()

    def _on_canvas_click(self, event):
        # pick nearest station within radius*2
        clicked = self._find_nearest_station(event.x, event.y, max_dist=25)
        if not clicked:
            return
        name = clicked
        # selection logic: first click sets "from", second sets "to"
        if not self.from_station or (self.from_station and self.to_station):
            self.from_station = name
            self.to_station = None
            self.current_path = None
            self.from_var.set(name)
            self.to_var.set("")
            self.summary_label.config(text=f"From station: {name}. Choose destination.")
            self.route_listbox.delete(0, tk.END)
        else:
            self.to_station = name
            self.to_var.set(name)
            if self.from_station == self.to_station:
                self.summary_label.config(text="From and To are the same station.")
                self.current_path = [name]
                self._update_route_display()
            else:
                path = self.network.shortest_path(self.from_station, self.to_station)
                if not path:
                    messagebox.showwarning("No route", f"No route found between {self.from_station} and {self.to_station}.")
                    self.current_path = None
                else:
                    self.current_path = path
                    self._update_route_display()
        self._draw_map()

    def _on_canvas_hover(self, event):
        name = self._find_nearest_station(event.x, event.y, max_dist=15)
        if name:
            self.hover_label.config(text=f"Hover: {name}")
        else:
            self.hover_label.config(text="Hint: Click stations on the map to set From/To.")

    def _find_nearest_station(self, x, y, max_dist=20):
        # search by coordinates
        nearest = None
        nearest_d2 = max_dist * max_dist
        for name, (circle_id, _) in self.canvas_station_items.items():
            x1, y1, x2, y2 = self.canvas.coords(circle_id)
            cx = (x1 + x2) / 2
            cy = (y1 + y2) / 2
            dx = cx - x
            dy = cy - y
            d2 = dx*dx + dy*dy
            if d2 <= nearest_d2:
                nearest_d2 = d2
                nearest = name
        return nearest


# --------------------------
# Run
# --------------------------

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = TrainRouteMapApp(root)
    root.mainloop()
