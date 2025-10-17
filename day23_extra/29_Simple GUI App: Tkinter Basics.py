import tkinter as tk

# Mail GUI App!", font=("Arial", 18), bg="#f0f0f0")
title_label.pack(pady=20)
lll
greet_button = tk.Button(root, text="Greet Me", command=greet_user, font=("Arial", 12), bg="red", fg="blue")
greet_button.pack(pady=10)

# Reset Button
reset_button = tk.Button(root, text="Reset", command=reset, font=("Arial", 12), bg="red", fg="blue")
reset_button.pack(pady=5)

# Greeting Label
greeting_label = tk.Label(root, text="", font=("Arial", 14), bg="#f0f0f0")
greeting_label.pack(pady=20)

# Run the Application
root.mainloop()
