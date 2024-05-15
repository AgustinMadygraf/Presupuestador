#src/database.py
import mysql.connector
from mysql.connector import Error
from logs.config_logger import configurar_logging
from dotenv import load_dotenv
import os

logger = configurar_logging()

load_dotenv()

def create_connection():
    """Create a database connection to the MySQL database."""
    host = os.getenv('MYSQL_HOST')
    user = os.getenv('MYSQL_USER')
    password = os.getenv('MYSQL_PASSWORD')
    db_name = os.getenv('MYSQL_DB')
    
    # Asegúrate de que todas las variables de entorno estén configuradas
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
    except Error as e:
        if 'Unknown database' in str(e):
            logger.info("La base de datos especificada no existe. Intentando crearla...")
            return create_and_connect_db(host, user, password, db_name)
        else:
            logger.error(f"Error al conectar a la base de datos: {e}")
            return None

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

def initialize_database(conn):
    """Verifica y crea tablas si es necesario utilizando un nuevo cursor para evitar conflictos de resultados no consumidos."""
    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()  # Asegúrate de consumir todos los resultados

        if not tables:  # Si no hay tablas, procede a crearlas
            logger.info("No se encontraron tablas en la base de datos. Creando tablas...")
            create_tables(conn)

def create_database(conn, db_name):
    """Create the database if it does not exist and create tables within a transaction."""
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        conn.database = db_name  # Esto es necesario para apuntar a la base de datos recién creada
        logger.info(f"Base de datos '{db_name}' creada exitosamente.")
        
        # Iniciar transacción para crear tablas
        conn.start_transaction()
        create_tables(conn)
        conn.commit()  # Confirmar cambios solo si todas las tablas se crean sin errores
        logger.info("Todas las tablas fueron creadas exitosamente en la transacción.")
        
    except Error as e:
        conn.rollback()  # Revertir cambios en caso de error
        logger.error(f"Error al crear la base de datos o las tablas: {e}", exc_info=True)
    finally:
        cursor.close()


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

        # Creación de la tabla 'vendedores'
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendedores (
            Legajo_vendedor INT AUTO_INCREMENT PRIMARY KEY,
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

    except Error as e:
        logger.error(f"Error al crear las tablas: {e}", exc_info=True)
    finally:
        cursor.close()

def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
    return cursor.fetchone() is not None

def get_next_budget_id(cursor):
    cursor.execute("SELECT MAX(ID_presupuesto) FROM presupuestos;")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id is not None else 1




