import random
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------
# Fake Tweet Generator
# ----------------------------
TICKERS = ["TSLA", "AAPL", "GOOG", "MSFT", "AMZN", "META"]

POSITIVE_WORDS = [
    "bullish", "moon", "pump", "strong", "buying", "profit", "love",
    "amazing", "growth", "surging", "breaking out"
]

NEGATIVE_WORDS = [
    "bearish", "dump", "crash", "weak", "losing", "hate",
    "falling", "drop", "panic", "bubble"
]

NEUTRAL_WORDS = [
    "hold", "watching", "market", "price", "move",
    "waiting", "sideways", "pattern", "volume"
]

def generate_fake_tweets(stock, n=200):
    tweets = []
    for i in range(n):
        sentiment = random.choice(["positive", "negative", "neutral"])
        if sentiment == "positive":
            text = f"{stock} is {random.choice(POSITIVE_WORDS)} 🚀"
        elif sentiment == "negative":
            text = f"{stock} is {random.choice(NEGATIVE_WORDS)} 😡"
        else:
            text = f"{stock} is {random.choice(NEUTRAL_WORDS)} 🤔"

        timestamp = pd.Timestamp.now() - pd.Timedelta(minutes=random.randint(0, 600))
        tweets.append([timestamp, text])
    return pd.DataFrame(tweets, columns=["Time", "Tweet"])

