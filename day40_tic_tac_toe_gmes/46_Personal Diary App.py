"""                                                        Day = 46

                                                        Personal Diary App
"""

import os
import getpass
from datetime import datetime
from cryptography.fernet import Fernet # type: ignore

# Encryption Setup

# Generate and save a secret key for encryption
def generate_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

# Load the encryption key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt the diary entry content
def encrypt_text(text):
    key = load_key()
    cipher = Fernet(key)
    return cipher.encrypt(text.encode())

# Decrypt the content of a diary entry
def decrypt_text(encrypted_text):
    key = load_key()
    cipher = Fernet(key)
    return cipher.decrypt(encrypted_text).decode()

# Diary Function: Creating a new diary entry
def create_entry():
    title = input("What shall we call this moment? (Title): ")
    print("Let your thoughts flow... \n")
    content = input("Write freely, express your feelings: ")
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Encrypt content before saving it
    encrypted_content = encrypt_text(content)

    os.makedirs("entries", exist_ok=True)

    # Save the entry to a file
    file_name = f"{date}_{title}.txt"
    with open(os.path.join("entries", file_name), "wb") as file:
        file.write(encrypted_content)
    print(f"\n 'Your Diary Entry - {title}' has been preserved in time! ")

# Diary Function: Listing all existing entries
def list_entries():
    os.makedirs("entries", exist_ok=True)
    entries = os.listdir("entries")
    if entries:
        print("\nHere are your cherished memories: ")
        for index, entry in enumerate(entries, start=1):
            print(f"{index}. {entry}")
    else:
        print("Your diary is still a blank canvas. Start writing today.")

# Diary Function: Reading an existing entry
def read_entry():
    list_entries()
    file_name = input("\nWhich entry would you like to read? (Enter the filename): ")
    file_path = os.path.join("entries", file_name)
    
    try:
        with open(file_path, "rb") as file:
            encrypted_content = file.read()
        content = decrypt_text(encrypted_content)
        print("\n Your Diary Entry: ")
        print(content)
    except FileNotFoundError:
        print("This entry does not exist. Perhaps it was a dream.")

# Authentication: Simple password authentication
def authenticate():
    correct_password = "PassW0rd"  # The secret password for access
    password = getpass.getpass("Enter the sacred password to enter your realm: ")
    if password == correct_password:
        print("Access Granted! Welcome to your private space.")
        return True
    else:
        print("Access Denied. Only trusted souls may enter.")
        return False

# Main App: User interface for interacting with the diary
def main():
    generate_key()
    if authenticate():
        while True:
            print("\nChoose your path: ")
            print("1. Create a New Diary Entry")
            print("2. View All Entries")
            print("3. Read an Entry")
            print("4. Exit the Realm")
            choice = input("Enter your choice: ")
            if choice == "1":
                create_entry()
            elif choice == "2":
                list_entries()
            elif choice == "3":
                read_entry()
            elif choice == "4":
                print("Farewell, until next time. ")
                break
            else:
                print("Hmm, that doesn't seem right. Try again.")

if __name__ == "__main__":
    main()


############################################################################################################################################################################
                                                       Thanks for visting keep support us
############################################################################################################################################################################


                break
            else:
                print("Hmm, that doesn't seem right. Try again.")

if __name__ == "__main__":
    main()


            if choice == "1":
                create_entry()
            elif choice == "2":
                list_entries()
            elif choice == "3":
                read_entry()
            elif choice == "4":
                print("Farewell, until next time. 🌙")

# Main App: User interface for interacting with the diary
def main():
    generate_key()
    if authenticate():
        while True:
            print("\nChoose your path: ")
            print("1. Create a New Diary Entry")
            print("2. View All Entries")
            print("3. Read an Entry")
            print("4. Exit the Realm")
            choice = input("Enter your choice: ")


# Authentication: Simple password authentication
def authenticate():
    correct_password = "PassW0rd"  # The secret password for access
    password = getpass.getpass("Enter the sacred password to enter your realm: ")
    if password == correct_password:
        print("Access Granted! Welcome to your private space.")
        return True
    else:
        print("Access Denied. Only trusted souls may enter.")
        return False


    try:
        with open(file_path, "rb") as file:
            encrypted_content = file.read()
        content = decrypt_text(encrypted_content)
        print("\n🌙 Your Diary Entry: ")
        print(content)
    except FileNotFoundError:
        print("This entry does not exist. Perhaps it was a dream.")



# Diary Function: Reading an existing entry
def read_entry():
    list_entries()
    file_name = input("\nWhich entry would you like to read? (Enter the filename): ")
    file_path = os.path.join("entries", file_name)
    

