from flask import Flask, request, render_template_string
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# ------------------ DATA ------------------
ROLES = {
    "Data Analyst": [
        "Explain a data-driven decision you made.",
        "How do you handle missing data?",
        "What is overfitting?"
    ],
    "ML Engineer": [
        "Explain bias-variance tradeoff.",
        "How would you deploy an ML model?",
        "What is model drift?"
    ]
}
