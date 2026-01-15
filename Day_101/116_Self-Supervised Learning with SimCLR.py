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

    logits = tf.matmul(z1, z2, transpose_b=True) / temperature
    labels = tf.range(tf.shape(z1)[0])
    loss = tf.keras.losses.sparse_categorical_crossentropy(
        labels, logits, from_logits=True
    )
    return tf.reduce_mean(loss)

# -----------------------------
# ENCODER NETWORK
# -----------------------------
def build_encoder():
    base = tf.keras.applications.ResNet50(
        include_top=False,
        weights=None,
        pooling="avg"
    )
    projection = tf.keras.Sequential([
        layers.Dense(256, activation="relu"),
        layers.Dense(128)
    ])
    return base, projection

# -----------------------------
# TRAINING LOOP
# -----------------------------
def train(images, epochs=5):
    encoder, projector = build_encoder()
    optimizer = tf.keras.optimizers.Adam(1e-3)

    for epoch in range(epochs):
        for batch in images:
            with tf.GradientTape() as tape:
                x1 = augment(batch)
                x2 = augment(batch)

                h1 = encoder(x1, training=True)
                h2 = encoder(x2, training=True)

                z1 = projector(h1)
                z2 = projector(h2)

                loss = contrastive_loss(z1, z2)

            grads = tape.gradient(
                loss, encoder.trainable_weights + projector.trainable_weights
            )
            optimizer.apply_gradients(zip(
                grads, encoder.trainable_weights + projector.trainable_weights
            ))

        print(f"Epoch {epoch+1} | Loss: {loss.numpy():.4f}")

# -----------------------------
# DUMMY DATA (REPLACE WITH REAL IMAGES)
# -----------------------------
dummy_images = tf.random.uniform((32, 224, 224, 3))

if __name__ == "__main__":
    dataset = tf.data.Dataset.from_tensor_slices(dummy_images).batch(8)
    train(dataset)
