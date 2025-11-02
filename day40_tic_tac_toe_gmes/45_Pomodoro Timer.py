"""                                                                 Day 45

					                                           Pomodoro Timer
"""



import tkinter as tk
from tkinter import messagebox
import time
import winsound  # For sound notifications on Windows

# Initialize Timer Variables
session_count = 0
timer_running = False
remaining_seconds = 0

# Timer Logic
def countdown():
    global remaining_seconds, timer_running
    if remaining_seconds >= 0:
        mins, secs = divmod(remaining_seconds, 60)
        timer_label.config(text=f"{mins:02d}:{secs:02d}")
        remaining_seconds -= 1
        window.after(1000, countdown)  # Update every second
    else:
        timer_running = False
        start_timer()

# Start Timer Function
def start_timer():
    global session_count, timer_running, remaining_seconds
    if not timer_running:
        timer_running = True
        if session_count % 8 == 7:
            remaining_seconds = 15 * 60  # Long Break (15 minutes)
            status_label.config(text="Long Break", fg="blue")
            winsound.Beep(1000, 500)  # Sound for long break start
        elif session_count % 2 == 0:
            remaining_seconds = 25 * 60  # Work Session (25 minutes)
            status_label.config(text="Work", fg="green")
            winsound.Beep(800, 500)  # Sound for work session start
        else:
            remaining_seconds = 5 * 60  # Short Break (5 minutes)
            status_label.config(text="Break", fg="orange")
            winsound.Beep(600, 500)  # Sound for short break start
        countdown()
        session_count += 1
        session_counter.config(text=f"Pomodoros: {session_count // 2}")  # Count completed Pomodoros

# Reset Timer
def reset_timer():
    global session_count, timer_running, remaining_seconds
    session_count = 0
    timer_running = False
    remaining_seconds = 25 * 60  # Default to 25 minutes work session
    timer_label.config(text="25:00")
    status_label.config(text="Ready", fg="black")
    session_counter.config(text="Pomodoros: 0")
    winsound.Beep(400, 500)  # Reset sound

# Create Main Window
window = tk.Tk()
window.title("Pomodoro Timer")
window.geometry("400x400")
window.configure(bg="#f7f7f7")

# Add a label for Timer
timer_label = tk.Label(window, text="25:00", font=("Arial", 48, "bold"), bg="#f7f7f7", fg="#333")
timer_label.pack(pady=30)

# Status Label
status_label = tk.Label(window, text="Ready", font=("Arial", 20), bg="#f7f7f7", fg="black")
status_label.pack()

# Pomodoro Counter
session_counter = tk.Label(window, text="Pomodoros: 0", font=("Arial", 16), bg="#f7f7f7", fg="black")
session_counter.pack(pady=10)

# Start Button with Custom Style
start_button = tk.Button(window, text="Start", command=start_timer, font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", relief="flat", height=2, width=10)
start_button.pack(side="left", padx=20, pady=20)

# Reset Button with Custom Style
reset_button = tk.Button(window, text="Reset", command=reset_timer, font=("Arial", 16, "bold"), bg="#FF5733", fg="white", relief="flat", height=2, width=10)
reset_button.pack(side="right", padx=20, pady=20)

# Exit Button
exit_button = tk.Button(window, text="Exit", command=window.quit, font=("Arial", 16, "bold"), bg="#9E9E9E", fg="white", relief="flat", height=2, width=10)
exit_button.pack(side="bottom", pady=20)

# Styling the Window
window.configure(bg="#f7f7f7")
window.resizable(False, False)

# Run the Application
window.mainloop()




#############################################################################################################################################################################
                                                               Thanks for visting keep support us
#############################################################################################################################################################################
