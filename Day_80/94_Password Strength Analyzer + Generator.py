# Project 94: Password Strength Analyzer + Generator

import re
import random
import string

# -----------------------------
# Password Strength Checker
# -----------------------------
def check_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add at least one digit.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        feedback.append("Add at least one special character.")

    strength_levels = {
        1: "Very Weak",
        2: "Weak",
        3: "Moderate",
        4: "Strong",
        5: "Very Strong"
    }

    return strength_levels.get(score, "Very Weak"), feedback

# -----------------------------
# Password Generator
# -----------------------------
def generate_password(length=12):
    if length < 8:
        raise ValueError("Password length should be at least 8")

    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    password = "".join(random.choice(characters) for _ in range(length))
    return password

# -----------------------------
# MAIN MENU
# -----------------------------
def main():
    while True:
        print("\n--- Password Tool ---")
        print("1. Check Password Strength")
        print("2. Generate Strong Password")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            password = input("Enter password: ")
            strength, feedback = check_strength(password)
            print(f"\nStrength: {strength}")
            if feedback:
                print("Suggestions:")
                for f in feedback:
                    print("-", f)

        elif choice == "2":
            length = int(input("Enter password length: "))
            password = generate_password(length)
            print("\nGenerated Password:", password)

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
