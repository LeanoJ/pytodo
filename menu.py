from colorama import Fore
from tasks import add_task, list_tasks, remove_task, complete_task, add_priority, remove_priority, add_due_date, remove_due_date, search_tasks, edit_task, sort_tasks, filter_tasks

# Prints the menu options.
# Druckt die Menüoptionen.
def print_menu(t, colored_print):
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
def menu_loop(t, colored_print):
    print_menu(t, colored_print)
    while True:
        choice = input(t("enter_choice"))
        
        if choice.lower() == 'm':
            print_menu(t, colored_print)
            continue
        elif choice == "0":
            colored_print(t("goodbye"), Fore.CYAN)
            break
        elif choice == "1":
            task = input(t("enter_task_description"))
            add_task(task, t)
        elif choice == "2":
            list_tasks(t)
        elif choice == "3":
            list_tasks(t)
            task_id = input(t("enter_task_number"))
            try:
                remove_task(int(task_id), t)
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "4":
            list_tasks(t)
            task_id = input(t("enter_task_number"))
            try:
                complete_task(int(task_id), t)
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "5":
            list_tasks(t)
            task_id = input(t("enter_task_number"))
            priority = input(t("enter_priority"))
            try:
                add_priority(int(task_id), priority, t)
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "6":
            list_tasks(t)
            task_id = input(t("enter_task_number"))
            try:
                remove_priority(int(task_id), t)
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "7":
            list_tasks(t)
            task_id = input(t("enter_task_number"))
            due_date = input(t("enter_due_date"))
            try:
                add_due_date(int(task_id), due_date, t)
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "8":
            list_tasks(t)
            task_id = input(t("enter_task_number"))
            try:
                remove_due_date(int(task_id), t)
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "9":  # New menu option for search
            keyword = input(t("enter_keyword"))
            search_tasks(keyword, t)
        elif choice == "10":  # New menu option for edit
            list_tasks(t)
            task_id = input(t("enter_task_number"))
            try:
                edit_task(int(task_id), t)
            except ValueError:
                colored_print(t("invalid_task_number"), Fore.RED)
        elif choice == "11":  # New menu option for sort
            option = input(t("enter_sort_option"))
            sort_tasks(option, t)
        elif choice == "12":  # New menu option for filter
            option = input(t("enter_filter_option"))
            filter_tasks(option, t)
        else:
            colored_print(t("invalid_choice"), Fore.RED)
