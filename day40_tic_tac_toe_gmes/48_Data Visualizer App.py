import tkinter as tk
from tkinter import filedialog
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def load_file(file_path):
    if file_path.endswith(".csv"):
        return pd.read_csv(file_path)
    elif file_path.endswith(".xlsx"):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")


def plot_data(df, column_x, column_y):
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(df[column_x], df[column_y], marker="o")
    ax.set_title(f"{column_x} vs {column_y}")
    ax.set_xlabel(column_x)
    ax.set_ylabel(column_y)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=20)


def update_dropdowns(columns):
    x_dropdown.set("")
    y_dropdown.set("")
    x_menu["menu"].delete(0, "end")
    y_menu["menu"].delete(0, "end")
    for column in columns:
        x_menu["menu"].add_command(label=column, command=lambda value=column: x_dropdown.set(value))
        y_menu["menu"].add_command(label=column, command=lambda value=column: y_dropdown.set(value))


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
    print(f"File selected: {file_path}")
    return file_path

def handle_file_upload():
    global df
    file_path = open_file()
    try:
        df = load_file(file_path)
        update_dropdowns(df.columns)
        print(f"Columns available: {df.columns}")
    except Exception as e:
        print(f"Error: {e}")

def handle_plot():
    try:
        column_x = x_dropdown.get()
        column_y = y_dropdown.get()
        if not column_x or not column_y:
            print("Please select both X and Y axes.")
            return
        plot_data(df, column_x, column_y)
    except Exception as e:
        print(f"Error: {e}")


# Initialize Tkinter App
root = tk.Tk()
root.title("Data Visualizer")
root.geometry("800x600")


upload_button = tk.Button(root, text="Upload File", command=handle_file_upload)
upload_button.pack(pady=10)


# Dropdowns for selecting columns
x_label = tk.Label(root, text="Select X-axis:")
x_label.pack(pady=5)
x_dropdown = tk.StringVar()
x_menu = tk.OptionMenu(root, x_dropdown, [])
x_menu.pack(pady=5)

y_label = tk.Label(root, text="Select Y-axis:")
y_label.pack(pady=5)
y_dropdown = tk.StringVar()
y_menu = tk.OptionMenu(root, y_dropdown, [])
y_menu.pack(pady=5)


plot_button = tk.Button(root, text="Generate Plot", command=handle_plot)
plot_button.pack(pady=10)


root.mainloop()




























