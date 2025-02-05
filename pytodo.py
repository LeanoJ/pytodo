import json
import os
from colorama import init, Fore, Style
from storage import create_database
from menu import menu_loop

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