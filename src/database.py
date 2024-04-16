#src/database.py
import mysql.connector
from mysql.connector import Error
from logs.config_logger import configurar_logging
from dotenv import load_dotenv
import os

logger = configurar_logging()

load_dotenv()


def create_tables(conn):
    """Create tables in the specified database."""
    cursor = conn.cursor()
    try:
        # Creación de la tabla 'presupuestos'
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS presupuestos (
            ID_presupuesto INT AUTO_INCREMENT PRIMARY KEY,
            Legajo_vendedor INT NOT NULL,
            ID_cliente INT NOT NULL,
            Entrega_incluido VARCHAR(255),
            Fecha_envio VARCHAR(255),
            comentario TEXT,
            Condiciones TEXT,
            subtotal FLOAT,
            IVA_21 FLOAT GENERATED ALWAYS AS (subtotal * 0.21) STORED,
            total FLOAT GENERATED ALWAYS AS (subtotal * 1.21) STORED,
            fecha_presupuesto DATETIME DEFAULT CURRENT_TIMESTAMP,
            tiempo_dias_valido INT,
            fecha_caducidad DATETIME GENERATED ALWAYS AS (DATE_ADD(fecha_presupuesto, INTERVAL tiempo_dias_valido DAY)) STORED
        );
        """)
        logger.info("Tabla 'presupuestos' creada exitosamente.")

        # Añade aquí la creación de otras tablas: 'vendedores', 'clientes', 'items'
        # Ejemplo de creación de otra tabla
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendedores (
            Legajo_vendedor INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL
        );
        """)
        logger.info("Tabla 'vendedores' creada exitosamente.")
        # Repite para 'clientes' y 'items'

    except Error as e:
        logger.error(f"Error al crear las tablas: {e}", exc_info=True)
    finally:
        cursor.close()

def create_database(conn, db_name):
    """Create the database if it does not exist and create tables."""
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        conn.database = db_name  # Esto es necesario para apuntar a la base de datos recién creada
        logger.info(f"Base de datos '{db_name}' creada exitosamente.")
        create_tables(conn)  # Llamada a la función para crear tablas
    except Error as e:
        logger.error(f"Error al crear la base de datos: {e}", exc_info=True)
    finally:
        cursor.close()

def create_connection():
    """Create a database connection to the MySQL database"""
    conn = None
    
    db_name = os.getenv('MYSQL_DB')
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    
    # Asegúrate de que todas las variables de entorno estén configuradas
    if None in (db_name, host, user, password):
        logger.error("Falta una o más variables de entorno requeridas para la conexión a la base de datos.")
        return None

    try:
        # Intenta conectarse a la base de datos especificada
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        if conn.is_connected():
            db_info = conn.get_server_info()
            logger.info(f"Conectado al servidor MySQL versión {db_info}")
    except Error as e:
        if 'Unknown database' in str(e):
            # Si la base de datos no existe, crea una conexión sin especificar la base de datos
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            if conn.is_connected():
                logger.info("Conexión inicial sin base de datos establecida exitosamente.")
                # Crea la base de datos
                create_database(conn, db_name)
                # Cierra la conexión inicial y reconéctate a la nueva base de datos
                conn.close()
                conn = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db_name
                )
                logger.info(f"Reconectado a la nueva base de datos '{db_name}'.")
        else:
            logger.error(f"Error al conectar a la base de datos: {e}", exc_info=True)
    return conn


