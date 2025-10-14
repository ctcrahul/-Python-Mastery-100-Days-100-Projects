
"""                                                Day26.py

                                   Secure User Profile App: Encapsulation

"""

class User:
  def __init__(self, username, password):
    self.username = username
    self.__password = password

  def get_password(self):
    return "*****"
a
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

#Main Programaa
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
