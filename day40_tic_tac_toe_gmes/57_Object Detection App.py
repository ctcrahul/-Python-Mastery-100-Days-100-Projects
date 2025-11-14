"""
Object Detection App (single-file)

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
        

