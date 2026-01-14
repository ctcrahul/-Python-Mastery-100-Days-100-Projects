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
inputs = processor(
    text=texts,
    images=image,
    return_tensors="pt",
    padding=True
).to(device)

# -----------------------------
# EMBEDDINGS
# -----------------------------
with torch.nowith torch.no_grad():
    outputs = model(**inputs)
    image_embeds = outputs.image_embeds
    text_embeds = outputs.text_embeds

# Normalize embeddings
image_embeds = image_embeds / image_embeds.norm(dim=-1, keepdim=True)
text_embeds = text_embeds / text_embeds.norm(dim=-1, keepdim=True)

# -----------------------------
# SIMILARITY
# -----------------------------
similarity = (image_embeds @ text_embeds.T).squeeze(0)

print("\nImage–Text Similarity Scores:\n")
for txt, score in zip(texts, similarity):
    print(f"{txt:<30} -> {float(score):.3f}")


