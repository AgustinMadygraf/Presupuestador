#src/database.py
import mysql.connector
from mysql.connector import Error

def create_connection(db_file=None):
    """Create a database connection to a MySQL database"""
    conn = None
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='presupuesto',
            user='root',
            password='12345678'
        )
        if conn.is_connected():
            db_info = conn.get_server_info()
            print("Conectado al servidor MySQL versión", db_info)
    except Error as e:
        print(e)
    return 
