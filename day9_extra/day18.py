
"""                            Day18.py

                      Mini To-Do App: JSON Files
                          

"""

import json

with open('json_data', 'r') as file:
  tasks = json.load(file)
  print(tasks)

import json

tasks = [
    {"task": "Complete Project", "status": "Incomplete"}
]

with open('tasks.json', 'w') as file:
  json.dump(tasks, file, indent=2)

import json

with open('tasks.json', 'r') as file:
  tasks = json.load(file)

tasks.append({"task": "Learn Python 2", "status": "Incomplete"})

with open('tasks.json', 'w') as file:
  json.dump(tasks, file, indent=2)

# Mini To-Do App using JSON
import json
import os

# File for storing tasks
TASK_FILE = 'my_tasks.json'

# Ensure the tasks file exists
if not os.path.exists(TASK_FILE):
  with open(TASK_FILE, 'w') as file:
    json.dump([], file)

# Step 1: Load Tasks from JSON
def load_tasks():
  with open(TASK_FILE, 'r') as file:
    return json.load(file)

# Step 2: Save Tasks to JSON
def save_tasks(tasks):
  with open(TASK_FILE, 'w') as file:
    json.dump(tasks, file, indent=2)

# Step 3: Add a new task
def add_task():
  task_name = input("Enter the task name: ").strip()
  tasks = load_tasks()
  tasks.append({"task": task_name, "status": "Incomplete"})
  save_tasks(tasks)
  print(f'Task "{task_name}" added successfully!')

# Step 4: View All Tasks
# Step 5: Update Task Status
def update_status():
  tasks = load_tasks()
  view_tasks()
  try:
    task_index = int(input("Enter the task number to update: ")) - 1
    if 0 <= task_index < len(tasks):
      new_status = input("Enter the new status (Complete/Incomplete): ").strip()
      tasks[task_index]['status'] = new_status
      save_tasks(tasks)
      print(f'Task "{deleted_task["task"]}" deleted successfully!')
    else:
  print("2. View all tasks")
