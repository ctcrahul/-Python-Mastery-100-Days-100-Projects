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

# -----------------------------
# View Expenses
# -----------------------------
def view_expenses():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No expenses found.")
    else:
        print(df)

# -----------------------------
# Expense Analysis
# -----------------------------
def analyze_expenses():
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        print("No data to analyze.")
        return

    summary = df.groupby("Category")["Amount"].sum()
    print("\nExpense Summary:\n")
    print(summary)

    summary.plot(kind="bar")
    plt.title("Expense Distribution by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Amount")
    plt.tight_layout()
    plt.show()

# -----------------------------
# MAIN MENU
# -----------------------------
def main():
    initialize_file()

    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Analyze Expenses")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            category = input("Category: ")
            amount = float(input("Amount: "))
            note = input("Note (optional): ")
            add_expense(category, amount, note)

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            analyze_expenses()

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
