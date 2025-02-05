# PYTODO

## Description
PYTODO is a simple command-line based task management application. It allows users to add, list, remove, complete, prioritize, and set due dates for tasks. The application supports multilingual functionality (English and German) and provides color-coded output for better readability.

## Features
- Add new tasks
- List all tasks
- Remove tasks with confirmation
- Mark tasks as complete
- Add priority to tasks (high, medium, low)
- Remove priority from tasks
- Add due dates to tasks
- Remove due dates from tasks
- Search tasks by keyword
- Edit task description, priority, and due date
- Sort tasks by priority, due date, or status
- Filter tasks by status (completed/not completed) or priority (high/medium/low)
- Multilingual support (English and German)
- Color-coded output for better readability

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/LeanoJ/pytodo.git
    ```
2. Navigate to the project directory:
    ```sh
    cd pytodo
    ```
3. Install the required dependencies:
    ```sh
    pip install colorama
    ```

## Usage
1. Run the application:
    ```sh
    python pytodo.py
    ```
2. Choose your preferred language (English or German).
3. Follow the on-screen menu to manage your tasks.

## Menu Options
- `1. Add new task`: Add a new task with a description.
- `2. List all tasks`: List all tasks with their status, priority, and due date.
- `3. Remove task`: Remove a task by its number with confirmation.
- `4. Mark task as complete`: Mark a task as complete by its number.
- `5. Add priority to task`: Add a priority (high/medium/low) to a task by its number.
- `6. Remove priority from task`: Remove the priority from a task by its number.
- `7. Add due date to task`: Add a due date to a task by its number.
- `8. Remove due date from task`: Remove the due date from a task by its number.
- `9. Search tasks`: Search for tasks containing a specific keyword.
- `10. Edit task`: Edit the description, priority, or due date of a task by its number.
- `11. Sort tasks`: Sort tasks by priority, due date, or status.
- `12. Filter tasks`: Filter tasks by status (completed/not completed) or priority (high/medium/low).
- `0. Exit`: Exit the application.

## Example
```sh
=== TODO List Manager ===
1. Add new task
2. List all tasks
3. Remove task
4. Mark task as complete
5. Add priority to task
6. Remove priority from task
7. Add due date to task
8. Remove due date from task
9. Search tasks
10. Edit task
11. Sort tasks
12. Filter tasks
0. Exit
=====================
Enter your choice (0-12) or 'm' for menu: 1
Enter task description: Finish the project
Tasks saved successfully.
Enter your choice (0-12) or 'm' for menu: 2
1. [ ] Finish the project
Enter your choice (0-12) or 'm' for menu: 0
Goodbye!
```

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Author
- LeanoJ - [LeanoJ](https://github.com/LeanoJ)