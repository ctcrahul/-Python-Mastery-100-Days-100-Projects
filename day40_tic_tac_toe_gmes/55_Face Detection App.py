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
        self.cascade_name = cascade_name
        self._load_cascade()

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

        # Cascade selection & params
        params = ttk.Frame(self.root)
        params.pack(side="top", fill="x", padx=8, pady=6)

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
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(side="top", fill="both", expand=True, padx=8, pady=6)
        self.video_label = ttk.Label(canvas_frame)
        self.video_label.pack(fill="both", expand=True)

        # Bottom controls
        bottom = ttk.Frame(self.root)
        bottom.pack(side="bottom", fill="x", padx=8, pady=8)

        ttk.Button(bottom, text="Snapshot (save frame)", command=self.take_snapshot).pack(side="left", padx=6)
        ttk.Button(bottom, text="Save Detected Faces", command=self.save_detected_faces).pack(side="left", padx=6)
        ttk.Button(bottom, text="Crop & Save Selected Face", command=self.save_selected_face).pack(side="left", padx=6)

        ttk.Button(bottom, text="Switch Camera", command=self.switch_camera).pack(side="left", padx=6)
        ttk.Button(bottom, text="Clear Output Folder", command=self.clear_output).pack(side="left", padx=6)

        # Info area
        info = ttk.Frame(self.root)
        info.pack(side="bottom", fill="x", padx=8, pady=(0,8))
        self.info_var = tk.StringVar(value="No camera opened.")
        ttk.Label(info, textvariable=self.info_var).pack(side="left")

    # -----------------------------
    # Camera control
    # -----------------------------
    def open_camera(self, index):
        self.close_camera()
        try:
            self.cap = cv2.VideoCapture(index, cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY)
            if not self.cap or not self.cap.isOpened():
                self.cap = None
                self.info_var.set(f"Unable to open camera {index}.")
                return False
            self.running = True
            self.video_thread = threading.Thread(target=self._video_loop, daemon=True)
            self.video_thread.start()
            self.info_var.set(f"Camera {index} opened.")
            return True
        except Exception as e:
            self.cap = None
            self.info_var.set(f"Failed to open camera: {e}")
            return False

    def close_camera(self):
        self.running = False
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
        self.cap = None
        self.info_var.set("Camera closed.")

    def _on_open_camera(self):
        try:
            idx = int(self.cam_entry.get().strip())
        except Exception:
            messagebox.showwarning("Input", "Camera index must be integer.")
            return
        self.cam_index = idx
        self.open_camera(idx)

    def _on_close_camera(self):
        self.close_camera()

    def switch_camera(self):
        # try next index
        next_idx = (self.cam_index + 1) % 4  # cycle through 0..3
        self.cam_entry.delete(0, tk.END)
        self.cam_entry.insert(0, str(next_idx))
        self._on_open_camera()

    # -----------------------------
    # Video loop & detection
    # -----------------------------
    def _video_loop(self):
        prev_time = time.time()
        fps = 0.0
        while self.running and self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                time.sleep(0.05)
                continue

            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            display_frame = color_frame.copy()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            self.detector.set_params(scaleFactor=self.scale_var.get(), minNeighbors=self.nbrs_var.get(), minSize=(self.min_size_var.get(), self.min_size_var.get()))

            faces = []
            if self.detect_enabled.get():
                faces = self.detector.detect(gray)
                # faces: array-like of x,y,w,h

            # draw boxes
            self.last_faces = faces
            self.last_color_frame = display_frame

            for i, (x,y,w,h) in enumerate(faces):
                # color changes by index
                color = (255, 0, 0) if i != self.selected_face_index else (0, 255, 0)
                cv2.rectangle(display_frame, (x,y), (x+w, y+h), color, 2)
                # label with index
                cv2.putText(display_frame, f"#{i}", (x, y-8), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # overlay face count
            cv2.putText(display_frame, f"Faces: {len(faces)}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,0), 2)

            # fps calc
            now = time.time()
            dt = now - prev_time
            prev_time = now
            if dt > 0:
                fps = 0.9*fps + 0.1*(1.0/dt)
            if self.show_fps.get():
                cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

            # convert to ImageTk and display
            img = Image.fromarray(display_frame)
            imgtk = ImageTk.PhotoImage(image=img)
            # need to save reference to avoid GC
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

            # small sleep to reduce CPU use
            time.sleep(0.01)

    # -----------------------------
    # Actions: snapshot & save faces
    # -----------------------------
    def take_snapshot(self):
        if self.last_color_frame is None:
            messagebox.showinfo("No frame", "No video frame available to snapshot.")
            return
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(OUTPUT_DIR, f"snapshot_{ts}.png")
        img_bgr = cv2.cvtColor(self.last_color_frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite(fname, img_bgr)
        messagebox.showinfo("Saved", f"Snapshot saved: {fname}")
        self.info_var.set(f"Saved snapshot: {fname}")

    def save_detected_faces(self):
        if self.last_color_frame is None:
            messagebox.showinfo("No frame", "No video frame available.")
            return
        if len(self.last_faces) == 0:
            messagebox.showinfo("No faces", "No faces detected in current frame.")
            return
        saved = []
        for i, (x,y,w,h) in enumerate(self.last_faces):
            crop = self.last_color_frame[y:y+h, x:x+w]
            if crop.size == 0:
                continue
            ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            fname = os.path.join(OUTPUT_DIR, f"face_{i}_{ts}.png")
            cv2.imwrite(fname, cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
            saved.append(fname)
        messagebox.showinfo("Saved", f"Saved {len(saved)} faces to {OUTPUT_DIR}")
        self.info_var.set(f"Saved {len(saved)} faces.")

    def save_selected_face(self):
        if self.last_color_frame is None:
            messagebox.showinfo("No frame", "No video frame available.")
            return
        if not self.last_faces:
            messagebox.showinfo("No faces", "No faces detected.")
            return
        # if user hasn't selected an index, take the first
        idx = self.selected_face_index if self.selected_face_index is not None else 0
        if idx < 0 or idx >= len(self.last_faces):
            messagebox.showwarning("Index", "Selected face index out of range.")
            return
        x,y,w,h = self.last_faces[idx]
        crop = self.last_color_frame[y:y+h, x:x+w]
        if crop.size == 0:
            messagebox.showinfo("Empty", "Selected crop is empty.")
            return
        ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(OUTPUT_DIR, f"face_selected_{idx}_{ts}.png")
        cv2.imwrite(fname, cv2.cvtColor(crop, cv2.COLOR_RGB2BGR))
        messagebox.showinfo("Saved", f"Saved selected face to {fname}")
        self.info_var.set(f"Saved selected face: {fname}")

    def clear_output(self):
        if messagebox.askyesno("Confirm", f"Delete all files in {OUTPUT_DIR}?"):
            count = 0
            for fname in os.listdir(OUTPUT_DIR):
                try:
                    os.remove(os.path.join(OUTPUT_DIR, fname))
                    count += 1
                except Exception:
                    pass
            messagebox.showinfo("Cleared", f"Removed {count} files.")
            self.info_var.set(f"Cleared {count} files from {OUTPUT_DIR}.")

    # -----------------------------
    # Apply detector params
    # -----------------------------
    def _apply_detector(self):
        try:
            sf = float(self.scale_var.get())
            mn = int(self.nbrs_var.get())
            ms = int(self.min_size_var.get())
        except Exception:
            messagebox.showwarning("Params", "Invalid detector parameters.")
            return
        self.detector.set_params(scaleFactor=sf, minNeighbors=mn, minSize=(ms, ms))
        # change cascade if needed
        sel = self.cascade_var.get()
        if sel != self.detector.cascade_name:
            try:
                self.detector.set_cascade(sel)
            except Exception as e:
                messagebox.showerror("Cascade", f"Failed to load cascade: {e}")
                return
        messagebox.showinfo("Applied", "Detector parameters updated.")

    # -----------------------------
    # Shutdown
    # -----------------------------
    def on_close(self):
        self.running = False
        # allow thread to stop
        time.sleep(0.2)
        try:
            if self.cap and self.cap.isOpened():
                self.cap.release()
        except Exception:
            pass
        self.root.destroy()

# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app = FaceDetectionApp(root)
    root.mainloop()

#===========================================================================================================================================================================
                                                         Thanks for visting keep supporting us...
#===========================================================================================================================================================================
          
