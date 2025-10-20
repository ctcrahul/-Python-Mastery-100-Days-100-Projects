import tkinter as tk
from tkinter import colorchooser

# Main Window
root = tk.Tk()
root.title("Drawing Pad App")
root.geometry("600x600")
root.configure(bg="#f0f0f0")

# Global Variables
current_color = "black"
current_thickness = 2

# Create Canvas
canvas = tk.Canvas(root, width=500, height=400, bg="white", relief="ridge", bd=2)
canvas.pack(pady=20)

# Drawing Function
def draw(event):
    x, y = event.x, event.y
    canvas.create_oval(
        x - current_thickness, y - current_thickness,
        x + current_thickness, y + current_thickness,
        fill=current_color, outline=current_color
    )

# Clear Canvas
def clear_canvas():
    canvas.delete("all")

# Change Color
def change_color():
    global current_color
    color = colorchooser.askcolor()[1]
    if color:
        current_color = color

# Change Thickness
def change_thickness(value):
    global current_thickness
    current_thickness = int(value)

# Bind Drawing
canvas.bind("<B1-Motion>", draw)

# Control Panel
control_frame = tk.Frame(root, bg="#f0f0f0")
control_frame.pack(pady=10)

# Color Button
color_btn = tk.Button(control_frame, text="Choose Color", command=change_color, bg="#4CAF50", fg="black", font=("Arial", 10))
color_btn.grid(row=0, column=0, padx=10)

# Clear Button
clear_btn = tk.Button(control_frame, text="Clear Canvas", command=clear_canvas, bg="#f44336", fg="black", font=("Arial", 10))
clear_btn.grid(row=0, column=1, padx=10)

# Thickness Control
thickness_label = tk.Label(control_frame, text="Thickness:", bg="#f0f0f0", font=("Arial", 10))
thickness_label.grid(row=0, column=2, padx=10)

thickness_slider = tk.Scale(control_frame, from_=1, to=10, orient="horizontal", command=change_thickness, bg="#f0f0f0")
thickness_slider.set(2)
thickness_slider.grid(row=0, column=3, padx=10)

# Run Application
root.mainloop()













