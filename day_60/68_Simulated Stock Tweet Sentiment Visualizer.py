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
 ----------------------------
# Sentiment Analyzer (Rule-Based)
# ----------------------------
def calculate_sentiment(tweet):
    tweet = tweet.lower()
    score = 0

    for word in POSITIVE_WORDS:
        if word in tweet:
            score += 1

    for word in NEGATIVE_WORDS:
        if word in tweet:
            score -= 1

    return score


# ----------------------------
# Visualizer
# ----------------------------
def visualize_sentiment(stock):

    df = generate_fake_tweets(stock)

    df["Sentiment"] = df["Tweet"].apply(calculate_sentiment)
    df["Minute"] = df["Time"].dt.floor("5min")

    grouped = df.groupby("Minute")["Sentiment"].mean()

    # Plot line graph
    plt.figure(figsize=(12,6))
    plt.plot(grouped.index, grouped.values, marker="o")

    plt.axhline(0, linestyle="--")
    plt.title(f"Simulated Twitter Sentiment for {stock}")
    plt.xlabel("Time")
    plt.ylabel("Sentiment Score")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Heatmap
    df["Hour"] = df["Time"].dt.hour
    heat = df.groupby(["Hour"])["Sentiment"].mean()

    plt.figure(figsize=(10,4))
    plt.bar(heat.index, heat.values)
    plt.title(f"Hourly Sentiment Heatmap - {stock}")
    plt.xlabel("Hour")
    plt.ylabel("Avg Sentiment")
    plt.tight_layout()
    plt.show()
# ----------------------------
# GUI App
# ----------------------------
class StockSentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Tweet Sentiment Visualizer")
        self.root.geometry("450x300")

        title = tk.Label(root, text="Stock Tweet Sentiment Simulator",
                         font=("Arial", 14, "bold"))
        title.pack(pady=15)

        tk.Label(root, text="Select Stock Ticker:").pack(pady=5)

        self.stock_var = tk.StringVar(value=TICKERS[0])

        self.dropdown = ttk.Combobox(root, textvariable=self.stock_var,
                                     values=TICKERS, state="readonly")
        self.dropdown.pack(pady=5)

        self.generate_btn = tk.Button(root,
                                      text="Generate Sentiment Analysis",
                                      command=self.run_simulation,
                                      bg="black", fg="white", width=28)
        self.generate_btn.pack(pady=20)

        self.status = tk.Label(root, text="", fg="green")
        self.status.pack()

    def run_simulation(self):
        stock = self.stock_var.get()

        self.status.config(text="Simulating tweets & generating graphs...")

        visualize_sentiment(stock)

        self.status.config(text="Done! Check graphs.")


# ----------------------------
# Run Application
# ----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = StockSentimentApp(root)
    root.mainloop()

