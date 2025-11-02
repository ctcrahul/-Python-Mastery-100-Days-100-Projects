import tkinter as tk

# Initialize Timer variables
session_count = 0
timer_running = False

# Timer Logic
def countdown(seconds):
	global timer_running
	if seconds >= 0:
		mins, secs = divmod(seconds, 60)
		timer_label.config(text=f"{mins:02d}:{secs:02d}")
		window.after(1, countdown, seconds - 1)
	else:
		timer_running = False
		start_timer()

def start_timer():
	global session_count, timer_running
	if not timer_running:
		timer_running = True
		if session_count % 8 == 7:
			countdown(15 * 60) # Long Break
			status_label.config(text="Long Break", fg="blue")
		elif session_count % 2 == 0:
			countdown(25 * 60) # Work Session
			status_label.config(text="Work", fg="green")
		else:
			countdown(5 * 60) # Short Break
			status_label.config(text="Break", fg="orange")
		session_count += 1

# Reset Timer
def reset_timer():
	global session_count, timer_running
	session_count = 0
	timer_running = False
	timer_label.config(text="25:00")
	status_label.config(text="Ready")


# Create Main Window
window = tk.Tk()
window.title("Pomodoro Timer")
window.geometry("300x300")

# Add a label for Timer
timer_label = tk.Label(window, text="25:00", font=("Arial", 40))
timer_label.pack(pady=20)

# Status Label
status_label = tk.Label(window, text="Ready", font=("Arial", 20))
status_label.pack()

# Start Button
start_button = tk.Button(window, text="Start", command=start_timer, font=("Arial", 16))
start_button.pack(side="left", padx=20)


# Reset Button
reset_button = tk.Button(window, text="Reset", command=reset_timer, font=("Arial", 16))
reset_button.pack(side="right", padx=20)

window.mainloop()







