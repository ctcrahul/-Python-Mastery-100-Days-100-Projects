"""                                                           Day = 57
                                                               
                                                        Object Detection App 

Dependencies:
    pip install opencv-python pillow numpy requests

What this does:
 - Uses MobileNet-SSD (Caffe) model for real-time object detection on webcam or video file.
 - If model files are missing, the script downloads them automatically.
 - Tkinter GUI to start/stop detection, adjust confidence threshold, switch camera, take snapshots,
   save detected object crops, and export detection log to CSV.
 - Draws bounding boxes, labels and confidence scores on video frames.

Run:
    python object_detection_app.py
"""
import os
import sys
import time
import threading
import csv
import urllib.request
from urllib.error import URLError, HTTPError
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime

# ---------------------------
# Model files & download URLs
# ---------------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

PROTOTXT_URL = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.prototxt"
CAFFEMODEL_URL = "https://github.com/chuanqi305/MobileNet-SSD/raw/master/MobileNetSSD_deploy.caffemodel"
PROTOTXT_PATH = os.path.join(MODEL_DIR, "MobileNetSSD_deploy.prototxt")
CAFFEMODEL_PATH = os.path.join(MODEL_DIR, "MobileNetSSD_deploy.caffemodel")

# ---------------------------
# Class labels for MobileNet-SSD (VOC)
# ---------------------------
CLASS_NAMES = [
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair",
    "cow", "diningtable", "dog", "horse", "motorbike",
    "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"
]

OUTPUT_DIR = os.path.join(BASE_DIR, "detections_output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ---------------------------
# Utilities: download model files if missing
# ---------------------------
def download_file(url, dest_path, show_progress=True):
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 100:
        return
    try:
        def _report(block_num, block_size, total_size):
            if show_progress:
                downloaded = block_num * block_size
                pct = min(100, int(downloaded * 100 / total_size)) if total_size > 0 else 0
                sys.stdout.write(f"\rDownloading {os.path.basename(dest_path)}... {pct}%")
                sys.stdout.flush()
        urllib.request.urlretrieve(url, dest_path, _report)
        if show_progress:
            print()
    except (URLError, HTTPError) as e:
        raise RuntimeError(f"Failed to download {url}: {e}")

def ensure_model_files():
    try:
        download_file(PROTOTXT_URL, PROTOTXT_PATH)
        download_file(CAFFEMODEL_URL, CAFFEMODEL_PATH)
    except Exception as e:
        raise RuntimeError(f"Model download failed: {e}")

# ---------------------------
# Object Detector wrapper
# ---------------------------
class MobileNetSSDDetector:
    def __init__(self, prototxt=PROTOTXT_PATH, model=CAFFEMODEL_PATH, conf_threshold=0.5):
        ensure_model_files()
        self.net = cv2.dnn.readNetFromCaffe(prototxt, model)
        self.conf_threshold = conf_threshold

    def set_confidence(self, val):
        self.conf_threshold = float(val)

    def detect(self, frame):
        """
        frame: BGR image (numpy array)
        returns: list of dicts: {class_id, class_name, confidence, box: (x1,y1,x2,y2)}
        """
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
                                     0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        results = []
        for i in range(detections.shape[2]):
            conf = float(detections[0, 0, i, 2])
            if conf < self.conf_threshold:
                continue
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype("int")
            # clamp
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w - 1, x2), min(h - 1, y2)
            results.append({
                "class_id": idx,
                "class_name": CLASS_NAMES[idx] if idx < len(CLASS_NAMES) else str(idx),
                "confidence": conf,
                "box": (x1, y1, x2, y2)
            })
        return results

# ---------------------------
# Tkinter App
# ---------------------------
class ObjectDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Object Detection App - MobileNet-SSD")
        self.root.geometry("1100x700")
        self.root.resizable(True, True)

        # Detector (lazy init)
        self.detector = None
        self.conf_threshold = tk.DoubleVar(value=0.5)

        # Video capture state
        self.cap = None
        self.cam_index = 0
        self.running = False
        self.video_thread = None
        self.frame = None
        self.display_image = None

        # Detection log (for CSV)
        self.detection_log = []  # each entry: dict with time,class,conf,box,imagefile(optional)

        self._build_ui()

    def _build_ui(self):
        # Top controls
        top = ttk.Frame(self.root)
        top.pack(side="top", fill="x", padx=8, pady=6)

        ttk.Label(top, text="Camera index:").pack(side="left")
        self.cam_entry = ttk.Entry(top, width=5)
        self.cam_entry.insert(0, "0")
        self.cam_entry.pack(side="left", padx=4)

        ttk.Button(top, text="Open Camera", command=self.open_camera).pack(side="left", padx=4)
        ttk.Button(top, text="Open Video File", command=self.open_video_file).pack(side="left", padx=4)
        ttk.Button(top, text="Close Video", command=self.close_camera).pack(side="left", padx=4)

        ttk.Separator(top, orient="vertical").pack(side="left", fill="y", padx=8)

        ttk.Label(top, text="Confidence:").pack(side="left", padx=(8,2))
        self.conf_slider = ttk.Scale(top, from_=0.1, to=0.95, orient="horizontal", variable=self.conf_threshold, command=self._on_conf_change)
        self.conf_slider.pack(side="left", padx=4, ipadx=50)

        ttk.Button(top, text="Start Detection", command=self.start_detection).pack(side="left", padx=8)
        ttk.Button(top, text="Stop Detection", command=self.stop_detection).pack(side="left", padx=4)
        ttk.Button(top, text="Snapshot", command=self.take_snapshot).pack(side="left", padx=4)
        ttk.Button(top, text="Save Detections CSV", command=self.save_csv).pack(side="left", padx=4)
        ttk.Button(top, text="Save Crops", command=self.save_crops).pack(side="left", padx=4)

        # Video display
        display_frame = ttk.Frame(self.root)
        display_frame.pack(fill="both", expand=True, padx=8, pady=6)
        self.video_label = ttk.Label(display_frame)
        self.video_label.pack(fill="both", expand=True)

        # Right panel: options & log
        side = ttk.Frame(self.root, width=320)
        side.pack(side="right", fill="y", padx=8, pady=6)

        # Model / status
        model_fr = ttk.LabelFrame(side, text="Model & Status", padding=6)
        model_fr.pack(fill="x", pady=6)
        ttk.Button(model_fr, text="Load / Ensure Model", command=self.load_model).pack(fill="x", pady=4)
        self.status_var = tk.StringVar(value="Model not loaded.")
        ttk.Label(model_fr, textvariable=self.status_var, wraplength=280).pack(anchor="w")

        # Quick filter: show only selected class
        filter_fr = ttk.LabelFrame(side, text="Filter & Control", padding=6)
        filter_fr.pack(fill="x", pady=6)
        ttk.Label(filter_fr, text="Show only class (optional)").pack(anchor="w")
        self.filter_var = tk.StringVar(value="")
        self.filter_entry = ttk.Entry(filter_fr, textvariable=self.filter_var)
        self.filter_entry.pack(fill="x", pady=4)

        # Log
        log_fr = ttk.LabelFrame(side, text="Detection Log (session)", padding=6)
        log_fr.pack(fill="both", expand=True, pady=6)
        self.log_box = tk.Listbox(log_fr, height=20)
        self.log_box.pack(side="left", fill="both", expand=True)
        log_scroll = ttk.Scrollbar(log_fr, orient="vertical", command=self.log_box.yview)
        self.log_box.configure(yscrollcommand=log_scroll.set)
        log_scroll.pack(side="right", fill="y")

        # Footer
        footer = ttk.Frame(self.root)
        footer.pack(side="bottom", fill="x", padx=8, pady=6)
        self.info_var = tk.StringVar(value="Ready.")
        ttk.Label(footer, textvariable=self.info_var, relief="sunken", anchor="w").pack(fill="x")

    # ---------------------------
    # Model loading
    # ---------------------------
    def load_model(self):
        self.info_var.set("Ensuring model files... (may download ~16MB)")
        self.root.update_idletasks()
        try:
            ensure_model_files()
            self.detector = MobileNetSSDDetector(conf_threshold=self.conf_threshold.get())
            self.status_var.set("MobileNet-SSD loaded.")
            self.info_var.set("Model loaded. Ready.")
        except Exception as e:
            messagebox.showerror("Model error", str(e))
            self.status_var.set("Model load failed.")
            self.info_var.set("Model load failed.")

    def _on_conf_change(self, val):
        if self.detector:
            self.detector.set_confidence(float(val))

    # ---------------------------
    # Video control
    # ---------------------------
    def open_camera(self):
        try:
            idx = int(self.cam_entry.get().strip())
        except Exception:
            messagebox.showwarning("Input", "Camera index must be an integer.")
            return
        self.close_camera()
        self.cap = cv2.VideoCapture(idx, cv2.CAP_DSHOW if os.name == "nt" else cv2.CAP_ANY)
        if not self.cap or not self.cap.isOpened():
            self.cap = None
            messagebox.showerror("Camera", f"Unable to open camera {idx}.")
            return
        self.cam_index = idx
        self.info_var.set(f"Camera {idx} opened.")
        self._start_video_loop()

    def open_video_file(self):
        path = filedialog.askopenfilename(title="Open video file", filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv"), ("All files","*.*")])
        if not path:
            return
        self.close_camera()
        self.cap = cv2.VideoCapture(path)
        if not self.cap or not self.cap.isOpened():
            self.cap = None
            messagebox.showerror("Video", f"Unable to open video file.")
            return
        self.info_var.set(f"Video opened: {os.path.basename(path)}")
        self._start_video_loop()

    def close_camera(self):
        self.stop_detection()
        if self.cap:
            try:
                self.cap.release()
            except Exception:
                pass
        self.cap = None
        self.info_var.set("Camera/Video closed.")
        # clear frame display
        self.video_label.configure(image="")

    def _start_video_loop(self):
        if self.video_thread and self.video_thread.is_alive():
            return
        self.running = True
        self.video_thread = threading.Thread(target=self._video_loop, daemon=True)
        self.video_thread.start()

    def _video_loop(self):
        fps_time = time.time()
        while self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            self.frame = frame.copy()
            # detection visualization only when detection is running and model loaded
            if self.detector and self.running and getattr(self, "detecting", False):
                try:
                    results = self.detector.detect(frame)
                except Exception as e:
                    self.info_var.set(f"Detection error: {e}")
                    results = []
                # apply filter
                filter_text = self.filter_var.get().strip().lower()
                display = frame.copy()
                for r in results:
                    cls = r["class_name"]
                    if filter_text and filter_text not in cls.lower():
                        continue
                    x1, y1, x2, y2 = r["box"]
                    conf = r["confidence"]
                    label = f"{cls}: {conf:.2f}"
                    # draw box and label
                    cv2.rectangle(display, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    y_label = y1 - 10 if y1 - 10 > 10 else y1 + 10
                    cv2.putText(display, label, (x1, y_label), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
                    # log detection
                    now = datetime.utcnow().isoformat()
                    log_entry = {"time": now, "class": cls, "confidence": float(conf), "box": (int(x1),int(y1),int(x2),int(y2))}
                    self.detection_log.append(log_entry)
                    # update listbox - keep latest 500 for speed
                    self.root.after(0, lambda e=log_entry: self._append_log(e))
                # fps overlay
                if time.time() - fps_time > 0:
                    fps_time = time.time()
                # convert display
                display_rgb = cv2.cvtColor(display, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(display_rgb)
            else:
                display_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(display_rgb)
            # resize display to fit label while maintaining aspect ratio
            w_label = self.video_label.winfo_width() or 800
            h_label = self.video_label.winfo_height() or 600
            im.thumbnail((w_label, h_label))
            imgtk = ImageTk.PhotoImage(image=im)
            self.display_image = imgtk  # keep reference
            self.video_label.configure(image=imgtk)
            # small sleep to be cooperative
            time.sleep(0.01)
        # video ended or closed
        self.running = False
        self.detecting = False
        self.info_var.set("Video stream ended or closed.")

    # ---------------------------
    # Detection control
    # ---------------------------
    def start_detection(self):
        if not self.cap:
            messagebox.showwarning("No video", "Open a camera or video file first.")
            return
        if not self.detector:
            # attempt to load
            try:
                self.load_model()
            except Exception as e:
                messagebox.showerror("Model", f"Unable to load model: {e}")
                return
        self.detecting = True
        self.info_var.set("Detection started.")
        # clear previous log
        self.detection_log.clear()
        self.log_box.delete(0, tk.END)

    def stop_detection(self):
        self.detecting = False
        self.info_var.set("Detection stopped.")

    # ---------------------------
    # Actions: snapshot, save crops, save csv
    # ---------------------------
    def take_snapshot(self):
        if self.frame is None:
            messagebox.showinfo("No frame", "No frame available to snapshot.")
            return
        ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        fname = os.path.join(OUTPUT_DIR, f"snapshot_{ts}.jpg")
        cv2.imwrite(fname, self.frame)
        messagebox.showinfo("Saved", f"Snapshot saved: {fname}")
        self.info_var.set(f"Snapshot saved: {fname}")

    def save_crops(self):
        if not self.detection_log:
            messagebox.showinfo("No detections", "No detections recorded this session.")
            return
        saved = 0
        # for each log entry, try to crop from the latest frame (best-effort)
        frame = self.frame
        if frame is None:
            messagebox.showinfo("No frame", "No video frame available.")
            return
        for i, entry in enumerate(self.detection_log[-200:]):  # limit to last 200
            x1,y1,x2,y2 = entry["box"]
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue
            ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            cls = entry["class"]
            fname = os.path.join(OUTPUT_DIR, f"crop_{i}_{cls}_{ts}.jpg")
            cv2.imwrite(fname, crop)
            saved += 1
        messagebox.showinfo("Saved", f"Saved {saved} crops to {OUTPUT_DIR}")
        self.info_var.set(f"Saved {saved} crops.")

    def save_csv(self):
        if not self.detection_log:
            messagebox.showinfo("No data", "No detections this session.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files","*.csv")], initialfile=f"detections_{int(time.time())}.csv")
        if not path:
            return
        # write CSV
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["time","class","confidence","x1","y1","x2","y2"])
            for e in self.detection_log:
                t = e["time"]
                cls = e["class"]
                conf = e["confidence"]
                x1,y1,x2,y2 = e["box"]
                writer.writerow([t, cls, conf, x1, y1, x2, y2])
        messagebox.showinfo("Saved", f"Detections exported to {path}")
        self.info_var.set(f"Saved CSV: {path}")

    def _append_log(self, entry):
        text = f"{entry['time'].split('T')[0]} {entry['time'].split('T')[1][:8]} - {entry['class']} ({entry['confidence']:.2f})"
        self.log_box.insert(0, text)
        # cap length to 1000
        if self.log_box.size() > 1000:
            self.log_box.delete(1000, tk.END)

# ---------------------------
# Entry point
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectDetectionApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: (setattr(app, "running", False), app.close_camera(), root.destroy()))
    root.mainloop()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

