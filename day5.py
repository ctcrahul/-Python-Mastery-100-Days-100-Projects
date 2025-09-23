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
