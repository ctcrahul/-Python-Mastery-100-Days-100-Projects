# Smart Timetable Generator
# Builds an optimized weekly schedule

Subjects = {
  "Math": 5,
  "Coding": 7,
  "English": 3,
  "ML": 4
}
Total Daily Hours = 6# Smart Timetable Generator
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

# Expand subjects by priority
expanded = []
for sub, hrs in subjects.items():
    expanded += [sub] * hrs

index = 0

for day in days:
    used = 0
    while used < daily_hours and index < len(expanded):
        schedule[day].append(expanded[index])
        used += 1
        index += 1

# Print schedule
print("\nGenerated Weekly Study Timetable:\n")
for day in days:
    print(day, ":", schedule[day])



subjects = {
    "Math": 5,
    "Coding": 7,
    "English": 3,
    "ML": 4
}

daily_hours = 6
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

schedule = {day: [] for day in days}
# Expand subjects by priority
expanded = []
for sub, hrs in subjects.items():
    expanded += [sub] * hrs

index = 0

for day in days:
    used = 0
    while used < daily_hours and index < len(expanded):
        schedule[day].append(expanded[index])
        used += 1
        index += 1

# Print schedule
print("\nGenerated Weekly Study Timetable:\n")
for day in days:
    print(day, ":", schedule[day])
