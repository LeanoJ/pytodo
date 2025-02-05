import json
import os
import sqlite3
from datetime import datetime
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
        "delete_cancelled": "Task deletion cancelled.",
        "invalid_date": "Invalid date. Please enter in YYYY-MM-DD format."
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
        "delete_cancelled": "Aufgabenlöschung abgebrochen.",
        "invalid_date": "Ungültiges Datum. Bitte im Format JJJJ-MM-TT eingeben."
    }
}

# Function to get translated text based on the selected language
# Funktion zum Abrufen des übersetzten Textes basierend auf der ausgewählten Sprache
def t(key):
    return translations[language].get(key, key)

# Initialize the database
# Initialisiert die Datenbank
def create_database():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                      (id INTEGER PRIMARY KEY, 
                       description TEXT, 
                       priority TEXT, 
                       due_date TEXT, 
                       status TEXT)''')
    conn.commit()
    conn.close()

# Adds a new task with the given description.
# Fügt eine neue Aufgabe mit der angegebenen Beschreibung hinzu.
def add_task(description):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO tasks (description, priority, due_date, status) 
                      VALUES (?, ?, ?, ?)''', (description, None, None, 'not_completed'))
    conn.commit()
    conn.close()
    colored_print(t("tasks_saved"), Fore.GREEN)

# Prints text in a specified color.
# Druckt Text in einer angegebenen Farbe.
def colored_print(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

# Lists all tasks with their status, priority, and due date.
# Listet alle Aufgaben mit ihrem Status, ihrer Priorität und ihrem Fälligkeitsdatum auf.
def list_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    conn.close()
    if not tasks:
        colored_print(t("no_tasks"), Fore.YELLOW)
        return
    for task in tasks:
        status = "✓" if task[4] == 'completed' else " "
        priority = f"[{task[2]}]" if task[2] else ""
        due_date = f"(Due: {task[3]})" if task[3] else ""
        color = Fore.GREEN if task[4] == 'completed' else Fore.WHITE
        if task[4] != 'completed' and task[2] == "high":
            color = Fore.RED
        elif task[4] != 'completed' and task[2] == "medium":
            color = Fore.YELLOW
        colored_print(f"{task[0]}. [{status}] {task[1]} {priority} {due_date}", color)

# Removes a task by its ID with confirmation.
# Entfernt eine Aufgabe anhand ihrer ID mit Bestätigung.
def remove_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    task = cursor.fetchone()
    if task:
        confirm = input(t("confirm_delete")).strip().lower()
        if confirm == 'y':
            cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
            conn.commit()
            colored_print(t("tasks_saved"), Fore.GREEN)
        else:
            colored_print(t("delete_cancelled"), Fore.YELLOW)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    conn.close()

# Marks a task as completed by its ID.
# Markiert eine Aufgabe anhand ihrer ID als erledigt.
def complete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET status=? WHERE id=?', ('completed', task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    conn.close()

# Adds a priority to a task by its ID.
# Fügt einer Aufgabe anhand ihrer ID eine Priorität hinzu.
def add_priority(task_id, priority):
    if priority.lower() not in ['high', 'medium', 'low']:
        colored_print(t("invalid_priority"), Fore.RED)
        return
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET priority=? WHERE id=?', (priority.lower(), task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    conn.close()

# Removes the priority from a task by its ID.
# Entfernt die Priorität einer Aufgabe anhand ihrer ID.
def remove_priority(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET priority=? WHERE id=?', (None, task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    conn.close()

# Adds a due date to a task by its ID.
# Fügt einer Aufgabe anhand ihrer ID ein Fälligkeitsdatum hinzu.
def add_due_date(task_id, due_date):
    if not validate_due_date(due_date):
        return
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET due_date=? WHERE id=?', (due_date, task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    conn.close()

# Removes the due date from a task by its ID.
# Entfernt das Fälligkeitsdatum einer Aufgabe anhand ihrer ID.
def remove_due_date(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET due_date=? WHERE id=?', (None, task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    conn.close()

# Searches for tasks containing the given keyword.
# Sucht nach Aufgaben, die das angegebene Schlüsselwort enthalten.
def search_tasks(keyword):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE description LIKE ?', ('%' + keyword + '%',))
    tasks = cursor.fetchall()
    conn.close()
    if not tasks:
        colored_print(t("task_not_found"), Fore.YELLOW)
        return
    for task in tasks:
        status = "✓" if task[4] == 'completed' else " "
        priority = f"[{task[2]}]" if task[2] else ""
        due_date = f"(Due: {task[3]})" if task[3] else ""
        color = Fore.GREEN if task[4] == 'completed' else Fore.WHITE
        if task[4] != 'completed' and task[2] == "high":
            color = Fore.RED
        elif task[4] != 'completed' and task[2] == "medium":
            color = Fore.YELLOW
        colored_print(f"{task[0]}. [{status}] {task[1]} {priority} {due_date}", color)

# Edits the description, priority, or due date of a task by its ID.
# Bearbeitet die Beschreibung, Priorität oder das Fälligkeitsdatum einer Aufgabe anhand ihrer ID.
def edit_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    task = cursor.fetchone()
    if task:
        new_description = input(t("enter_new_description"))
        if new_description:
            cursor.execute('UPDATE tasks SET description=? WHERE id=?', (new_description, task_id))
        new_priority = input(t("enter_priority"))
        if new_priority.lower() in ['high', 'medium', 'low']:
            cursor.execute('UPDATE tasks SET priority=? WHERE id=?', (new_priority.lower(), task_id))
        new_due_date = input(t("enter_due_date"))
        if new_due_date and validate_due_date(new_due_date):
            cursor.execute('UPDATE tasks SET due_date=? WHERE id=?', (new_due_date, task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    conn.close()

# Sorts tasks by priority, due date, or status.
# Sortiert Aufgaben nach Priorität, Fälligkeitsdatum oder Status.
def sort_tasks(option):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    if option == "priority":
        cursor.execute('SELECT * FROM tasks ORDER BY priority IS NULL, priority')
    elif option == "due_date":
        cursor.execute('SELECT * FROM tasks ORDER BY due_date IS NULL, due_date')
    elif option == "status":
        cursor.execute('SELECT * FROM tasks ORDER BY status')
    else:
        colored_print(t("invalid_choice"), Fore.RED)
        conn.close()
        return
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        status = "✓" if task[4] == 'completed' else " "
        priority = f"[{task[2]}]" if task[2] else ""
        due_date = f"(Due: {task[3]})" if task[3] else ""
        color = Fore.GREEN if task[4] == 'completed' else Fore.WHITE
        if task[4] != 'completed' and task[2] == "high":
            color = Fore.RED
        elif task[4] != 'completed' and task[2] == "medium":
            color = Fore.YELLOW
        colored_print(f"{task[0]}. [{status}] {task[1]} {priority} {due_date}", color)

# Filters tasks by status or priority.
# Filtert Aufgaben nach Status oder Priorität.
def filter_tasks(option):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    if option == "completed":
        cursor.execute('SELECT * FROM tasks WHERE status=?', ('completed',))
    elif option == "not_completed":
        cursor.execute('SELECT * FROM tasks WHERE status=?', ('not_completed',))
    elif option in ["high", "medium", "low"]:
        cursor.execute('SELECT * FROM tasks WHERE priority=?', (option,))
    else:
        colored_print(t("invalid_choice"), Fore.RED)
        conn.close()
        return
    tasks = cursor.fetchall()
    conn.close()
    for task in tasks:
        status = "✓" if task[4] == 'completed' else " "
        priority = f"[{task[2]}]" if task[2] else ""
        due_date = f"(Due: {task[3]})" if task[3] else ""
        color = Fore.GREEN if task[4] == 'completed' else Fore.WHITE
        if task[4] != 'completed' and task[2] == "high":
            color = Fore.RED
        elif task[4] != 'completed' and task[2] == "medium":
            color = Fore.YELLOW
        colored_print(f"{task[0]}. [{status}] {task[1]} {priority} {due_date}", color)

# Validates the due date format.
# Validiert das Fälligkeitsdatum-Format.
def validate_due_date(due_date):
    try:
        datetime.strptime(due_date, '%Y-%m-%d')
        return True
    except ValueError:
        colored_print(t("invalid_date"), Fore.RED)
        return False

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
    create_database()
    language = input("Choose language (en/de): ").strip().lower()
    if language not in translations:
        language = "en"
    try:
        menu_loop()
    except KeyboardInterrupt:
        colored_print(f"\n{t('goodbye')}", Fore.CYAN)

if __name__ == "__main__":
    main()