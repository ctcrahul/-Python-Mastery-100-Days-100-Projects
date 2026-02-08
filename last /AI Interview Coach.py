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

IDEAL_ANSWERS = {
    "Explain a data-driven decision you made.": "business impact metrics analysis outcome",
    "How do you handle missing data?": "imputation deletion distribution statistics",
    "What is overfitting?": "model memorizes training data poor generalization",
    "Explain bias-variance tradeoff.": "underfitting overfitting balance error",
    "How would you deploy an ML model?": "api docker monitoring versioning",
    "What is model drift?": "data distribution changes performance degradation"
}

# ------------------ LOGIC ------------------
def evaluate_answer(answer, reference):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([answer, reference])
    similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    length_score = min(len(answer.split()) / 80, 1.0)
    final_score = round((similarity * 0.7 + length_score * 0.3) * 100, 2)

    return final_score, similarity
