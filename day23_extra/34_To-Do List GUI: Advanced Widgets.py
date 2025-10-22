import tkinter as tk
from tkinter import messagebox

# Main Window
root = tk.Tk()
root.title("To-Do List App")
root.geometry("400x500")
root.configure(bg="#e3f2fd")

# Functions
def add_task():
    task = task_entry.get()
    if task.strip():
        task_listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Task cannot be empty.")

def delete_task():
    selected = task_listbox.curselection()
    if selected:
        task_listbox.delete(selected[0])
    else:
        messagebox.showerror("Error", "Select a task to delete.")

def clear_tasks():
    task_listbox.delete(0, tk.END)

# Title Label
title_label = tk.Label(root, text="To-Do List", font=("Arial", 24), bg="#e3f2fd")
title_label.pack(pady=10)

# Entry Field
task_entry = tk.Entry(root, font=("Arial", 14), width=30)
task_entry.pack(pady=10)

# Buttons Frame
button_frame = tk.Frame(root, bg="#e3f2fd")
button_frame.pack(pady=10)

add_button = tk.Button(button_frame, text="Add Task", command=add_task, font=("Arial", 12), bg="#4caf50", fg="black")
add_button.grid(row=0, column=0, padx=5)

delete_button = tk.Button(button_frame, text="Delete Task", command=delete_task, font=("Arial", 12), bg="#f44336", fg="black")
delete_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(button_frame, text="Clear Tasks", command=clear_tasks, font=("Arial", 12), bg="#607d8b", fg="black")
clear_button.grid(row=0, column=2, padx=5)

# Task Listbox with Scrollbar
frame = tk.Frame(root)
frame.pack(pady=10)

scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

task_listbox = tk.Listbox(frame, width=50, height=15, yscrollcommand=scrollbar.set, font=("Arial", 12))
task_listbox.pack(pady=10)

scrollbar.config(command=task_listbox.yview)

# Exit Button
exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Arial", 12), bg="#d32f2f", fg="black")
exit_button.pack(pady=10)

# Run the App
root.mainloop()








