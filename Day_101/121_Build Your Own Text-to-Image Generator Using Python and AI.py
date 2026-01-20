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

# -----------------------------
# LOAD MODEL
# -----------------------------
pipe = StableDiffusionPipeline.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32
)

pipe = pipe.to(DEVICE)

# -----------------------------
# GENERATE IMAGE
# -----------------------------
def generate_image(prompt, output_path="output.png"):
    image = pipe(
        prompt=prompt,
        guidance_scale=7.5,
        num_inference_steps=30
    ).images[0]

    image.save(output_path)
    print(f"Image saved to {output_path}")

# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    prompt = input("Enter text prompt: ")
    generate_image(prompt)
