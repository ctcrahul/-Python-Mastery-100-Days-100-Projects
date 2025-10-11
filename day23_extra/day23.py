
"""                                                  Day23.py

                                  Library Management System: Constructors & Methods


"""

class Book:
  def __init__(self, title, author):
    self.title = title
    self.author = author

  def display_info(self):
    print(f"Title: {self.title}")
    print(f"Author: {self.author}")

# Create an object
book1 = Book("1984", "George Orwell")
book1.display_info()

class BankAccount:
  def __init__(self, owner, balance=0):
    self.owner = owner
    self.balance = balance

  def deposit(self, amount):
    self.balance += amount
    print(f"Deposited ${amount}. New balance: ${self.balance}")

account = BankAccount("John Doe", 1000)
account.deposit(500)

class Utility:
  app_version = "1.0"

  @classmethod
  def get_version(cls):
    print(f"App Version: {cls.app_version}")

  @staticmethod
  def greet():z
account.deposit(500)
print(f"Account Balance: ${account.get_balance()}")

# Library Management System
z
class Library:
  def __init__(self):
    self.books = []

  def add_book(self, title, author):
    new_book = Book(title, ax
        book.display_info()

  # Borrow a book
  def borrow_book(self, title):
    for book in self.books:
      if book.title == title and not book.is_borrowed:
        book.is_borrowed = True
        print(f"Book '{title}' has been borrowed. Enjoy Reading")
        return
    print(f"Book '{title}' is not available for borrowing.")


  # Return a book
  def return_book(self, title):
    for book in self.books:
      if book.title == title and book.is_borrowed:
        book.is_borrowed = False
        print(f"Book '{title}' has been returned.")
        return
    print(f"Book '{title}' is not in the library.")

# Main Program
library = Library()

while True:
  print("\n--- Library Management System ---")
  print("1. Add Book")
  print("2. View Books")
  print("3. Borrow Book")
  print("4. Return Book")
  print("5. Exit")

  choice = input("Enter your choice (1-5): ").strip()

  if choice == "1":
    title = input("Enter book title: ").strip()
    author = input("Enter author name: ").strip()
    library.add_book(title, author)
  elif choice == "2":
    library.view_books()
  elif choice == "3":
    title = input("Enter book title to borrow: ").strip()
    library.borrow_book(title)
  elif choice == "4":
    title = input("Enter book title to return: ").strip()
    library.return_book(title)
  elif choice == "5":
    print("Exiting the Library Management System. Goodbye!")
    break
  else:
    print("Invalid choice. Please select a valid option (1-5).")
