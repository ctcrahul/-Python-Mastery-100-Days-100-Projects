
"""                                            Day28.py

                                 Mini ATM Machine: Final OOP Project


"""

# The Mini ATM Machine will allow users to:

# Authenticate with PINs securely.
# Check account balance.
# Deposit money.
# Withdraw money with balance validation.
# Change PIN.
# Exit securely.

# Classes Overview:a
# Encapsulation: Secure PIN handling and balance access.
# Static Method: For utility tasks like PIN validation.
# Class Method: To maintain account-level settings.
# Polymorphism: Flexibility in transaction operations.

# Mini ATM Machine

class BankAccount:
    def __init__(self, account_number, pin, balance=0):
        self.account_number = account_numbera
    # Check Balance
    def check_balance(self):
        print(f"Current Balance: {self.__balance}")

    # Deposit Moneyaq
                self.authenticate_account()
            elif choice == '3':
                print("Thank you for using Mini ATM Machine. Goodbye!")
                break
            else:
                print("Invalid Choice. Please try again")


# Start the ATM System
if __name__ == "__main__":
  atm = ATM()
  atm.main_menu()

