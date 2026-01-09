# YOLO Object Detection - Real Time
# Uses YOLOv8 (modern, clean, fast)

import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")  # nano version (fast)

cap = cv2.VideoCapture(0)
