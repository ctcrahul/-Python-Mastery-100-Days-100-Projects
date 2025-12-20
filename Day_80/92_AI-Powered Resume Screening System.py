# Project 92: AI-Powered Resume Screening System
# Author: You (run this and understand every line)

import os
import re
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# -----------------------------
# Text Cleaning Function
# -----------------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# -----------------------------
# Load Resumes
# -----------------------------
def load_resumes(folder_path):
    resumes = []
    filenames = []

    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), 'r', encoding='utf-8', errors='ignore') as f:
                resumes.append(clean_text(f.read()))
                filenames.append(file)

    return resumes, filenames

# -----------------------------
# Resume Ranking Logic
# -----------------------------
def rank_resumes(job_description, resumes, filenames):
    documents = [clean_text(job_description)] + resumes

    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    results = pd.DataFrame({
        "Resume": filenames,
        "Match_Score": similarity_scores
    })

    return results.sort_values(by="Match_Score", ascending=False)
# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    job_description = """
    We are looking for a Python developer with experience in
    machine learning, data analysis, pandas, numpy, and scikit-learn.
    Knowledge of NLP is a plus.
    """

    resume_folder = "resumes"  # folder containing .txt resumes

    resumes, filenames = load_resumes(resume_folder)
    ranked_resumes = rank_resumes(job_description, resumes, filenames)

    print("\n===== Resume Ranking =====\n")
    print(ranked_resumes.to_string(index=False))
