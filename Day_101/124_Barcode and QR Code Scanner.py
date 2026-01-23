#pip install opencv-python
pip install pyzbar

import cv2
from pyzbar import pyzbar

def scan_codes(frame):
    decoded_objects = pyzbar.decode(frame)

    for obj in decoded_objects:
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(
                np.array([point for point in points], dtype=np.float32)
            )
            hull = list(map(tuple, np.squeeze(hull)))
        else:
            hull = points

        n = len(hull)
        for j in range(n):
            cv2.line(frame, hull[j], hull[(j + 1) % n], (0, 255, 0), 2)
