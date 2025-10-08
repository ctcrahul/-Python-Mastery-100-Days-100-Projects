
"""                           Day20.py

                  Event Countdown Timer: Dates & Time


"""



# Event Countdown Timer
from datetime import datetime, timedelta
import time

# Step 1: Get Event Date and Time from User
def get_event_datetime():se YYYY-MM-DD HH:MM:SS format.")
    return None

# Step 2: Calculating Time Remaining
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
