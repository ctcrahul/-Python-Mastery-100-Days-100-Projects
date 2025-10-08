
"""                           Day20.py

                  Event Countdown Timer: Dates & Time


"""
tetime

formatted_time = current_time.strftime("%m-%d-%Y %H:%M:%S")
print("Formatted Time:", formatted_time)

from datetime import datetime

event_date = datetime(2025, 1, 25)
curreent_date = datetime.now()
time_difference = event_date - curreent_date
print("Days Remaining:", time_difference.days)

# Event Countdown Timer
from datetime import datetime, timedelta
import time

# Step 1: Get Event Date and Time from User
def get_event_datetime():
  try:
    date_input = input("Enter the event date (YYYY-MM-DD HH:MM:SS): ")
    return datetime.strptime(date_input, "%Y-%m-%d %H:%M:%S")
  except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD HH:MM:SS format.")
    return None

# Step 2: Calculating Time Remaining
def calculate_time_remaining(event_date):
  current_datetime = datetime.now()
  time_difference = event_date - current_datetime
  return time_difference

# Step 3: Display Countdown
def display_countdown(time_left):
  days = time_left.days
  hours, remainder = divmod(time_left.seconds, 3600)
  minutes, seconds = divmod(remainder, 60)
  print(f"\nTime Remaining: {days} days, {hours} hours, {minutes} minutes, {seconds} seconds", end="")

# Step 4: Main Countdown Loop
def start_countdown(event_date):
  while True:
    time_left = calculate_time_remaining(event_date)
    if time_left.total_seconds() <= 0:
      print("\nCountdown Complete!")
      break
    display_countdown(time_left)
    time.sleep(1)


# Main Program
event_datetime = get_event_
  start_countdown(event_datetime)
