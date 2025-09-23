Python Interview Questions:

Ready to test your Python skills? Let’s get started! 💻


1. How to check if a string is a palindrome?

def is_palindrome(s):
    return s == s[::-1]

print(is_palindrome("madam"))  # True
print(is_palindrome("hello"))  # False


2. How to find the factorial of a number using recursion?

def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))  # 120

3. How to merge two dictionaries in Python?

dict1 = {'a': 1, 'b': 2}
dict2 = {'c': 3, 'd': 4}

# Method 1 (Python 3.5+)
merged_dict = {**dict1, **dict2}

# Method 2 (Python 3.9+)
merged_dict = dict1 | dict2

print(merged_dict)





4. How to find the intersection of two lists?

list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]

intersection = list(set(list1) & set(list2))
print(intersection)  # [3, 4]


5. How to generate a list of even numbers from 1 to 100?

even_numbers = [i for i in range(1, 101) if i % 2 == 0]
print(even_numbers)



6. How to find the longest word in a sentence?

def longest_word(sentence):
    words = sentence.split()
    return max(words, key=len)

print(longest_word("Python is a powerful language"))  # "powerful"



