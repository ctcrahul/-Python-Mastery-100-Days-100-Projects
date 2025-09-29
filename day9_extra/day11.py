# -*- coding: utf-8 -*-
"""Day11.py

Safe Calculator: Exception Handling

"""

try:
  num = int(input("Enter a number:"))
  result = 10 / num
  print("Result: ", result)
except ZeroDivisionError:
  print("Error: Division by zero is not allowed.")
except ValueError:
  print("Error: Invalid input. Please enter a valid number.")

try:
  # Code that might raise an exception
except ExceptionType:
  # Code to handle the exception
else:
  # Execute if no exception occurs
finally:
  # Always execute, even if an exception occurs

try:
  num = int(input("Enter a number:"))
  result = 10 / num
except ZeroDivisionError:
  print("Error: Division by zero is not allowed.")
else:
  print("No exception occurred. Result: ", result)
finally:
  print("Finally block executed. Program Ended")

try:
  num = int(input("Enter a number:"))
  result = 10 / num
except (ZeroDivisionError, ValueError):
  print("Error: Division by zero or Invalid Input")

def withdraw(amount):
  if amount < 0:
    raise ValueError("Invalid withdrawal amount - Amount cannot be negative")
  print(f"You have withdrawn ${amount}")

try:
  withdraw(-50)
except ValueError as e:
  print(e)

# Safe Calculator

# Step 1: Define Calculator Functions
def add(x, y):
  return x + y

def subtract(x, y):
  return x - y

def multiply(x, y):
  return x * y

def divide(x, y):
  if y == 0:
    raise ZeroDivisionError("Cannot divide by zero")
  return x / y

# Step 2: Display Menu
def show_menu():
  print("\n--- Safe Calculator Menu ---")
  print("1. Add")
  print("2. Subtract")
  print("3. Multiply")
  print("4. Divide")
  print("5. Exit")

# Step 3: Main Program
while True:
  show_menu()
  choice = input("Enter your choice (1-5): ")

  if choice == '5':
    print("Exiting the calculator. Goodbye!")
 

