# OCR System - Extract Text from Images
# Real-world CV + NLP pipeline

import cv2
import pytesseract
from PIL import Image

# If on Windows, uncomment and set path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

IMAGE_PATH = "sample.jpg"

# -----------------------------
# IMAGE PREPROCESSING
# -----------------------------
def preprocess(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
