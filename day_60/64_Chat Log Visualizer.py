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
    """
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
