# Smart Timetable Generator
# Builds an optimized weekly schedule

subjects = {
    "Math": 5,
    "Coding": 7,
    "English": 3,
    "ML": 4
}

daily_hours = 6
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

schedule = {day: [] for day in days}
