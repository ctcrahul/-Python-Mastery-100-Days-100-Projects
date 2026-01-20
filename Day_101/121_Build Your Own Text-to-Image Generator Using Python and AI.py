# Text-to-Image Generator using Stable Diffusion
# Real generative AI system

import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

# -----------------------------
# CONFIG
# -----------------------------
MODEL_ID = "runwayml/stable-diffusion-v1-5"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
