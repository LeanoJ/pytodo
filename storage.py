import sqlite3

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
