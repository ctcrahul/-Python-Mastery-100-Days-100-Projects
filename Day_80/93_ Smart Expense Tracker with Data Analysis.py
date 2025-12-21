# Project 93: Smart Expense Tracker with Data Analysis
# Author: You

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

FILE_NAME = "expenses.csv"

# -----------------------------
# Initialize CSV if not exists
# -----------------------------
def initialize_file():
    try:
        pd.read_csv(FILE_NAME)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Date", "Category", "Amount", "Note"])
        df.to_csv(FILE_NAME, index=False)

# -----------------------------
# Add Expense
# -----------------------------
def add_expense(category, amount, note=""):
    df = pd.read_csv(FILE_NAME)
    new_entry = {
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Category": category,
        "Amount": amount,
        "Note": note
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    print("Expense added successfully.")

