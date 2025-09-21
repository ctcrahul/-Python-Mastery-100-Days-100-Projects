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




original[2].append(5)
print(copy1)
# [1, 2, [3, 4, 5]] — nested list changed!
print(copy4)
# [1, 2, [3, 4]] — unchanged



original = [1, 2, [3, 4]]

# 1. Slice (shallow copy)
copy1 = original[:]

# 2. .copy() method (shallow copy)
copy2 = original.copy()

# 3. Using list() (shallow copy)
copy3 = list(original)

# 4. deepcopy (deep copy)
import copy
copy4 = copy.deepcopy(original)





original = [1, 2, [3, 4]]

# 1. Slice (shallow copy)
copy1 = original[:]

# 2. .copy() method (shallow copy)
copy2 = original.copy()

# 3. Using list() (shallow copy)
copy3 = list(original)

# 4. deepcopy (deep copy)
import copy
copy4 = copy.deepcopy(original)



original[2].append(5)
print(copy1)
# [1, 2, [3, 4, 5]] — nested list changed!
print(copy4)
# [1, 2, [3, 4]] — unchanged






original[2].append(5)
print(copy1)
# [1, 2, [3, 4, 5]] — nested list changed!
print(copy4)
# [1, 2, [3, 4]] — unchanged



