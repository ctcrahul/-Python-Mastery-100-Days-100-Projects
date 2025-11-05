"""                                                            Day = 48
  
                                                          Data Visualizer App
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Data Visualizer Pro")
        self.root.geometry("950x650")
        self.root.configure(bg="#f2f4f7")

        self.df = None

        # Title Section
        title = tk.Label(root, text="Data Visualizer Pro", font=("Segoe UI", 20, "bold"), fg="#2c3e50", bg="#f2f4f7")
        title.pack(pady=20)

        # Upload Section
        upload_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
        upload_frame.pack(pady=15, padx=30, fill="x")

        upload_label = tk.Label(upload_frame, text="Upload your CSV or Excel file:", font=("Segoe UI", 12), bg="#ffffff")
        upload_label.pack(side="left", padx=20, pady=15)

        upload_btn = tk.Button(upload_frame, text="📂 Choose File", command=self.handle_file_upload,
                               font=("Segoe UI", 11, "bold"), bg="#3498db", fg="white", activebackground="#2980b9",
                               relief="flat", padx=20, pady=5, cursor="hand2")
        upload_btn.pack(side="right", padx=20, pady=10)

        # Dropdown Section
        self.dropdown_frame = tk.Frame(root, bg="#f2f4f7")
        self.dropdown_frame.pack(pady=10)

        tk.Label(self.dropdown_frame, text="Select X-axis:", font=("Segoe UI", 11), bg="#f2f4f7").grid(row=0, column=0, padx=10, pady=5)
        self.x_dropdown = tk.StringVar()
        self.x_menu = tk.OptionMenu(self.dropdown_frame, self.x_dropdown, ())
        self.style_optionmenu(self.x_menu)
        self.x_menu.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.dropdown_frame, text="Select Y-axis:", font=("Segoe UI", 11), bg="#f2f4f7").grid(row=0, column=2, padx=10, pady=5)
        self.y_dropdown = tk.StringVar()
        self.y_menu = tk.OptionMenu(self.dropdown_frame, self.y_dropdown, ())
        self.style_optionmenu(self.y_menu)
        self.y_menu.grid(row=0, column=3, padx=10, pady=5)

        # Plot Button
        plot_btn = tk.Button(root, text="📈 Generate Plot", command=self.handle_plot,
                             font=("Segoe UI", 12, "bold"), bg="#27ae60", fg="white", activebackground="#1e8449",
                             relief="flat", padx=20, pady=10, cursor="hand2")
        plot_btn.pack(pady=20)

        # Frame for the plot
        self.plot_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
        self.plot_frame.pack(pady=10, padx=30, fill="both", expand=True)

    def style_optionmenu(self, menu):
        menu.config(font=("Segoe UI", 10), bg="white", relief="flat", highlightthickness=1, width=20, cursor="hand2")

    def handle_file_upload(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")],
            title="Select a CSV or Excel file"
        )
        if not file_path:
            return

        try:
            self.df = self.load_file(file_path)
            self.update_dropdowns(self.df.columns)
            messagebox.showinfo("Success", f"File loaded successfully!\n\nColumns detected:\n{', '.join(self.df.columns)}")
        except Exception as e:
            messagebox.showerror("Error", f"Unable to load file.\n\n{str(e)}")

    def load_file(self, file_path):
        if file_path.endswith(".csv"):
            return pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file format. Please provide a .csv or .xlsx file.")

    def update_dropdowns(self, columns):
        # Clear old options
        menu_x = self.x_menu["menu"]
        menu_y = self.y_menu["menu"]
        menu_x.delete(0, "end")
        menu_y.delete(0, "end")

        for col in columns:
            menu_x.add_command(label=col, command=lambda v=col: self.x_dropdown.set(v))
            menu_y.add_command(label=col, command=lambda v=col: self.y_dropdown.set(v))

        self.x_dropdown.set("")
        self.y_dropdown.set("")

    def handle_plot(self):
        if self.df is None:
            messagebox.showerror("Error", "Please upload a file first.")
            return

        col_x = self.x_dropdown.get()
        col_y = self.y_dropdown.get()

        if not col_x or not col_y:
            messagebox.showerror("Error", "Please select both X and Y columns.")
            return

        self.display_plot(col_x, col_y)

    def display_plot(self, col_x, col_y):
        # Clear previous plot
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(self.df[col_x], self.df[col_y], color="#3498db", marker="o", linewidth=2)
        ax.set_title(f"{col_y} vs {col_x}", fontsize=14, color="#2c3e50")
        ax.set_xlabel(col_x, fontsize=12)
        ax.set_ylabel(col_y, fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.5)

        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizerApp(root)
    root.mainloop()


############################################################################################################################################################################
                                                         Thanks for visting keep supporting us
############################################################################################################################################################################



import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DataVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Data Visualizer Pro")
        self.root.geometry("950x650")
        self.root.configure(bg="#f2f4f7")

        self.df = None

        # Title Section
        title = tk.Label(root, text="Data Visualizer Pro", font=("Segoe UI", 20, "bold"), fg="#2c3e50", bg="#f2f4f7")
        title.pack(pady=20)

        # Upload Section
        upload_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
        upload_frame.pack(pady=15, padx=30, fill="x")



