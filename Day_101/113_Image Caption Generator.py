# Image Caption Generator (Inference Pipeline)
# Multimodal AI: Vision + Language

import tensorflow as tf
import numpy as np
from PIL import Image

# -----------------------------
# LOAD CNN (Feature Extractor)
# -----------------------------
cnn = tf.keras.applications.InceptionV3(
    weights="imagenet",
    include_top=False,
    pooling="avg"
)
