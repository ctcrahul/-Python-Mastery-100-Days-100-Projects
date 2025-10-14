
"""                                                Day26.py

                                   Secure User Profile App: Encapsulation

"""

class User:
  def __init__(self, username, password):
    self.username = username
    self.__password = password

  def get_password(self):
    return "*****"

  def set_password(self, new_password):
    if len(new_password) >= 8:z
print(user.get_password())
user.set_password("NewPassword")
z}")

user = UserProfile("Alice", "alice@example.com", "pass1234")
user.show_profile()

class Account:
  def __init__(self, balance):
    self.__balance = balance

  def get_balance(self):z
print(account.get_balance())

class User:
  def __init__(self, username):z


  def get_password(self):
    return self.__password

user = User("Alice")
user.set_password("password123")
print(user.get_password())z
  def get_email(self):
    return self._email
zz

#Main Programa
  username = input("Enter username to update email: ")
  for user in users:
    if user.username == username:
      new_email = input("Enter new email: ")
      user.set_email(new_email)
      return
  print("User not found")

# Main Menu

while True:
  print("\n--- Secure User Profile App ---")
  print("1. Create User")
  print("2. View All Profiles")
  print("3. Update Email")
  print("4. Exit")

  choice = input("Enter your choice(1-4): ")

  if choice == "1":
    create_user()
  elif choice == "2":
    view_profiles()
  elif choice == "3":
    update_email()
  elif choice == "4":
    print("Exiting the program")
    break
  else:
    print("Invalid choice. Please try again")
