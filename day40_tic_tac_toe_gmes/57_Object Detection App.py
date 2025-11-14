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



