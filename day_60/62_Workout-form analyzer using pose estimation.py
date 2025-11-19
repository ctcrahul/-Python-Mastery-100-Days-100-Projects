"""
Workout Form Analyzer using Pose Estimation
------------------------------------------
Features:
 - Real-time webcam feed (OpenCV)
 - MediaPipe Pose detection
 - Joint angle calculation:
       * Elbow Angle
       * Knee Angle
       * Shoulder-Hip-Knee Back Angle
 - Automatic rep counter for:
       * Bicep Curls
       * Squats
 - Basic form warnings based on joint angles
 - Clean on-screen overlay

Run:
    python workout_form_analyzer.py
"""

import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
# ----------------------------------------
# Helper: calculate angle between 3 points
# ----------------------------------------
def calc_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Mid point
    c = np.array(c)  # End point

    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
              np.arctan2(a[1]-b[1], a[0]-b[0])

    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180:
        angle = 360 - angle
    return angle

# ----------------------------------------
# Live Workout Analyzer
# ----------------------------------------
def start_analyzer():
    cap = cv2.VideoCapture(0)

    curl_count = 0
    curl_state = "down"

    squat_count = 0
    squat_state = "up"

    with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w, _ = frame.shape

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = pose.process(img_rgb)

            if result.pose_landmarks:
                lm = result.pose_landmarks.landmark


