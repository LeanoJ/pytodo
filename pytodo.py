import json
import os
from colorama import init, Fore, Style

tasks = []

# Adds a new task with the given description.
# Fügt eine neue Aufgabe mit der angegebenen Beschreibung hinzu.
def add_task(description):
    tasks.append({"description": description, "completed": False, "priority": None, "due_date": None})
    save_tasks()

# Prints text in a specified color.
# Druckt Text in einer angegebenen Farbe.
def colored_print(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

# Lists all tasks with their status, priority, and due date.
# Listet alle Aufgaben mit ihrem Status, ihrer Priorität und ihrem Fälligkeitsdatum auf.
def list_tasks():
    if not tasks:
        colored_print("No tasks available.", Fore.YELLOW)
        return
    for i, task in enumerate(tasks):
        status = "✓" if task["completed"] else " "
        priority = f"[{task['priority']}]" if task["priority"] else ""
        due_date = f"(Due: {task['due_date']})" if task["due_date"] else ""
        color = Fore.GREEN if task["completed"] else Fore.WHITE
        if not task["completed"] and task["priority"] == "high":
            color = Fore.RED
        elif not task["completed"] and task["priority"] == "medium":
            color = Fore.YELLOW
        colored_print(f"{i+1}. [{status}] {task['description']} {priority} {due_date}", color)

# Removes a task by its ID.
# Entfernt eine Aufgabe anhand ihrer ID.
def remove_task(task_id):
    if 1 <= task_id <= len(tasks):
        tasks.pop(task_id - 1)
        save_tasks()
    else:
        colored_print("Invalid task number.", Fore.RED)
        
# Marks a task as completed by its ID.
# Markiert eine Aufgabe anhand ihrer ID als erledigt.
def complete_task(task_id):
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1]["completed"] = True
        save_tasks()
    else:
        colored_print("Invalid task number.", Fore.RED)

# Adds a priority to a task by its ID.
# Fügt einer Aufgabe anhand ihrer ID eine Priorität hinzu.
def add_priority(task_id, priority):
    if priority.lower() not in ['high', 'medium', 'low']:
        colored_print("Invalid priority level.", Fore.RED)
        return
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1]["priority"] = priority.lower()
        save_tasks()
    else:
        colored_print("Invalid task number.", Fore.RED)

# Removes the priority from a task by its ID.
# Entfernt die Priorität einer Aufgabe anhand ihrer ID.
def remove_priority(task_id):
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1]["priority"] = None
        save_tasks()
    else:
        colored_print("Invalid task number.", Fore.RED)

# Adds a due date to a task by its description.
# Fügt einer Aufgabe anhand ihrer Beschreibung ein Fälligkeitsdatum hinzu.
def add_due_date(task_description, due_date):
    for task in tasks:
        if task["description"] == task_description:
            task["due_date"] = due_date
            save_tasks()
            return
    colored_print("Task not found.", Fore.RED)

# Removes the due date from a task by its ID.
# Entfernt das Fälligkeitsdatum einer Aufgabe anhand ihrer ID.
def remove_due_date(task_id):
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1]["due_date"] = None
        save_tasks()
    else:
        colored_print("Invalid task number.", Fore.RED)

# Saves the current tasks to a JSON file.
# Speichert die aktuellen Aufgaben in einer JSON-Datei.
def save_tasks():
    with open("pytodo.json", "w") as file:
        json.dump(tasks, file, indent=4)
    colored_print("Tasks saved successfully.", Fore.GREEN)

# Loads tasks from a JSON file if it exists.
# Lädt Aufgaben aus einer JSON-Datei, falls diese existiert.
def load_tasks():
    if os.path.exists("pytodo.json"):
        with open("pytodo.json", "r") as file:
            global tasks
            tasks = json.load(file)
        colored_print("Tasks loaded successfully.", Fore.GREEN)
    else:
        colored_print("No saved tasks found.", Fore.YELLOW)

# Prints the menu options.
# Druckt die Menüoptionen.
def print_menu():
    colored_print("\n=== TODO List Manager ===", Fore.CYAN)
    colored_print("1. Add new task", Fore.CYAN)
    colored_print("2. List all tasks", Fore.CYAN)
    colored_print("3. Remove task", Fore.CYAN)
    colored_print("4. Mark task as complete", Fore.CYAN)
    colored_print("5. Add priority to task", Fore.CYAN)
    colored_print("6. Remove priority from task", Fore.CYAN)
    colored_print("7. Add due date to task", Fore.CYAN)
    colored_print("8. Remove due date from task", Fore.CYAN)
    colored_print("0. Exit", Fore.CYAN)
    colored_print("=====================", Fore.CYAN)

# Main loop for the menu.
# Hauptschleife für das Menü.
def menu_loop():
    print_menu()
    while True:
        choice = input("\nEnter your choice (0-8) or 'm' for menu: ")
        
        if choice.lower() == 'm':
            print_menu()
            continue
        elif choice == "0":
            colored_print("Goodbye!", Fore.CYAN)
            break
        elif choice == "1":
            task = input("Enter task description: ")
            add_task(task)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            list_tasks()
            task_id = input("Enter task number to remove: ")
            try:
                remove_task(int(task_id))
            except ValueError:
                colored_print("Please enter a valid number.", Fore.RED)
        elif choice == "4":
            list_tasks()
            task_id = input("Enter task number to mark as complete: ")
            try:
                complete_task(int(task_id))
            except ValueError:
                colored_print("Please enter a valid number.", Fore.RED)
        elif choice == "5":
            list_tasks()
            task_id = input("Enter task number to add priority: ")
            priority = input("Enter priority (high/medium/low): ")
            try:
                add_priority(int(task_id), priority)
            except ValueError:
                colored_print("Please enter a valid number.", Fore.RED)
        elif choice == "6":
            list_tasks()
            task_id = input("Enter task number to remove priority: ")
            try:
                remove_priority(int(task_id))
            except ValueError:
                colored_print("Please enter a valid number.", Fore.RED)
        elif choice == "7":
            task = input("Enter task description: ")
            due_date = input("Enter due date (e.g., YYYY-MM-DD): ")
            add_due_date(task, due_date)
        elif choice == "8":
            list_tasks()
            task_id = input("Enter task number to remove due date: ")
            try:
                remove_due_date(int(task_id))
            except ValueError:
                colored_print("Please enter a valid number.", Fore.RED)
        else:
            colored_print("Invalid choice. Please try again.", Fore.RED)

# Main function to initialize and start the program.
# Hauptfunktion zum Initialisieren und Starten des Programms.
def main():
    init(autoreset=True)
    load_tasks()
    try:
        menu_loop()
    except KeyboardInterrupt:
        colored_print("\nGoodbye!", Fore.CYAN)

if __name__ == "__main__":
    main()