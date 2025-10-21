"""
                                                       Day 33.py
                                                       
                                             Simple Login System: Message Boxes



"""



import tkinter as tk
from tkinter import messagebox

# Main Window
root = tk.Tk()
root.title("Simple Login System")
root.geometry("400x300")
root.configure(bg="#f0f4c3")

# Predefined Credentials
USER_CREDENTIALS = {
    "admin": "admin123",
    "user": "user123"
}

# Title Label
title_label = tk.Label(root, text="Login System", font=("Arial", 20), bg="#f0f4c3")
title_label.pack(pady=20)

# Username Input
username_label = tk.Label(root, text="Username:", font=("Arial", 12), bg="#f0f4c3")
username_label.pack()
username_entry = tk.Entry(root, font=("Arial", 12))
username_entry.pack(pady=5)

# Password Input
password_label = tk.Label(root, text="Password:", font=("Arial", 12), bg="#f0f4c3")
password_label.pack()
password_entry = tk.Entry(root, font=("Arial", 12), show="*")
password_entry.pack(pady=5)

# Login Function
def login():
    username = username_entry.get()
    password = password_entry.get()
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] =15632466
