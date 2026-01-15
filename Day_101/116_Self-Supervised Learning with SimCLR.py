# Self-Supervised Learning with SimCLR (Simplified)
# No labels. Representation learning only.

import tensorflow as tf
from tensorflow.keras import layers
import numpy as np


# -----------------------------
# DATA AUGMENTATION
# -----------------------------
def augment(image):
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_brightness(image, 0.2)
    image = tf.image.random_contrast(image, 0.8, 1.2)
