import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
from openai import OpenAI
import requests
import os

# ========== SET API KEY ==========
OPENAI_API_KEY = "YOUR_API_KEY"
client = OpenAI(api_key=OPENAI_API_KEY)

# ========== AI SLIDE GENERATOR ==========
def generate_slides(topic, num_slides):

    prompt = f"""
    Create a professional presentation on: {topic}

    Give exactly {num_slides} slides.

    For each slide provide:
    Slide Title:
    Bullet Points (3-5)
    Speaker Notes

    Format strictly like:

    Slide 1:
    Title:
    Points:
    Notes:

    Slide 2:
    ...
    """
