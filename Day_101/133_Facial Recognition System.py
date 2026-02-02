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
def register_face(name, frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)

    if len(boxes) != 1:
        print("Error: Ensure exactly ONE face is visible.")
        return

    embedding = face_recognition.face_encodings(rgb, boxes)[0]
    face_db["names"].append(name)
    face_db["embeddings"].append(embedding)

    with open(DATA_FILE, "wb") as f:
        pickle.dump(face_db, f)

    print(f"[INFO] Face registered for {name}")

def recognize_faces(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)

    names = []

    for encoding in encodings:
        if len(face_db["embeddings"]) == 0:
            names.append("Unknown")
            continue

        distances = face_recognition.face_distance(
            face_db["embeddings"], encoding
        )
        min_dist = np.min(distances)
        best_match = np.argmin(distances)

        if min_dist < THRESHOLD:
            names.append(face_db["names"][best_match])
        else:
            names.append("Unknown")

    return boxes, names
