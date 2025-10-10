
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
  name = input("Enter your name: ").strip()
  if name in accounts:
    account = accounts[name]
    while True:
      print("\n--- Account Menu ---")
      print("1. Deposit")
      print("2. Withdraw")
      print("3. Show Details")
      print("4. Exit")
      choice = input("Enter your choice(1-4): ")

      if choice == '1':
        amount = float(input("Enter deposit amount: "))
        account.deposit(amount)
    print("Account not found. Please create an account first.")

# Main Menu
while True:
  print("\n--- Bank Account Simulator ---")
  print("1. Create Account")
  print("2. Access Account")
  print("3. Exit")
  choice = input("Enter your choice(1-3): ")

  print(accounts)

  if choice == '1':
    create_account()
  elif choice == '2':
    access_account()
  elif choice == '3':
    print("Exiting the program. Goodbye!")
    break
  else:
    print("Invalid choice. Please select a valid option.")
