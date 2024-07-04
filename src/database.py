#Presupuestador/src/database.py
import mysql.connector
from mysql.connector import Error, DatabaseError, ProgrammingError, IntegrityError
from logs.config_logger import logger
from dotenv import load_dotenv
import os
from colorama import Fore

load_dotenv()

def create_connection():
    """Create a database connection to the MySQL database."""
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    db_name = os.getenv('MYSQL_DB')

    if None in (db_name, host, user, password):
        logger.error("Falta una o más variables de entorno requeridas para la conexión a la base de datos.")
        return None
    conn = attempt_connection(host, user, password, db_name)
    if conn is None:
        logger.error("No fue posible establecer una conexión inicial con la base de datos.")
        return None
    if conn.is_connected():
        db_info = conn.get_server_info()
        logger.info(f"Conectado al servidor MySQL versión {db_info}")
        initialize_database(conn)
    return conn

def attempt_connection(host, user, password, db_name):
    """Intenta conectar a la base de datos y maneja la ausencia de la misma."""
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        return conn
    except ProgrammingError as pe:
        logger.error(f"Error de programación en SQL: {pe}")
        return None
    except DatabaseError as de:
        logger.error(f"Error de base de datos: {de}")
        return None
    except Error as e:
        logger.error(f"Error general de conexión a la base de datos: {e}")
        return None

def initialize_database(conn):
    """Verifica y crea tablas si es necesario utilizando un nuevo cursor para evitar conflictos de resultados no consumidos."""
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()  # Asegúrate de consumir todos los resultados

        if not tables:  # Si no hay tablas, procede a crearlas
            logger.info("No se encontraron tablas en la base de datos. Creando tablas...")
            create_tables(conn)

def create_tables(conn):
    """Create tables in the specified database."""
    cursor = conn.cursor()
    try:
        logger.debug("Creando tablas en la base de datos")
        # Creación de la tabla 'presupuestos'
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS presupuestos (
            ID_presupuesto INT AUTO_INCREMENT PRIMARY KEY,
            Legajo_vendedor INT NOT NULL,
            ID_cliente INT NOT NULL,
            Entrega_incluido VARCHAR(255),
            Fecha_presupuesto VARCHAR(255),
            comentario TEXT,
            Condiciones TEXT,
            subtotal FLOAT,
            IVA_21 FLOAT GENERATED ALWAYS AS (subtotal * 0.21) STORED,
            total FLOAT GENERATED ALWAYS AS (subtotal * 1.21) STORED,
            tiempo_dias_valido INT,
            fecha_caducidad DATETIME GENERATED ALWAYS AS (DATE_ADD(fecha_presupuesto, INTERVAL tiempo_dias_valido DAY)) STORED
        );
        """)
        logger.info("Tabla 'presupuestos' creada exitosamente.")

        # Creación de la tabla 'vendedores'
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendedores (
            ID_vendedor INT AUTO_INCREMENT PRIMARY KEY,
            Legajo_vendedor INT NOT NULL,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL
        );
        """)
        logger.info("Tabla 'vendedores' creada exitosamente.")

        # Creación de la tabla 'clientes'
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            ID_cliente INT AUTO_INCREMENT PRIMARY KEY,
            CUIT VARCHAR(255),
            Razon_social VARCHAR(255),
            Direccion VARCHAR(255),
            Ubicacion_geografica VARCHAR(255),
            N_contacto VARCHAR(255),
            nombre VARCHAR(255),
            apellido VARCHAR(255),
            Unidad_de_negocio VARCHAR(255),
            Legajo_vendedor INT,
            Facturacion_anual FLOAT
        );
        """)
        logger.info("Tabla 'clientes' creada exitosamente.")

        # Creación de la tabla 'items'
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            ID_items INT AUTO_INCREMENT PRIMARY KEY,
            ID_presupuesto INT,
            Cantidad INT,
            precio_por_unidad FLOAT,
            importe FLOAT GENERATED ALWAYS AS (Cantidad * precio_por_unidad) STORED,
            FOREIGN KEY (ID_presupuesto) REFERENCES presupuestos(ID_presupuesto)
        );
        """)
        logger.info("Tabla 'items' creada exitosamente.")
    except IntegrityError as ie:
        conn.rollback()
        logger.error(f"Error de integridad: {ie}")
    except ProgrammingError as pe:
        conn.rollback()
        logger.error(f"Error de sintaxis SQL: {pe}")
    except DatabaseError as de:
        conn.rollback()
        logger.error(f"Error al interactuar con la base de datos: {de}")
    except Error as e:
        conn.rollback()
        logger.error(f"Error de MySQL no especificado: {e}")
    finally:
        cursor.close()




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

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
    return cursor.fetchone() is not None

def get_next_budget_id(cursor):
    cursor.execute("SELECT MAX(ID_presupuesto) FROM presupuestos;")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id is not None else 1

def insert_budget_into_db(cursor, conn, budget_data):
    if budget_data is None:
        return
    try:
        sql = """
        INSERT INTO presupuestos (ID_presupuesto, Legajo_vendedor, ID_cliente, Entrega_incluido, Fecha_presupuesto, comentario, Condiciones, subtotal, tiempo_dias_valido)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (
            budget_data["new_id"], budget_data["Legajo_vendedor"], budget_data["client_id"], 
            budget_data["Entrega_incluido"], budget_data["Fecha_presupuesto"], budget_data["comentario"], 
            budget_data["Condiciones"], budget_data["subtotal"], budget_data["tiempo_dias_valido"]
        ))
        conn.commit()
        print(Fore.GREEN + "Presupuesto creado con éxito.")
    except mysql.connector.Error as error:
        print(Fore.RED + f"Error al crear presupuesto: {error}")
        conn.rollback()

def get_new_budget_id(cursor):
    new_id = get_next_budget_id(cursor)
    print(f"\nCreando un nuevo presupuesto con ID {new_id}\n")
    return new_id

def check_and_create_tables(cursor, conn):
    if not table_exists(cursor, 'presupuestos'):
        logger.info("The 'presupuestos' table was not found. Creating tables...")
        create_tables(conn)
        logger.info("Tables created successfully.")
