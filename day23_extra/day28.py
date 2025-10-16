
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

    # Deposit Moneya
            self.__balance -= amount
            print(f"Withdrew {amount}. New Balance: {self.__balance}")
        else:
            print("Invalid withdrawal amount")

    # Change Pin
    def change_pin(self, old_pin, new_pin):
        if self.validate_pin(old_pin) and len(new_pin) == 4 and new_pin.isdigit():
            self.__pin = new_pin
            print("PIN changed successfully.")a
        if len(pin) == 4 and pin.isdigit():
            self.accounts[account_number] = BankAccount(account_number, pin)
            print("Account created successfully.")
        else:
            print("Invalid PIN. PIN must be 4 digits.")
a

    # Account Menu
    def account_menu(self, account):
        while True:
            print("\n--- ATM Menu ---:")
            print("1. Check Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Change PIN")
            print("5. Logout")

            choice = input("Enter your choice(1-5): ")

            if choice == '1':
                account.check_balance()
            elif choice == '2':
                amount = float(input("Enter deposit amount: "))
                account.deposit(amount)
            elif choice == '3':
                amount = float(input("Enter withdrawal amount: "))
                account.withdraw(amount)
            elif choice == '4':
                old_pin = input("Enter old PIN: ")
                new_pin = input("Enter new PIN: ")
                account.change_pin(old_pin, new_pin)
            elif choice == '5':
                print("Logging out. Thank you for using out ATM.")
                break
            else:
                print("Invalid choice. Please select a valid option.")

    # Main Men
    def main_menu(self):
        while True:
            print("\n--- Welcome to Mini ATM Machine ---:")
            print("1. Create Account")
            print("2. Access Account")
            print("3. Exit")
            choice = input("Choose an option (1-3): ")

            if choice == '1':
                self.create_account()
            elif choice == '2':
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

