from datetime import datetime
from colorama import Fore, Style
from storage import get_db_connection

# Prints text in a specified color.
# Druckt Text in einer angegebenen Farbe.
def colored_print(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

# Adds a new task with the given description.
# Fügt eine neue Aufgabe mit der angegebenen Beschreibung hinzu.
def add_task(description, t):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO tasks (description, priority, due_date, status) 
                      VALUES (%s, %s, %s, %s)''', (description, None, None, 'not_completed'))
    conn.commit()
    cursor.close()
    conn.close()
    colored_print(t("tasks_saved"), Fore.GREEN)

# Lists all tasks with their status, priority, and due date.
# Listet alle Aufgaben mit ihrem Status, ihrer Priorität und ihrem Fälligkeitsdatum auf.
def list_tasks(t):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    cursor.close()
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
def remove_task(task_id, t):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=%s', (task_id,))
    task = cursor.fetchone()
    if task:
        confirm = input(t("confirm_delete")).strip().lower()
        if confirm in ['y', 'j']:
            cursor.execute('DELETE FROM tasks WHERE id=%s', (task_id,))
            conn.commit()
            colored_print(t("tasks_saved"), Fore.GREEN)
        else:
            colored_print(t("delete_cancelled"), Fore.YELLOW)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    cursor.close()
    conn.close()

# Marks a task as completed by its ID.
# Markiert eine Aufgabe anhand ihrer ID als erledigt.
def complete_task(task_id, t):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=%s', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET status=%s WHERE id=%s', ('completed', task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    cursor.close()
    conn.close()

# Adds a priority to a task by its ID.
# Fügt einer Aufgabe anhand ihrer ID eine Priorität hinzu.
def add_priority(task_id, priority, t):
    if priority.lower() not in ['high', 'medium', 'low']:
        colored_print(t("invalid_priority"), Fore.RED)
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=%s', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET priority=%s WHERE id=%s', (priority.lower(), task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    cursor.close()
    conn.close()

# Removes the priority from a task by its ID.
# Entfernt die Priorität einer Aufgabe anhand ihrer ID.
def remove_priority(task_id, t):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=%s', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET priority=%s WHERE id=%s', (None, task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    cursor.close()
    conn.close()

# Adds a due date to a task by its ID.
# Fügt einer Aufgabe anhand ihrer ID ein Fälligkeitsdatum hinzu.
def add_due_date(task_id, due_date, t):
    if not validate_due_date(due_date, t):
        return
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=%s', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET due_date=%s WHERE id=%s', (due_date, task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    cursor.close()
    conn.close()

# Removes the due date from a task by its ID.
# Entfernt das Fälligkeitsdatum einer Aufgabe anhand ihrer ID.
def remove_due_date(task_id, t):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=%s', (task_id,))
    task = cursor.fetchone()
    if task:
        cursor.execute('UPDATE tasks SET due_date=%s WHERE id=%s', (None, task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    cursor.close()
    conn.close()

# Searches for tasks containing the given keyword.
# Sucht nach Aufgaben, die das angegebene Schlüsselwort enthalten.
def search_tasks(keyword, t):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE description LIKE %s', ('%' + keyword + '%',))
    tasks = cursor.fetchall()
    cursor.close()
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
def edit_task(task_id, t):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=%s', (task_id,))
    task = cursor.fetchone()
    if task:
        new_description = input(t("enter_new_description"))
        if new_description:
            cursor.execute('UPDATE tasks SET description=%s WHERE id=%s', (new_description, task_id))
        new_priority = input(t("enter_priority"))
        if new_priority.lower() in ['high', 'medium', 'low']:
            cursor.execute('UPDATE tasks SET priority=%s WHERE id=%s', (new_priority.lower(), task_id))
        new_due_date = input(t("enter_due_date"))
        if new_due_date and validate_due_date(new_due_date, t):
            cursor.execute('UPDATE tasks SET due_date=%s WHERE id=%s', (new_due_date, task_id))
        conn.commit()
        colored_print(t("tasks_saved"), Fore.GREEN)
    else:
        colored_print(t("invalid_task_number"), Fore.RED)
    cursor.close()
    conn.close()

# Sorts tasks by priority, due date, or status.
# Sortiert Aufgaben nach Priorität, Fälligkeitsdatum oder Status.
def sort_tasks(option, t):
    conn = get_db_connection()
    cursor = conn.cursor()
    if option == "priority":
        cursor.execute('SELECT * FROM tasks ORDER BY priority IS NULL, priority')
    elif option == "due_date":
        cursor.execute('SELECT * FROM tasks ORDER BY due_date IS NULL, due_date')
    elif option == "status":
        cursor.execute('SELECT * FROM tasks ORDER BY status')
    else:
        colored_print(t("invalid_choice"), Fore.RED)
        cursor.close()
        conn.close()
        return
    tasks = cursor.fetchall()
    cursor.close()
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
def filter_tasks(option, t):
    conn = get_db_connection()
    cursor = conn.cursor()
    if option == "completed":
        cursor.execute('SELECT * FROM tasks WHERE status=%s', ('completed',))
    elif option == "not_completed":
        cursor.execute('SELECT * FROM tasks WHERE status=%s', ('not_completed',))
    elif option in ["high", "medium", "low"]:
        cursor.execute('SELECT * FROM tasks WHERE priority=%s', (option,))
    else:
        colored_print(t("invalid_choice"), Fore.RED)
        cursor.close()
        conn.close()
        return
    tasks = cursor.fetchall()
    cursor.close()
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
def validate_due_date(due_date, t):
    try:
        datetime.strptime(due_date, '%Y-%m-%d')
        return True
    except ValueError:
        colored_print(t("invalid_date"), Fore.RED)
        return False
