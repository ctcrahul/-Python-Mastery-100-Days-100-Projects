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
