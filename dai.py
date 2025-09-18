# Python Mastery Projects
print("Hlo World")

# MINI PROJECTS

# To DO List
todo = []
todo.append("Buy milk")
todo.append("Study Python")
print(todo)


# Number Guessing Game 

import random
num = random.randint(1, 10)
guess = int(input("Guess a number (1-10): "))
if guess == num:
    print("Correct!")
else:
    print("Wrong, number was", num)
