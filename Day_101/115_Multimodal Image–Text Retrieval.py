# Multimodal Image–Text Retrieval (CLIP-style)
# Image ↔ Text similarity system

import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# -----------------------------
# LOAD MODEL
# -----------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

# -----------------------------
# INPUTS
# -----------------------------
image_path = "sample.jpg"
texts = [
    "a dog playing on grass",
    "a car on the road",
    "a person cooking food",
    "a cat sleeping on a sofa"
]

image = Image.open(image_path)

# -----------------------------
# PREPROCESS
# -----------------------------
