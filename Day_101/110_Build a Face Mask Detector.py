import cv2
import tensorflow as tf
import numpy as np

# Load trained mask classifier
model = tf.keras.models.load_model("model.h5")

# Load OpenCV face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cap = cv2.VideoCapture(0)

IMG_SIZE = 128
