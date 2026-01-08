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
    # Noise removal
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Thresholding
    _, thresh = cv2.threshold(blur, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh

# -----------------------------
# OCR FUNCTION
# -----------------------------
def extract_text(processed_img):
    text = pytesseract.image_to_string(processed_img)
    return text
