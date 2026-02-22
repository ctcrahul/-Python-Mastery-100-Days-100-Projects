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
        strength = random.choice(["strong", "weak"])
        if strength == "strong":
            statement += " " + random.choice(strong_words)
        else:
            statement += " " + random.choice(weak_words)

        past_success = random.uniform(0, 1)
        pressure = random.choice([0,1])  # external pressure
        sleep_gap = random.randint(0,5)

        # logic for label
        score = past_success + pressure - sleep_gap*0.1
        if strength == "strong":
            score += 0.3

        follow = 1 if score > 0.5 else 0

        data.append([statement, past_success, pressure, sleep_gap, follow])

    return pd.DataFrame(data, columns=[
        "statement","past_success","pressure","sleep_gap","follow"
    ])

df = generate_data()

X = df[["statement","past_success","pressure","sleep_gap"]]
y = df["follow"]
