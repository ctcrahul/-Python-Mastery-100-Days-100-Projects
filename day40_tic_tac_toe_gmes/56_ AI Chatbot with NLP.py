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
from tkinter import ttk
import re
import random
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle



# -------------------------------------------
# 1. INTENTS (edit this for training)
# -------------------------------------------
INTENTS = [
    {
        "tag": "greeting",
        "patterns": [
            "hello", "hi", "hey", "good morning", "good evening",
            "what's up", "how are you", "is anyone there"
        ],
        "responses": [
            "Hello! How can I help you today?",
            "Hi there! What can I do for you?",
            "I'm here. Ask anything."
        ]

         },
    {
        "tag": "goodbye",
        "patterns": [
            "bye", "goodbye", "see you later", "talk to you later"
        ],
        "responses": [
            "Goodbye! Take care.",
            "See you later!",
            "Have a nice day!"
        ]
    },
    {
