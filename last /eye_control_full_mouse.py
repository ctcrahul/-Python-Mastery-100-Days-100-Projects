import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

pyautogui.FAILSAFE = False

mp_face = mp.solutions.face_mesh
face_mesh = mp_face.FaceMesh(refine_landmarks=True)

cam = cv2.VideoCapture(0)
screen_w, screen_h = pyautogui.size()

LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
IRIS = [474, 475, 476, 477]

blink_threshold = 0.004
blink_cooldown = 0.4
drag_threshold = 0.9

alpha = 0.25
smooth_x, smooth_y = 0, 0

last_blink = 0
blink_count = 0
blink_start = None
dragging = False

def iris_position(landmarks, w, h):
    x = int(np.mean([landmarks[i].x for i in IRIS]) * w)
    y = int(np.mean([landmarks[i].y for i in IRIS]) * h)
    return x, y

def eye_aspect_ratio(landmarks, eye):
    return abs(landmarks[eye[0]].y - landmarks[eye[1]].y)

print("Eye control active")
print("Blink = left click | Double blink = right click | Long blink = drag")
print("Look up/down = scroll | ESC to exit")


while True:
    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark

        iris_x, iris_y = iris_position(landmarks, w, h)

        screen_x = np.interp(iris_x, (0, w), (0, screen_w))
        screen_y = np.interp(iris_y, (0, h), (0, screen_h))

        smooth_x = alpha * screen_x + (1 - alpha) * smooth_x
        smooth_y = alpha * screen_y + (1 - alpha) * smooth_y

        pyautogui.moveTo(smooth_x, smooth_y, duration=0.01)
