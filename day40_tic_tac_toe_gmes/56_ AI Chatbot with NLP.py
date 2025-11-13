"""
AI Chatbot with NLP (Single File)
No extra files required.

Features:
 - Train your own chatbot using a simple intent-based NLP model
 - Uses TF-IDF + LogisticRegression for intent classification
 - Preprocessing: lowercasing, punctuation removal, stopword removal
 - GUI built with Tkinter
 - You can add/edit intents directly inside this file
 - Fallback answers when confidence is low
 - Context-independent (no external dataset required)

Dependencies:
    pip install scikit-learn nltk pandas
    python -m nltk.downloader punkt stopwords

Run:
    python ai_chatbot_nlp.py
"""

import tkinter as tk
