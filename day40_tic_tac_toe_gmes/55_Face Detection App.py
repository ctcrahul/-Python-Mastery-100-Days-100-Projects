"""                                                                     Day = 55
                                                    
                                                              Face Detection App (single-file)
Dependencies:
    pip install opencv-python pillow numpy
Run:
    python face_detection_app.py

Features:
 - Real-time webcam preview with face detection (Haar cascades shipped with OpenCV)
 - Toggle detection on/off, take snapshots, save detected face crops
 - Switch between frontal face and LBP face detectors
 - Adjustable scaleFactor and minNeighbors for tuning detection sensitivity
 - Count faces and show bounding boxes & confidence-like visual
 - Uses Tkinter GUI, no external model files required (uses cv2.data.haarcascades)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
from PIL import Image, ImageTk
import threading
import time
import os
import numpy as np
import datetime


# -----------------------------
# Helper / Config
# -----------------------------
CASCADE_FILES = {
    "Haar-Frontal": "haarcascade_frontalface_default.xml",
    "Haar-Profile": "haarcascade_profileface.xml",
    "LBP-Face": "lbpcascade_frontalface.xml"
}

DEFAULT_CAMERA = 0
OUTPUT_DIR = "face_captures"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# -----------------------------
# Face Detector Class
# -----------------------------
class FaceDetector:
    def __init__(self, cascade_name="Haar-Frontal", scaleFactor=1.1, minNeighbors=5, minSize=(30,30)):
        self.cascade_name = cascade_name
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.minSize = minSize
        self._load_cascade()

    def _load_cascade(self):
        cascade_file = CASCADE_FILES.get(self.cascade_name, CASCADE_FILES["Haar-Frontal"])
        cascade_path = cv2.data.haarcascades + cascade_file
        if not os.path.exists(cascade_path):
            raise RuntimeError(f"Cascade file not found: {cascade_path}")
        # use CascadeClassifier for both Haar and LBP xmls
        self.detector = cv2.CascadeClassifier(cascade_path)

    def set_params(self, scaleFactor=None, minNeighbors=None, minSize=None):
        if scaleFactor is not None:
            self.scaleFactor = float(scaleFactor)
        if minNeighbors is not None:
            self.minNeighbors = int(minNeighbors)
        if minSize is not None:
            self.minSize = tuple(minSize)
        # no reload required for these params

    def set_cascade(self, cascade_name):
        self.cascade_name =


    def detect(self, gray_frame):
        # returns list of (x,y,w,h)
        faces = self.detector.detectMultiScale(
            gray_frame,
            scaleFactor=self.scaleFactor,
            minNeighbors=self.minNeighbors,
            minSize=self.minSize
        )
        return faces

# -----------------------------
# Main App (Tkinter)
# -----------------------------
class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection App")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


     # Video capture
        self.cam_index = DEFAULT_CAMERA
        self.cap = None
        self.video_thread = None
        self.running = False

        # Detector
        self.detector = FaceDetector()

        # GUI state
        self.detect_enabled = tk.BooleanVar(value=True)
        self.show_fps = tk.BooleanVar(value=True)
        self.cascade_var = tk.StringVar(value="Haar-Frontal")
        self.scale_var = tk.DoubleVar(value=1.1)
        self.nbrs_var = tk.IntVar(value=5)
        self.min_size_var = tk.IntVar(value=30)
        self.selected_face_index = None

        # last frame & faces
        self.last_color_frame = None
        self.last_faces = []

        self._build_ui()
        self.open_camera(self.cam_index)

    def _build_ui(self):
              # Top controls
        top = ttk.Frame(self.root)
        top.pack(side="top", fill="x", padx=8, pady=6)

        ttk.Label(top, text="Camera:").pack(side="left")
        self.cam_entry = ttk.Entry(top, width=5)
        self.cam_entry.insert(0, str(DEFAULT_CAMERA))
        self.cam_entry.pack(side="left", padx=(4, 10))

        ttk.Button(top, text="Open Camera", command=self._on_open_camera).pack(side="left", padx=4)
        ttk.Button(top, text="Close Camera", command=self._on_close_camera).pack(side="left", padx=4)

        ttk.Separator(top, orient="vertical").pack(side="left", fill="y", padx=8)

        ttk.Checkbutton(top, text="Enable Detection", variable=self.detect_enabled).pack(side="left", padx=6)
        ttk.Checkbutton(top, text="Show FPS", variable=self.show_fps).pack(side="left", padx=6)


          ttk.Label(params, text="Detector:").grid(row=0, column=0, sticky="w")
        cascade_menu = ttk.Combobox(params, textvariable=self.cascade_var, values=list(CASCADE_FILES.keys()), state="readonly", width=18)
        cascade_menu.grid(row=0, column=1, padx=6)
        ttk.Button(params, text="Apply Detector", command=self._apply_detector).grid(row=0, column=2, padx=6)

        ttk.Label(params, text="scaleFactor:").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Spinbox(params, from_=1.01, to=2.5, increment=0.01, textvariable=self.scale_var, width=8).grid(row=1, column=1, sticky="w")
        ttk.Label(params, text="minNeighbors:").grid(row=1, column=2, sticky="w", padx=(12,0))
        ttk.Spinbox(params, from_=1, to=20, textvariable=self.nbrs_var, width=6).grid(row=1, column=3, sticky="w")

        ttk.Label(params, text="minSize(px):").grid(row=1, column=4, sticky="w", padx=(12,0))
        ttk.Spinbox(params, from_=10, to=300, textvariable=self.min_size_var, width=6).grid(row=1, column=5, sticky="w")

        # Canvas area for video
        canvas_frame = ttk.Frame(se
                                 
        # Cascade selection & params
        params = ttk.Frame(self.root)
        params.pack(side="top", fill="x", padx=8, pady=6)
      
      

