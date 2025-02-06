# PYTODO

## Description
PYTODO is a command-line based task management application with MySQL database backend. It runs in Kubernetes, allowing for scalable and persistent task management. The application supports multilingual functionality (English and German) and provides color-coded output for better readability.

## Features
- Add, list, remove, and complete tasks
- Priority management (high, medium, low)
- Due date management
- Search, edit, sort, and filter tasks
- Multilingual support (English and German)
- Color-coded output
- MySQL database backend
- Kubernetes deployment support
- Docker containerization

## Prerequisites
- Docker
- Kubernetes cluster (e.g., Minikube)
- kubectl CLI tool

## Installation

### Local Development
1. Clone the repository:
```sh
git clone https://github.com/LeanoJ/pytodo.git
cd pytodo
```

2. Install dependencies:
```sh
pip install -r requirements.txt
```

### Kubernetes Deployment
1. Start your Kubernetes cluster (e.g., Minikube)

2. Create necessary resources:
```sh
# Create MySQL secret
kubectl apply -f ./minikube/mysql-secret.yaml

# Create MySQL PVC
kubectl apply -f ./minikube/mysql-pvc.yaml

# Deploy MySQL
kubectl apply -f ./minikube/mysql-service.yaml
kubectl apply -f ./minikube/mysql-deployment.yaml

# Deploy PYTODO
kubectl apply -f ./minikube/pytodo-deployment.yaml
```

3. Build and deploy the application:
```sh
# Build Docker image
eval $(minikube docker-env)  # Only for Minikube
docker build -t pytodo:latest .
```

## Usage

### Kubernetes Environment
1. Connect to the PYTODO pod:
```sh
kubectl exec -it <pytodo-pod-name> -- bash
```

2. Run the application:
```sh
python pytodo.py
```

## Configuration
The application uses the following environment variables:
- `MYSQL_HOST`: MySQL server hostname (default: mysql-service)
- `MYSQL_USER`: MySQL username (default: root)
- `MYSQL_PASSWORD`: MySQL password (from Kubernetes secret)
- `MYSQL_DATABASE`: MySQL database name (default: pytododb)
- `LANGUAGE`: Interface language (en/de, default: en)

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

## Architecture
- Frontend: Python CLI application
- Database: MySQL 8.0
- Container: Docker
- Orchestration: Kubernetes
- Persistence: Kubernetes PersistentVolumeClaim

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Author
- LeanoJ - [LeanoJ](https://github.com/LeanoJ)