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

