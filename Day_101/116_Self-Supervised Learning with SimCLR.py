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
    image = tf.image.resize(image, (224, 224))
    return image

# -----------------------------
# CONTRASTIVE LOSS (NT-Xent)
# -----------------------------
def contrastive_loss(z1, z2, temperature=0.5):
    z1 = tf.math.l2_normalize(z1, axis=1)
    z2 = tf.math.l2_normalize(z2, axis=1)
