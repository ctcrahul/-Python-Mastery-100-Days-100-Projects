# Simple To-Do List Application in Python

tasks = []

def show_menu():
    print("\n===== TO-DO LIST MENU =====")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Delete Task")
    print("4. Exit")

while True:
    show_menu()
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        if len(tasks) == 0:
            print("\nNo tasks yet! 🎉")
        else:
            print("\nYour Tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")

    elif choice == "2":
        task = input("Enter new task: ")
        tasks.append(task)
        print(f"✅ Task '{task}' added!")

    elif choice == "3":
        if len(tasks) == 0:
            print("No tasks to delete.")
        else:
            try:
                task_num = int(input("Enter task number to delete: "))
                if 1 <= task_num <= len(tasks):
                    removed = tasks.pop(task_num - 1)
                    print(f"🗑 Task '{removed}' deleted!")
                else:
                    print("❌ Invalid task number.")
            except ValueError:
                print("⚠ Enter a valid number!")

    elif choice == "4":
        print("Goodbye! 👋")
        break

    else:
        print("⚠ Invalid choice! Please enter 1-4.")
