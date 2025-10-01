# -*- coding: utf-8 -*-
"""day13.ipynb

                          Student Grade Manager: List Comprehensions

"""

# [expression for item in iterable if condition]

squares = [x**2 for x in range(10)]
print(squares)

numbers = [1, 2, 3, 4, 5]
doubled = [x * 2 for x in numbers]
print(doubled)

numbers = [1, 2, 3, 4, 5, 6, 7]
evens = [x for x in numbers if x % 2 == 0]
print(evens)

names = ["Alice", "Bob", "Charlie", "Dave"]
short_names = [name for name in names if len(name) < 5]
print(short_names)

numbers = [1, 2, 3, 4, 5, 6]
labels = ["Even" if x % 2 == 0 else "Odd" for x in numbers]
print(labels)

# Student Grade Manager

# Step 1: Get student scores
student_scores = input("Enter student scores separated by commas: ")
scores = [int(score) for score in student_scores.split(",")]

# Step 2: Assign Grades using List Comprehension
grades = [
    "A" if score >= 90 else
    "B" if score >= 80 else
    "C" if score >= 70 else
    "D" if score >= 60 else
    "F"
    for score in scores
]

# Step 3: Filter Passing and Failing Students
passing_students = [score for score in scores if score >=60]
failing_students = [score for score in scores if score < 60]

# Step 4: Print Results
print("\n--- Student Grades ----")
for i, (score, grade) in enumerate(zip(scores, grades), start=1):
    print(f"Student {i}: Score = {score}, Grade = {grade}")

print("\n--- Passing and Failing Students ---")
print("Passing Students:", passing_students)
print("Failing Students:", failing_students)
