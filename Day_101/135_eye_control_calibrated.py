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
blink_cooldown = 1
last_blink = 0

alpha = 0.2  # smoothing factor
smooth_x, smooth_y = 0, 0

calibration_points = [
    (0.1, 0.1),
    (0.9, 0.1),
    (0.5, 0.5),
    (0.1, 0.9),
    (0.9, 0.9)
]

eye_points = []

def get_iris_position(landmarks, w, h):
    x = int(np.mean([landmarks[i].x for i in IRIS]) * w)
    y = int(np.mean([landmarks[i].y for i in IRIS]) * h)
    return x, y

def eye_aspect_ratio(landmarks, eye):
    return abs(landmarks[eye[0]].y - landmarks[eye[1]].y)

print("Calibration starting...")
print("Look at each red dot and press SPACE")

for target in calibration_points:
    while True:
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb)

        cx, cy = int(target[0] * w), int(target[1] * h)
        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), -1)
        cv2.putText(frame, "Press SPACE", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0].landmark
            iris = get_iris_position(landmarks, w, h)
            cv2.circle(frame, iris, 5, (0, 255, 0), -1)

        cv2.imshow("Calibration", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 32 and result.multi_face_landmarks:
            eye_points.append(iris)
            break

    time.sleep(0.5)

cv2.destroyWindow("Calibration")

eye_points = np.array(eye_points)
screen_points = np.array([
    (p[0] * screen_w, p[1] * screen_h)
    for p in calibration_points
])

M, _ = cv2.estimateAffine2D(eye_points, screen_points)

print("Calibration done. Eye control active.")

while True:
    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark
        iris_x, iris_y = get_iris_position(landmarks, w, h)

        eye_vec = np.array([[iris_x, iris_y, 1]])
        screen_pos = np.dot(M, eye_vec.T).flatten()

        smooth_x = alpha * screen_pos[0] + (1 - alpha) * smooth_x
        smooth_y = alpha * screen_pos[1] + (1 - alpha) * smooth_y

        pyautogui.moveTo(smooth_x, smooth_y, duration=0.01)

        ear = (
            eye_aspect_ratio(landmarks, LEFT_EYE) +
            eye_aspect_ratio(landmarks, RIGHT_EYE)
        ) / 2

        if ear < blink_threshold:
            now = time.time()
            if now - last_blink > blink_cooldown:
                pyautogui.click()
                last_blink = now

    cv2.imshow("Eye Controlled Laptop", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
cv2.destroyAllWindows()
