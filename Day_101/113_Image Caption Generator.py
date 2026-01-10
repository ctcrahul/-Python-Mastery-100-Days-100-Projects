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
# -----------------------------
# IMAGE PREPROCESSING
# -----------------------------
def preprocess_image(path):
    img = Image.open(path).resize((299, 299))
    img = np.array(img)
    img = tf.keras.applications.inception_v3.preprocess_input(img)
    return np.expand_dims(img, axis=0)

# -----------------------------
# DUMMY VOCAB (for demo)
# -----------------------------
idx_to_word = {
    0: "<start>",
    1: "a",
    2: "dog",
    3: "on",
    4: "grass",
    5: "<end>"
}
# -----------------------------
# SIMPLE DECODER (SIMULATED)
# -----------------------------
def generate_caption(features):
    # In real systems, this is an LSTM loop
    # Here we simulate output for learning clarity
    return "a dog on grass"

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    image_path = "sample.jpg"
