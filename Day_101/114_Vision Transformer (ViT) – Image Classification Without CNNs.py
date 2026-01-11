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

TRAIN_DIR = "dataset/train"
TEST_DIR = "dataset/test"

# -----------------------------
# DATA PIPELINE
# -----------------------------
datagen = ImageDataGenerator(rescale=1./255)

train_data = datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

test_data = datagen.flow_from_directory(
    TEST_DIR,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical"
)

# -----------------------------
# PATCH EMBEDDING
# -----------------------------
class PatchEmbedding(layers.Layer):
    def __init__(self):
        super().__init__()
        self.projection = layers.Conv2D(
            filters=64,
            kernel_size=PATCH_SIZE,
            strides=PATCH_SIZE
        )

    def call(self, x):
        x = self.projection(x)
        x = tf.reshape(x, (tf.shape(x)[0], -1, x.shape[-1]))
        return x

# -----------------------------
# TRANSFORMER BLOCK
# -----------------------------
def transformer_block(x):
    attn = layers.MultiHeadAttention(num_heads=4, key_dim=64)(x, x)
    x = layers.Add()([x, attn])
    x = layers.LayerNormalization()(x)

    mlp = layers.Dense(128, activation="relu")(x)
    mlp = layers.Dense(64)(mlp)
    x = layers.Add()([x, mlp])
    x = layers.LayerNormalization()(x)
    return x

# -----------------------------
# BUILD MODEL
# -----------------------------
inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))
x = PatchEmbedding()(inputs)

for _ in range(4):
    x = transformer_block(x)

x = layers.GlobalAveragePooling1D()(x)
outputs = layers.Dense(NUM_CLASSES, activation="softmax")(x)

model = tf.keras.Model(inputs, outputs)

# -----------------------------
# COMPILE & TRAIN
# -----------------------------
model.compile(
    optimizer=tfa.optimizers.AdamW(learning_rate=1e-4, weight_decay=1e-4),
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

model.fit(train_data, epochs=EPOCHS, validation_data=test_data)

model.save("vit_classifier.h5")
print("ViT model saved.")
