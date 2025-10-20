"""
                                                      Day 32.py
                                                     
                                            Drawing Pad App: Canvas Widgets


"""



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
ws
# Control Panel
control_frame = tk.Frame(root, bg="#f0f0f0")
control_frame.pack(pady=10)

# Color Buttonss









