# YOLO Object Detection - Real Time
# Uses YOLOv8 (modern, clean, fast)

import cv2
from ultralytics import YOLO

# Load YOLO model
model = YOLO("yolov8n.pt")  # nano version (fast)

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Run detection
    results = model(frame, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = round(float(box.conf[0]), 2)
            cls = int(box.cls[0])
            label = model.names[cls]
