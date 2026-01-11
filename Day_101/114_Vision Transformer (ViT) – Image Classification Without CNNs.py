# Vision Transformer (ViT) Image Classification
# Modern CV without CNNs

import tensorflow as tf
import tensorflow_addons as tfa
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# -----------------------------
# CONFIG
# -----------------------------
IMG_SIZE = 224
PATCH_SIZE = 16
NUM_CLASSES = 2
BATCH_SIZE = 16
EPOCHS = 5
