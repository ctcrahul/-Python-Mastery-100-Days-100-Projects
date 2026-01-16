# Speech Emotion Recognition
# Audio Classification using MFCC + Neural Network

import os
import librosa
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical
# -----------------------------
# FEATURE EXTRACTION
# -----------------------------
def extract_mfcc(file_path):
    audio, sr = librosa.load(file_path, duration=3, offset=0.5)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=40)
    return np.mean(mfcc.T, axis=0)

# -----------------------------
# LOAD DATASET
# -----------------------------
DATASET_PATH = "dataset"  # folder with emotion subfolders

X, y = [], []
for emotion in os.listdir(DATASET_PATH):
    emotion_path = os.path.join(DATASET_PATH, emotion)
    if not os.path.isdir(emotion_path):
        continue

    for file in os.listdir(emotion_path):
        if file.endswith(".wav"):
            features = extract_mfcc(os.path.join(emotion_path, file))
            X.append(features)
            y.append(emotion)

X = np.array(X)
y = np.array(y)
# -----------------------------
# ENCODE LABELS
# -----------------------------
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)
y_categorical = to_categorical(y_encoded)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_categorical, test_size=0.2, random_state=42
)

# -----------------------------
# MODEL
# -----------------------------
model = Sequential([
    Dense(256, activation="relu", input_shape=(40,)),
    Dropout(0.3),
    Dense(128, activation="relu"),
    Dropout(0.3),
    Dense(y_categorical.shape[1], activation="softmax")
])

model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

# -----------------------------
# TRAIN
# -----------------------------
model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=32,
    validation_data=(X_test, y_test)
)

model.save("speech_emotion_model.h5"
