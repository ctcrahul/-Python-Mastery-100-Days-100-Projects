# Image Classification using CNN
# Project Level: Real-world beginner → intermediate

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# -----------------------------
# CONFIG
# -----------------------------
IMG_SIZE = 128
BATCH_SIZE = 32
EPOCHS = 10
