
"""                                Day15.py

                        Recipe Viewer App: Reading Files


"""

with open("sample.txt", "r") as file:
  content = file.read()
  print(content)

with open("sample.txt", "r") as file:
  for line in file:
    print(line.strip())

with open("sample.txt", "r") as file:
  lines = file.readlines()
  for line in lines:
    print(line.strip())

try:
  with open("sample.txt", "r") as file:
    content = file.read()
    print(content)
except FileNotFoundError:
  print("File not found.")

# Recipe Viewer App

# Step 1: Load Recipes from File
def load_recipes(file_path):
  try:
    with open(file_path, "r") as file:
      content = file.read()
      recipes = content.split("\n\n")
      recipe_dict = {}
      for recipe in recipes:
        lines = recipe.split("\n")
  print("2. 
