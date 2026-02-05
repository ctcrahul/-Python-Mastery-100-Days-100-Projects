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
