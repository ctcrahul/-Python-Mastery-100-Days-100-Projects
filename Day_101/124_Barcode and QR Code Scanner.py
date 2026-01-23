#pip install opencv-python
pip install pyzbar

import cv2
from pyzbar import pyzbar

def scan_codes(frame):
    decoded_objects = pyzbar.decode(frame)

    for obj in decoded_objects:
        points = obj.polygon
        if len(points) > 4:
