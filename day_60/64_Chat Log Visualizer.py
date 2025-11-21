                                                                     Day = 63

                                                                Chat Log Visualize

import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns


def parse_chat(file_path):
    """
    Parses WhatsApp-like chat files into structured DataFrame
    """
    pattern = r"(\d{1,2}/\d{1,2}/\d{4}), (\d{1,2}:\d{2}) (AM|PM) - (.*?): (.*)"

    data = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.match(pattern, line)
            if match:
                date, time, period, sender, message = match.groups()
                timestamp = f"{date} {time} {period}"
                data.append([timestamp, sender, message])

    df = pd.DataFrame(data, columns=["Timestamp", "Sender", "Message"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], format="%d/%m/%Y %I:%M %p", errors="coerce")

    df["Hour"] = df["Timestamp"].dt.hour
    df["Day"] = df["Timestamp"].dt.day_name()
    df["Date"] = df["Timestamp"].dt.date

    return df


def visualize_chat(df):
    """
    Create multiple visualizations in one window
    """

    plt.figure(figsize=(15, 10))

    # 1. Messages per person
    plt.subplot(2, 2, 1)
    df["Sender"].value_counts().plot(kind="bar")
    plt.title("Messages per Person")
    plt.ylabel("Count")

    # 2. Messages per day
    plt.subplot(2, 2, 2)
    df["Day"].value_counts().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ]).plot(kind="bar")
    plt.title("Messages per Day")

    # 3. Messages per hour
    plt.subplot(2, 2, 3)
    df["Hour"].value_counts().sort_index().plot(kind="line", marker="o")
    plt.title("Messages per Hour")
    plt.xlabel("Hour")
    plt.ylabel("Messages")

    # 4. Heatmap
    plt.subplot(2, 2, 4)
    heatmap_data = df.groupby(["Day", "Hour"]).size().unstack(fill_value=0)
    heatmap_data = heatmap_data.reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ])

    sns.heatmap(heatmap_data, cmap="coolwarm")
    plt.title("Chat Activity Heatmap")

    plt.tight_layout()
    plt.show()


class ChatVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Log Visualizer")
        self.root.geometry("600x300")

        title = tk.Label(root, text="Chat Log Visualizer", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        info = tk.Label(root, text="Load a WhatsApp chat export (.txt) to visualize")
        info.pack(pady=5)

        load_btn = tk.Button(root, text="Load Chat File", command=self.load_file, width=20)
        load_btn.pack(pady=20)

        self.status = tk.Label(root, text="Waiting for file...", fg="blue")
        self.status.pack(pady=5)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return
        
        try:
            self.status.config(text="Processing chat...", fg="orange")
            df = parse_chat(file_path)

            if df.empty:
                messagebox.showerror("Error", "No valid messages found in file!")
                return

            self.status.config(text="Generating visualizations...", fg="green")
            visualize_chat(df)

            self.status.config(text="Done!", fg="green")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.config(text="Error occurred", fg="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatVisualizerApp(root)
    root.mainloop()


#===========================================================================================================================================================================
                                                        Keep Exploring and Keep Learning..
#===========================================================================================================================================================================


    
