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
