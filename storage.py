import mysql.connector
import os

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'mysql-service'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'my-secret-pw'),
        database=os.getenv('MYSQL_DATABASE', 'pytododb')
    )

def create_database():
    try:
        # First connect without database
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'mysql-service'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', 'my-secret-pw')
        )
        cursor = conn.cursor()
        
        # Create database if not exists
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('MYSQL_DATABASE', 'pytododb')}")
        cursor.execute(f"USE {os.getenv('MYSQL_DATABASE', 'pytododb')}")
        
        # Create tasks table
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                          (id INT AUTO_INCREMENT PRIMARY KEY, 
                           description TEXT, 
                           priority VARCHAR(10), 
                           due_date DATE, 
                           status VARCHAR(20))''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Database and table created successfully")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        raise
