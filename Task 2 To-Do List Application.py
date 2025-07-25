import os

FILENAME = "todo.txt"

def load_tasks():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r") as file:
        return [line.strip() for line in file.readlines()]

def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        for task in tasks:
            file.write(task + "\n")

def show_menu():
    print("\n==== To-Do List Menu ====")
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Delete Task")
    print("4. Edit Task")
    print("5. Exit")

def view_tasks(tasks):
    if not tasks:
        print("No tasks found.")
    else:
        print("\n📋 Your Tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}. {task}")

def add_task(tasks):
    task = input("Enter the new task: ").strip()
    if task:
        tasks.append(task)
        print("✅ Task added.")
    else:
        print("⚠️ Task cannot be empty.")

def delete_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter the task number to delete: ")) - 1
        if 0 <= index < len(tasks):
            removed = tasks.pop(index)
            print(f"❌ Deleted task: {removed}")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def edit_task(tasks):
    view_tasks(tasks)
    try:
        index = int(input("Enter the task number to edit: ")) - 1
        if 0 <= index < len(tasks):
            new_task = input("Enter the new task text: ").strip()
            if new_task:
                old_task = tasks[index]
                tasks[index] = new_task
                print(f"✏️ Task updated: '{old_task}' → '{new_task}'")
            else:
                print("⚠️ Task cannot be empty.")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")

def main():
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == '1':
            view_tasks(tasks)
        elif choice == '2':
            add_task(tasks)
        elif choice == '3':
            delete_task(tasks)
        elif choice == '4':
            edit_task(tasks)
        elif choice == '5':
            save_tasks(tasks)
            print("👋 Exiting... Tasks saved.")
            break
        else:
            print("⚠️ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
