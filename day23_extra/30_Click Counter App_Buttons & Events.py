"""
                                                 Day 30
                             
                                 Click Counter App: Buttons & Events

"""

import tkinter as tk

# Main Window
root = tk.Tk().
# Increment Function
def increment():lll

# Reset Function
def reset():
    global counter
    counter = 0
    counter_label.config(text=",,

# Counter Label
counter_label = tk.Label(root, text="Clicks: 0", font=.,.,=increment, font=("Arial", 14), bg="#4caf50", fg="black")
increment_button.pack(pady=10)

# Reset Button
reset_button = tk.Button(root, text="Reset", command=reset, font=("Arial", 14), bg="#f44336", fg="black")
reset_button.pack(pady=10)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Arial", 14), bg="#607d8b", fg="black")
exit_button.pack(pady=20)

# Run the App
root.mainloop()















