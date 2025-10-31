import matplotlib.pyplot as plt
from collections import defaultdict

expenses = []

def set_savings_goal():
	goal = float(input("Enter your monthly savings goal: "))
	print(f"Your savings goal is set to ${goal:.2f}")
	return goal

def add_income():
	income = float(input("Enter your income amount: "))
	print(f"Income of ${income:.2f} added.")
	return income

def add_expense():
	category = input("Enter expense category (eg, Food, Housing,..): ").capitalize()
	amount = float(input("Enter expense amount: "))
	expenses.append({"category": category, "amount": amount})
	print(f"Expense of ${amount:.2f} added under {category}")

def view_expenses_by_category():
	category_totals = defaultdict(float)
	for expense in expenses:
		category_totals[expense["category"]] += expense["amount"]
	print("\nExpenses by Category:")
	for category, total in category_totals.items():
		print(f"{category}: ${total:.2f}")

def calculate_remaining_budget(income, expenses):
    total_expenses = sum(expense["amount"] for expense in expenses)
    remaining = income - total_expenses
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Remaining Budget: ${remaining:.2f}")
    return remaining


def check_savings_goal(remaining, goal):
    if remaining >= goal:
        print(f"Congratulations! You have met your savings goal with ${remaining - goal:.2f} extra.")
    else:
        print(f"You are ${goal - remaining:.2f} away from your savings goal.")


def plot_expenses():
    category_totals = defaultdict(float)
    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]
    
    labels = category_totals.keys()
    sizes = category_totals.values()
    plt.pie(sizes, labels=labels, autopct="%1.1f%%")
    plt.title("Expense Distribution")
    plt.show()


def main():
    print("Welcome to the Personal Budget Planner!")
    goal = set_savings_goal()
    income = add_income()
    
    while True:
        print("\nOptions:")
        print("1. Add Expense")
        print("2. View Expenses by Category")
        print("3. Calculate Remaining Budget")
        print("4. Check Savings Goal")
        print("5. Visualize Expenses")
        print("6. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses_by_category()
        elif choice == "3":
            calculate_remaining_budget(income, expenses)
        elif choice == "4":
            remaining = calculate_remaining_budget(income, expenses)
            check_savings_goal(remaining, goal)
        elif choice == "5":
            plot_expenses()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()	

















