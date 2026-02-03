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


blink_threshold = 0.004
blink_cooldown = 1
last_blink_time = 0

LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
IRIS = [474, 475, 476, 477]

def eye_aspect_ratio(landmarks, eye):
    left = landmarks[eye[0]]
    right = landmarks[eye[1]]
    return abs(left.y - right.y)

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

        iris_x = int(np.mean([landmarks[i].x for i in IRIS]) * w)
        iris_y = int(np.mean([landmarks[i].y for i in IRIS]) * h)

        screen_x = np.interp(iris_x, (0, w), (0, screen_w))
        screen_y = np.interp(iris_y, (0, h), (0, screen_h))

        pyautogui.moveTo(screen_x, screen_y, duration=0.05)

        left_ear = eye_aspect_ratio(landmarks, LEFT_EYE)
        right_ear = eye_aspect_ratio(landmarks, RIGHT_EYE)
        ear = (left_ear + right_ear) / 2

        if ear < blink_threshold:
          current_time = time.time()
            if current_time - last_blink_time > blink_cooldown:
                pyautogui.click()
                last_blink_time = current_time

        cv2.circle(frame, (iris_x, iris_y), 4, (0, 255, 0), -1)

    cv2.imshow("Eye Controlled Laptop", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
