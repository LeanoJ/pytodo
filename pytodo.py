import json
import os
from colorama import init, Fore, Style

tasks = []
language = "en"

# Dictionary for multilingual support
# Wörterbuch für mehrsprachige Unterstützung
translations = {
    "en": {
        "menu": "\n=== TODO List Manager ===",
        "add_task": "1. Add new task",
        "list_tasks": "2. List all tasks",
        "remove_task": "3. Remove task",
        "complete_task": "4. Mark task as complete",
        "add_priority": "5. Add priority to task",
        "remove_priority": "6. Remove priority from task",
        "add_due_date": "7. Add due date to task",
        "remove_due_date": "8. Remove due date from task",
        "search_tasks": "9. Search tasks",
        "edit_task": "10. Edit task",
        "sort_tasks": "11. Sort tasks",
        "filter_tasks": "12. Filter tasks",
        "exit": "0. Exit",
        "invalid_choice": "Invalid choice. Please try again.",
        "goodbye": "Goodbye!",
        "enter_choice": "Enter your choice (0-12) or 'm' for menu: ",
        "enter_task_description": "Enter task description: ",
        "enter_task_number": "Enter task number: ",
        "enter_priority": "Enter priority (high/medium/low): ",
        "enter_due_date": "Enter due date (e.g., YYYY-MM-DD): ",
        "enter_keyword": "Enter keyword to search for: ",
        "no_tasks": "No tasks available.",
        "task_not_found": "Task not found.",
        "invalid_task_number": "Invalid task number.",
        "invalid_priority": "Invalid priority level.",
        "tasks_saved": "Tasks saved successfully.",
        "tasks_loaded": "Tasks loaded successfully.",
        "no_saved_tasks": "No saved tasks found.",
        "enter_new_description": "Enter new description: ",
        "enter_sort_option": "Enter sort option (priority/due_date/status): ",
        "enter_filter_option": "Enter filter option (completed/not_completed/high/medium/low): ",
        "confirm_delete": "Are you sure you want to delete this task? (y/n): ",
        "delete_cancelled": "Task deletion cancelled."
    },
    "de": {
        "menu": "\n=== TODO-Listen-Manager ===",
        "add_task": "1. Neue Aufgabe hinzufügen",
        "list_tasks": "2. Alle Aufgaben auflisten",
        "remove_task": "3. Aufgabe entfernen",
        "complete_task": "4. Aufgabe als erledigt markieren",
        "add_priority": "5. Priorität zur Aufgabe hinzufügen",
        "remove_priority": "6. Priorität von Aufgabe entfernen",
        "add_due_date": "7. Fälligkeitsdatum zur Aufgabe hinzufügen",
        "remove_due_date": "8. Fälligkeitsdatum von Aufgabe entfernen",
        "search_tasks": "9. Aufgaben durchsuchen",
        "edit_task": "10. Aufgabe bearbeiten",
        "sort_tasks": "11. Aufgaben sortieren",
        "filter_tasks": "12. Aufgaben filtern",
        "exit": "0. Beenden",
        "invalid_choice": "Ungültige Wahl. Bitte versuchen Sie es erneut.",
        "goodbye": "Auf Wiedersehen!",
        "enter_choice": "Geben Sie Ihre Wahl ein (0-12) oder 'm' für Menü: ",
        "enter_task_description": "Aufgabenbeschreibung eingeben: ",
        "enter_task_number": "Aufgabennummer eingeben: ",
        "enter_priority": "Priorität eingeben (hoch/mittel/niedrig): ",
        "enter_due_date": "Fälligkeitsdatum eingeben (z.B. YYYY-MM-DD): ",
        "enter_keyword": "Schlüsselwort zur Suche eingeben: ",
        "no_tasks": "Keine Aufgaben verfügbar.",
        "task_not_found": "Aufgabe nicht gefunden.",
        "invalid_task_number": "Ungültige Aufgabennummer.",
        "invalid_priority": "Ungültige Prioritätsstufe.",
        "tasks_saved": "Aufgaben erfolgreich gespeichert.",
        "tasks_loaded": "Aufgaben erfolgreich geladen.",
        "no_saved_tasks": "Keine gespeicherten Aufgaben gefunden.",
        "enter_new_description": "Neue Beschreibung eingeben: ",
        "enter_sort_option": "Sortieroption eingeben (priorität/fälligkeitsdatum/status): ",
        "enter_filter_option": "Filteroption eingeben (erledigt/nicht_erledigt/hoch/mittel/niedrig): ",
        "confirm_delete": "Sind Sie sicher, dass Sie diese Aufgabe löschen möchten? (j/n): ",
        "delete_cancelled": "Aufgabenlöschung abgebrochen."
    }
}

# Function to get translated text based on the selected language
# Funktion zum Abrufen des übersetzten Textes basierend auf der ausgewählten Sprache
def t(key):
    return translations[language].get(key, key)

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
        colored_print(t("no_tasks"), Fore.YELLOW)
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

# Removes a task by its ID with confirmation.
# Entfernt eine Aufgabe anhand ihrer ID mit Bestätigung.
def remove_task(task_id):
    if 1 <= task_id <= len(tasks):
        confirm = input(t("confirm_delete")).strip().lower()
        if confirm == 'y':
            tasks.pop(task_id - 1)
            save_tasks()
        else:
            colored_print(t("delete_cancelled"), Fore.YELLOW)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)

# Marks a task as completed by its ID.
# Markiert eine Aufgabe anhand ihrer ID als erledigt.
def complete_task(task_id):
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1]["completed"] = True
        save_tasks()
    else:
        colored_print(t("invalid_task_number"), Fore.RED)

# Adds a priority to a task by its ID.
# Fügt einer Aufgabe anhand ihrer ID eine Priorität hinzu.
def add_priority(task_id, priority):
    if priority.lower() not in ['high', 'medium', 'low']:
        colored_print(t("invalid_priority"), Fore.RED)
        return
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1]["priority"] = priority.lower()
        save_tasks()
    else:
        colored_print(t("invalid_task_number"), Fore.RED)

# Removes the priority from a task by its ID.
# Entfernt die Priorität einer Aufgabe anhand ihrer ID.
def remove_priority(task_id):
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1]["priority"] = None
        save_tasks()
    else:
        colored_print(t("invalid_task_number"), Fore.RED)

# Adds a due date to a task by its ID.
# Fügt einer Aufgabe anhand ihrer ID ein Fälligkeitsdatum hinzu.
def add_due_date(task_id, due_date):
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1]["due_date"] = due_date
        save_tasks()
    else:
        colored_print(t("invalid_task_number"), Fore.RED)

# Removes the due date from a task by its ID.
# Entfernt das Fälligkeitsdatum einer Aufgabe anhand ihrer ID.
def remove_due_date(task_id):
    if 1 <= task_id <= len(tasks):
        tasks[task_id - 1]["due_date"] = None
        save_tasks()
    else:
        colored_print(t("invalid_task_number"), Fore.RED)

# Searches for tasks containing the given keyword.
# Sucht nach Aufgaben, die das angegebene Schlüsselwort enthalten.
def search_tasks(keyword):
    results = [task for task in tasks if keyword.lower() in task["description"].lower()]
    if not results:
        colored_print(t("task_not_found"), Fore.YELLOW)
        return
    for i, task in enumerate(results):
        status = "✓" if task["completed"] else " "
        priority = f"[{task['priority']}]" if task["priority"] else ""
        due_date = f"(Due: {task['due_date']})" if task["due_date"] else ""
        color = Fore.GREEN if task["completed"] else Fore.WHITE
        if not task["completed"] and task["priority"] == "high":
            color = Fore.RED
        elif not task["completed"] and task["priority"] == "medium":
            color = Fore.YELLOW
        colored_print(f"{i+1}. [{status}] {task['description']} {priority} {due_date}", color)

# Edits the description, priority, or due date of a task by its ID.
# Bearbeitet die Beschreibung, Priorität oder das Fälligkeitsdatum einer Aufgabe anhand ihrer ID.
def edit_task(task_id):
    if 1 <= task_id <= len(tasks):
        task = tasks[task_id - 1]
        new_description = input(t("enter_new_description"))
        if new_description:
            task["description"] = new_description
        new_priority = input(t("enter_priority"))
        if new_priority.lower() in ['high', 'medium', 'low']:
            task["priority"] = new_priority.lower()
        new_due_date = input(t("enter_due_date"))
        if new_due_date:
            task["due_date"] = new_due_date
        save_tasks()
    else:
        colored_print(t("invalid_task_number"), Fore.RED)

# Sorts tasks by priority, due date, or status.
# Sortiert Aufgaben nach Priorität, Fälligkeitsdatum oder Status.
def sort_tasks(option):
    if option == "priority":
        tasks.sort(key=lambda x: (x["priority"] is None, x["priority"]))
    elif option == "due_date":
        tasks.sort(key=lambda x: (x["due_date"] is None, x["due_date"]))
    elif option == "status":
        tasks.sort(key=lambda x: x["completed"])
    else:
        colored_print(t("invalid_choice"), Fore.RED)
    save_tasks()

# Filters tasks by status or priority.
# Filtert Aufgaben nach Status oder Priorität.
def filter_tasks(option):
    if option == "completed":
        filtered_tasks = [task for task in tasks if task["completed"]]
    elif option == "not_completed":
        filtered_tasks = [task for task in tasks if not task["completed"]]
    elif option in ["high", "medium", "low"]:
        filtered_tasks = [task for task in tasks if task["priority"] == option]
    else:
        colored_print(t("invalid_choice"), Fore.RED)
        return
    for i, task in enumerate(filtered_tasks):
        status = "✓" if task["completed"] else " "
        priority = f"[{task['priority']}]" if task["priority"] else ""
        due_date = f"(Due: {task['due_date']})" if task["due_date"] else ""
        color = Fore.GREEN if task["completed"] else Fore.WHITE
        if not task["completed"] and task["priority"] == "high":
            color = Fore.RED
        elif not task["completed"] and task["priority"] == "medium":
            color = Fore.YELLOW
        colored_print(f"{i+1}. [{status}] {task['description']} {priority} {due_date}", color)

# Saves the current tasks to a JSON file.
# Speichert die aktuellen Aufgaben in einer JSON-Datei.
def save_tasks():
    with open("pytodo.json", "w") as file:
        json.dump(tasks, file, indent=4)
    colored_print(t("tasks_saved"), Fore.GREEN)

# Loads tasks from a JSON file if it exists.
# Lädt Aufgaben aus einer JSON-Datei, falls diese existiert.
def load_tasks():
    if os.path.exists("pytodo.json"):
        with open("pytodo.json", "r") as file:
            global tasks
            tasks = json.load(file)
        colored_print(t("tasks_loaded"), Fore.GREEN)
    else:
        colored_print(t("no_saved_tasks"), Fore.YELLOW)

# Prints the menu options.
# Druckt die Menüoptionen.
def print_menu():
    colored_print(t("menu"), Fore.CYAN)
    colored_print(t("add_task"), Fore.CYAN)
    colored_print(t("list_tasks"), Fore.CYAN)
    colored_print(t("remove_task"), Fore.CYAN)
    colored_print(t("complete_task"), Fore.CYAN)
    colored_print(t("add_priority"), Fore.CYAN)
    colored_print(t("remove_priority"), Fore.CYAN)
    colored_print(t("add_due_date"), Fore.CYAN)
    colored_print(t("remove_due_date"), Fore.CYAN)
    colored_print(t("search_tasks"), Fore.CYAN)
    colored_print(t("edit_task"), Fore.CYAN)
    colored_print(t("sort_tasks"), Fore.CYAN)
    colored_print(t("filter_tasks"), Fore.CYAN)
    colored_print(t("exit"), Fore.CYAN)
    colored_print("=====================", Fore.CYAN)

# Main loop for the menu.
# Hauptschleife für das Menü.
def menu_loop():
    print_menu()
    while True:
        choice = input(t("enter_choice"))
        
        if choice.lower() == 'm':
            print_menu()
            continue
        elif choice == "0":
            colored_print(t("goodbye"), Fore.CYAN)
            break
        elif choice == "1":
            task = input(t("enter_task_description"))
            add_task(task)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            list_tasks()
            task_id = input(t("enter_task_number"))
            try:
                remove_task(int(task_id))
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "4":
            list_tasks()
            task_id = input(t("enter_task_number"))
            try:
                complete_task(int(task_id))
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "5":
            list_tasks()
            task_id = input(t("enter_task_number"))
            priority = input(t("enter_priority"))
            try:
                add_priority(int(task_id), priority)
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "6":
            list_tasks()
            task_id = input(t("enter_task_number"))
            try:
                remove_priority(int(task_id))
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "7":
            list_tasks()
            task_id = input(t("enter_task_number"))
            due_date = input(t("enter_due_date"))
            try:
                add_due_date(int(task_id), due_date)
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "8":
            list_tasks()
            task_id = input(t("enter_task_number"))
            try:
                remove_due_date(int(task_id))
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "9":  # New menu option for search
            keyword = input(t("enter_keyword"))
            search_tasks(keyword)
        elif choice == "10":  # New menu option for edit
            list_tasks()
            task_id = input(t("enter_task_number"))
            try:
                edit_task(int(task_id))
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "11":  # New menu option for sort
            option = input(t("enter_sort_option"))
            sort_tasks(option)
        elif choice == "12":  # New menu option for filter
            option = input(t("enter_filter_option"))
            filter_tasks(option)
        else:
            colored_print(t("invalid_choice"), Fore.RED)

# Main function to initialize and start the program.
# Hauptfunktion zum Initialisieren und Starten des Programms.
def main():
    global language
    init(autoreset=True)
    load_tasks()
    language = input("Choose language (en/de): ").strip().lower()
    if language not in translations:
        language = "en"
    try:
        menu_loop()
    except KeyboardInterrupt:
        colored_print(f"\n{t('goodbye')}", Fore.CYAN)

if __name__ == "__main__":
    main()