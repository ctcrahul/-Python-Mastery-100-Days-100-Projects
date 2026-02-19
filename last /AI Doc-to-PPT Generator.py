import streamlit as st
from pptx import Presentation
from openai import OpenAI
from pypdf import PdfReader

OPENAI_API_KEY = "YOUR_API_KEY"
client = OpenAI(api_key=OPENAI_API_KEY)

# -------- Extract Text from PDF --------
def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

