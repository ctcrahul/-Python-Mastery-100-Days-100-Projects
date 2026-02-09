# pip install flask scikit-learn spacy
# python -m spacy download en_core_web_sm

from flask import Flask, request, render_template_string
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)
nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Learning Content
# -----------------------------
TOPICS = {
    "Python Basics": {
        "easy": "Explain what a variable is in Python.",
        "medium": "Difference between list and tuple.",
        "hard": "Explain Python memory management."
    },
    "Machine Learning": {
        "easy": "What is supervised learning?",
        "medium": "Explain bias vs variance.",
        "hard": "How does gradient descent work?"
    }
}
