"""                                                            Day = 43

											           	  Personal Budget Planner
"""



import matplotlib.pyplot as plt
from collections import defaultdict
import os

# Store expenses globally
expenses = []

# Function to set savings goal
def set_savings_goal():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    print("Welcome to your Personal Budget Planner!")
    goal = float(input("Enter your monthly savings goal (e.g., 1500.00): $"))
    print(f"Your savings goal is set to ${goal:.2f}\n")
    return goal

# Function to add income
def add_income():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    print("Let's add your income details")
    income = float(input("Enter your income amount (e.g., 3500.00): $"))
    print(f"Income of ${income:.2f} added.\n")
    return income

# Function to add expense
def add_expense():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    print("Let's add a new expense")
    category = input("Enter expense category (e.g., Food, Housing): ").capitalize()
    amount = float(input(f"Enter amount for {category}: $"))
    expenses.append({"category": category, "amount": amount})
    print(f"Expense of ${amount:.2f} added under {category}.\n")

# Function to view expenses by category
def view_expenses_by_category():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    category_totals = defaultdict(float)
    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]
    print("Expenses by Category:")
    for category, total in category_totals.items():
        print(f"{category}: ${total:.2f}")
    print()

# Function to calculate remaining budget
def calculate_remaining_budget(income, expenses):
    total_expenses = sum(expense["amount"] for expense in expenses)
    remaining = income - total_expenses
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Remaining Budget: ${remaining:.2f}\n")
    return remaining

# Function to check savings goal
def check_savings_goal(remaining, goal):
    if remaining >= goal:
        print(f"Congratulations! You've met your savings goal with ${remaining - goal:.2f} extra!\n")
    else:
        print(f"You are ${goal - remaining:.2f} away from reaching your savings goal.\n")

# Function to plot expense distribution
def plot_expenses():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the terminal screen
    category_totals = defaultdict(float)
    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]
    
    labels = category_totals.keys()
    sizes = category_totals.values()
    
    # Pie chart style
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", colors=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6'])
    plt.title("Expense Distribution", fontsize=14)
    plt.axis('equal')  # Equal aspect ratio ensures the pie is drawn as a circle.
    plt.show()

# Main function to drive the budget planner
def main():
    while True:
        print("Budget Planner Menu:")
        print("1. Add Expense")
        print("2. View Expenses by Category")
        print("3. Calculate Remaining Budget")
        print("4. Check Savings Goal")
        print("5. Visualize Expenses")
        print("6. Exit\n")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses_by_category()
        elif choice == "3":
            income = add_income()  # Ensure user has income entered
            calculate_remaining_budget(income, expenses)
        elif choice == "4":
            income = add_income()  # Ensure user has income entered
            remaining = calculate_remaining_budget(income, expenses)
            goal = set_savings_goal()  # Ensure savings goal is set
            check_savings_goal(remaining, goal)
        elif choice == "5":
            plot_expenses()
        elif choice == "6":
            print("Goodbye! See you soon!")
            break
        else:
            print("Invalid choice, please try again.\n")

if __name__ == "__main__":
    main()
