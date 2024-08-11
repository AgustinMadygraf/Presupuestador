# src/factories/database_connection_factory.py
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

class DatabaseConnectionFactory:
    @staticmethod
    def create_connection():
        try:
            conn = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            if conn.is_connected():
                return conn
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None