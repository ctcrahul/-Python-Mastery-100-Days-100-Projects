import cv2
import numpy as np
from tensorflow.keras.models import load_model


# Load face detector
face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


# Load trained emotion model
classifier = load_model("emotion_model.hdf5")


emotion_labels = [
    "Angry",
    "Disgust",
    "Fear",
    "Happy",
    "Sad",
    "Surprise",
    "Neutral"
]


# Start webcam
cap = cv2.VideoCapture(0)
