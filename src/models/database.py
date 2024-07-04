import os
import mysql.connector
from mysql.connector import Error, ProgrammingError, DatabaseError, IntegrityError
from dotenv import load_dotenv
from src.logs.config_logger import LoggerConfigurator

load_dotenv()

logger = LoggerConfigurator().get_logger()

class DatabaseManager:
    def __init__(self):
        self.host = os.getenv('MYSQL_HOST')
        self.user = os.getenv('MYSQL_USER')
        self.password = os.getenv('MYSQL_PASSWORD')
        self.db_name = os.getenv('MYSQL_DB')
        self.conn = None

    def create_connection(self):
        """Create a database connection to the MySQL database."""
        if None in (self.db_name, self.host, self.user, self.password):
            logger.error("Falta una o más variables de entorno requeridas para la conexión a la base de datos.")
            return None

        self.conn = self.attempt_connection()
        if self.conn is None:
            logger.error("No fue posible establecer una conexión inicial con la base de datos.")
            return None

        if self.conn.is_connected():
            db_info = self.conn.get_server_info()
            logger.info(f"Conectado al servidor MySQL versión {db_info}")
            self.initialize_database()
            self.check_and_create_tables()
        return self.conn

    def attempt_connection(self):
        """Intenta conectar a la base de datos y maneja la ausencia de la misma."""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.db_name
            )
            return conn
        except ProgrammingError as pe:
            logger.error(f"Error de programación en SQL: {pe}")
        except DatabaseError as de:
            logger.error(f"Error de base de datos: {de}")
        except Error as e:
            logger.error(f"Error general de conexión a la base de datos: {e}")
        return None

    def initialize_database(self):
        """Verifica y crea tablas si es necesario utilizando un nuevo cursor para evitar conflictos de resultados no consumidos."""
        with self.conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()  # Asegúrate de consumir todos los resultados

            if not tables:  # Si no hay tablas, procede a crearlas
                logger.info("No se encontraron tablas en la base de datos. Creando tablas...")
                self.create_tables()

    def create_tables(self):
        """Create tables in the specified database."""
        cursor = self.conn.cursor()
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
            self.conn.rollback()
            logger.error(f"Error de integridad: {ie}")
        except ProgrammingError as pe:
            self.conn.rollback()
            logger.error(f"Error de sintaxis SQL: {pe}")
        except DatabaseError as de:
            self.conn.rollback()
            logger.error(f"Error al interactuar con la base de datos: {de}")
        except Error as e:
            self.conn.rollback()
            logger.error(f"Error de MySQL no especificado: {e}")
        finally:
            cursor.close()

    def table_exists(self, cursor, table_name):
        """Check if a table exists in the database."""
        cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
        return cursor.fetchone() is not None

    def check_and_create_tables(self):
        """Check and create tables if they do not exist."""
        logger.debug("Verificando y creando tablas si es necesario.")
        cursor = self.conn.cursor()
        if not self.table_exists(cursor, 'presupuestos'):
            logger.info("The 'presupuestos' table was not found. Creating tables...")
            self.create_tables()
            logger.info("Tables created successfully.")
        cursor.close()
