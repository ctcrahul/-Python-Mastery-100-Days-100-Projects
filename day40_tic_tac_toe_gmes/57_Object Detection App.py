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
