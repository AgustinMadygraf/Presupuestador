#Presupuestador/src/database.py
import mysql.connector
from mysql.connector import Error, DatabaseError, ProgrammingError, IntegrityError
from logs.config_logger import logger
from dotenv import load_dotenv
import os
from colorama import Fore
from models.database import DatabaseManager

load_dotenv()



def create_and_connect_db(host, user, password, db_name):
    """Crea la base de datos si no existe y reconecta."""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if conn.is_connected():
            create_database(conn, db_name)
            conn.close()
            return mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=db_name
            )
    except Error as e:
        logger.error(f"No se pudo crear la base de datos '{db_name}': {e}")
        return None

def create_database(conn, db_name):
    """Create the database if it does not exist."""
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        logger.info(f"Base de datos '{db_name}' creada exitosamente.")
    finally:
        cursor.close()

def list_salespeople(cursor, conn):
    """Obtiene la lista de vendedores de la base de datos y agrega un nuevo vendedor si no hay ninguno."""
    if not table_exists(cursor, 'vendedores'):
        print("La tabla 'vendedores' no existe. Creándola ahora...")
        create_vendedores_table(cursor, conn)
    
    cursor.execute("SELECT ID_vendedor, Legajo_vendedor, nombre, apellido FROM vendedores;")
    vendedores = cursor.fetchall()
    
    if not vendedores:
        print("No hay vendedores disponibles.")
        response = input("¿Desea agregar un nuevo vendedor? (S/N): ")
        if response.strip().upper() == 'S':
            new_vendedor_id = agregar_vendedor(cursor, conn)
            if new_vendedor_id:
                cursor.execute("SELECT ID_vendedor, Legajo_vendedor, nombre, apellido FROM vendedores;")
                vendedores = cursor.fetchall()
            else:
                return []
        else:
            return [] 
    return vendedores

def create_vendedores_table(cursor, conn):
    """Crea la tabla 'vendedores' si no existe."""
    try:
        cursor.execute("""
        CREATE TABLE vendedores (
            ID_vendedor INT AUTO_INCREMENT PRIMARY KEY,
            Legajo_vendedor INT NOT NULL,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)
        conn.commit()
        print("Tabla 'vendedores' creada exitosamente.")
    except (Error, IntegrityError, ProgrammingError, DatabaseError) as e:
        conn.rollback()
        print(f"Error al crear la tabla 'vendedores': {e}")

def agregar_vendedor(cursor, conn):
    print("Ingrese los datos del nuevo vendedor:")
    legajo = input("Legajo: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")

    try:
        sql = """
        INSERT INTO vendedores (nombre, apellido, Legajo_vendedor)
        VALUES (%s, %s, %s);
        """
        cursor.execute(sql, (nombre, apellido, legajo))
        conn.commit()
        new_vendedor_id = cursor.lastrowid
        print(Fore.GREEN + f"Vendedor agregado con éxito. ID asignado: {new_vendedor_id}")
        return new_vendedor_id
    except mysql.connector.Error as error:
        print(Fore.RED + f"Error al añadir vendedor: {error}")
        conn.rollback()
        return None

def table_exists(cursor, table_name): # función duplicada en /src/models/database.py
    cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
    return cursor.fetchone() is not None

def get_next_budget_id(cursor):
    cursor.execute("SELECT MAX(ID_presupuesto) FROM presupuestos;")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id is not None else 1

def get_new_budget_id(cursor):
    new_id = get_next_budget_id(cursor)
    print(f"\nCreando un nuevo presupuesto con ID {new_id}\n")
    return new_id
