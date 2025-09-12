# Smart Expense Tracker


import csv
from datetime import datetime

FILE_NAME = "expenses.csv"


# Initialize CSV with headers if not exists
def init_file():
    try:
        with open(FILE_NAME, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Category", "Amount", "Note"])
    except FileExistsError:
        pass

# Add expense
def add_expense():
    date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter category (Food, Travel, Shopping, etc.): ")
    amount = float(input("Enter amount: "))
    note = input("Enter note (optional): ")

    with open(FILE_NAME, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, note])

    print("✅ Expense Added!")
# Show report
def show_report():
    total = 0
    with open(FILE_NAME, "r") as file:
        reader = csv.DictReader(file)
        print("\n--- Expense Report ---")
        for row in reader:
            print(f"{row['Date']} | {row['Category']} | ₹{row['Amount']} | {row['Note']}")
            total += float(row["Amount"])
    print(f"\n💰 Total Expenses: ₹{total}")

# Main menu
def main():
    init_file()
    while True:
        print("\n1. Add Expense\n2. Show Report\n3. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_report()
        elif choice == "3":
            print("👋 Exiting... Bye!")
            break
        else:
            print("❌ Invalid choice, try again!")



if __name__ == "__main__":
    main()


# Why Best for Project?
# ✅ Simple but useful in real life
# ✅ File handling + CSV ka use
# ✅ Good for college/demo project
# ✅ Easy to extend (charts, GUI, database)



