
"""                                       Day22.py

                                Bank Account Simulator: Classes & Objects

"""



    if amount > 0 and amount <= self.balance:
      self.balance -= amount,
    print(f"Account Balance: ${self.balance}")


# Main Program
accounts = {}

def create_account():
  name = input("Enter account holder's name: ").strip()
  initial_deposit = float(input("Enter initial Deposit Amount: "))
  account = BankAccount(name, initial_deposit)
  accounts[name] = account
  print("Account created successfully!")

def access_account():
  name = input("Enter your name: ").
    create_account()
  elif choice == '2':
    access_account()
  elif choice == '3':
    print("Exiting the program. Goodbye!")
    break
  else:
    print("Invalid choice. Please select a valid option.")
