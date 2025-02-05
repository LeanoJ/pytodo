import argparse
import json
import os

tasks = []

def load_tasks():
    if os.path.exists("tasks.json"):
        with open("tasks.json", "r") as file:
            return json.load(file)
    return []

def save_tasks():
    with open("tasks.json", "w") as file:
        json.dump(tasks, file)

tasks = load_tasks()

def add_task(task):
    tasks.append(task)
    print(f"Added task: {task}")


def remove_task(task_id):
    if task_id < 1 or task_id > len(tasks):
        print("Invalid task number.")
    else:
        task = tasks.pop(task_id - 1)
        print(f"Removed task: {task}")

def complete_task(task_id):
    if task_id < 1 or task_id > len(tasks):
        print("Invalid task number.")
    else:
        task = tasks[task_id - 1]
        print(f"Completed task: {task}")
        tasks.pop(task_id - 1)

def list_tasks():
    if not tasks:
        print("No tasks available.")
    else:
        for idx, task in enumerate(tasks, 1):
            print(f"{idx}. {task}")

def main():
    parser = argparse.ArgumentParser(description="Simple TODO list application")
    parser.add_argument("command", choices=["add", "list", "remove"], help="Command to execute")
    parser.add_argument("task", nargs="?", help="Task to add")

    args = parser.parse_args()

    if args.command == "add":
        if args.task:
            add_task(args.task)
        else:
            print("Please provide a task to add.")
    elif args.command == "list":
        list_tasks()
    elif args.command == "remove":
        if args.task:
            remove_task(int(args.task))
        else:
            print("Please provide a task number to remove.")
    elif args.command == "complete":
        if args.task:
            complete_task(int(args.task))
        else:
            print("Please provide a task number to complete.")
    else:
        print("Invalid command.")
        
if __name__ == "__main__":
    main()