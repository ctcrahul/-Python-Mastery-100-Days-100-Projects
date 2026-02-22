from flask import Flask, request, render_template_string
import pandas as pd
import random
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split

app = Flask(__name__)

# ---------- SYNTHETIC DATASET GENERATION ----------
def generate_data(n=1000):
    data = []
    strong_words = ["definitely", "surely", "promise", "commit", "guarantee"]
    weak_words = ["try", "maybe", "hope", "plan", "want"]

    for _ in range(n):
        statement = random.choice([
            "I will wake up early",
            "I will go to gym",
            "I will study daily",
            "I will eat healthy",
            "I will quit sugar"
        ])
