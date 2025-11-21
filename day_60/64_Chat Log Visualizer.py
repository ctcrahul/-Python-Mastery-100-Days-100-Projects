import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns


def parse_chat(file_path):
    """
def parse_chat(file_path):
    """
    Parses WhatsApp-like chat files into structured DataFrame

    pattern = r"(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2}) (AM|PM) - (.*?): (.*)"

    data = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                date, time, period, sender, message = match.groups()
                timestamp = f"{date} {time} {period}"
                data.append([timestamp, sender, message])

    df = pd.DataFrame(data, col

                       df = pd.DataFrame(data, columns=["Timestamp", "Sender", "Message"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%d/%m/%Y %I:%M %p", errors="coerce")

    df["Hour"] = df["Timestamp"].dt.hour
    df["Day"] = df["Timestamp"].dt.day_name()
    df["Date"] = df["Timestamp"].dt.date

    return df


def visualize_chat(df):
    """
    Create multiple visualizations in one window
    """

    plt.figure(figsize=(15, 10))

    # 1. Messages per person
    plt.subplot(2, 2, 1)
    df["Sender"].value_counts().plot(kind="bar")
    plt.title("Messages per Person")
    plt.ylabel("Count")



    
