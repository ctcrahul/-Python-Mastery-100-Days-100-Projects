import cv2
import face_recognition
import numpy as np
import os
import pickle

DATA_FILE = "face_db.pkl"
THRESHOLD = 0.45  # lower = stricter matching

# Load existing face database
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "rb") as f:
        face_db = pickle.load(f)
else:
    face_db = {"names": [], "embeddings": []}
