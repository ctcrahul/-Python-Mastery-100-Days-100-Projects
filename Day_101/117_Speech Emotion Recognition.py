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
