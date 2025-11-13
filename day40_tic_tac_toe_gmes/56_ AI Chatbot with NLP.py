"""                                                       Day = 56
                                                                    
                                                       AI Chatbot with NLP 

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
        "tag": "thanks",
        "patterns": [
            "thanks", "thank you", "thx", "I appreciate it"
        ],
        "responses": [
            "You're welcome!",
            "Glad I could help.",
            "Anytime!"
        ]
    },
    {
        "tag": "weather",
        "patterns": [
            "what is the weather", "how is the weather", "weather today"
        ],
        "responses": [
            "I cannot check live weather now, but you can try searching online.",
            "Weather APIs are not enabled yet, but I can help with general questions."
        ]
    },
    {
        "tag": "creator",
        "patterns": [
            "who created you", "who made you", "your creator"
        ],
        "responses": [
            "I was created as a Python NLP project!",
            "A developer built me using machine learning and NLP."
        ]
    },
]

LOW_CONFIDENCE_RESPONSES = [
    "I'm not sure I understood that.",
    "Can you rephrase?",
    "I don't know that yet, but I'm learning.",
]

# -------------------------------------------
# 2. NLP Preprocessing
# -------------------------------------------
STOPWORDS = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    tokens = word_tokenize(text)
    tokens = [w for w in tokens if w not in STOPWORDS]
    return " ".join(tokens)

# -------------------------------------------
# 3. Train the Intent Classifier
# -------------------------------------------
def prepare_training_data():
    X = []
    y = []
    for intent in INTENTS:
        for pattern in intent["patterns"]:
            X.append(clean_text(pattern))
            y.append(intent["tag"])
    return X, y

X_train, y_train = prepare_training_data()

vectorizer = TfidfVectorizer()
X_vec = vectorizer.fit_transform(X_train)

model = LogisticRegression(max_iter=1000)
model.fit(X_vec, y_train)

# -------------------------------------------
# 4. Chatbot Logic
# -------------------------------------------
def predict_intent(msg):
    cleaned = clean_text(msg)
    vec = vectorizer.transform([cleaned])
    probabilities = model.predict_proba(vec)[0]
    max_prob = max(probabilities)
    intent = model.classes_[probabilities.argmax()]

    if max_prob < 0.40:
        return None, max_prob
    return intent, max_prob

def get_response(intent_tag):
    for intent in INTENTS:
        if intent["tag"] == intent_tag:
            return random.choice(intent["responses"])
    return random.choice(LOW_CONFIDENCE_RESPONSES)

def chatbot_reply(msg):
    intent, conf = predict_intent(msg)
    if intent is None:
        return random.choice(LOW_CONFIDENCE_RESPONSES)
    return get_response(intent)

# -------------------------------------------
# 5. Tkinter Chat UI
# -------------------------------------------
class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Chatbot with NLP")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.chat_window = tk.Text(root, bd=1, bg="#F5F5F5", height=20, width=50, wrap="word")
        self.chat_window.pack(pady=10)

        self.msg_entry = tk.Entry(root, bd=1, width=40, font=("Arial", 14))
        self.msg_entry.pack(side="left", padx=10, pady=10)
        self.msg_entry.bind("<Return>", self.send_msg)

        send_button = ttk.Button(root, text="Send", command=self.send_btn)
        send_button.pack(side="left", padx=10)

        self.chat_window.insert(tk.END, "Chatbot: Hello! Ask me anything.\n\n")

    def send_btn(self):
        self.send_msg(None)

    def send_msg(self, event):
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        self.chat_window.insert(tk.END, f"You: {msg}\n")
        self.msg_entry.delete(0, tk.END)

        reply = chatbot_reply(msg)
        self.chat_window.insert(tk.END, f"Chatbot: {reply}\n\n")
        self.chat_window.see(tk.END)

# -------------------------------------------
# 6. Run App
# -------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                                                    Thanks for visting and keep supporting us..
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
