#Presupuestador/src/models/db_manager.py
import os
import mysql.connector
from mysql.connector import Error, ProgrammingError, DatabaseError, IntegrityError
from dotenv import load_dotenv
from src.logs.config_logger import LoggerConfigurator
from src.models.table_manager import TableManager

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

        logger.debug("Intentando establecer una conexión inicial con la base de datos.")
        self.conn = self.attempt_connection()
        if self.conn is None:
            logger.error("No fue posible establecer una conexión inicial con la base de datos.")
            return None

        if self.conn.is_connected():
            db_info = self.conn.get_server_info()
            logger.info(f"Conectado al servidor MySQL versión {db_info}")
            self.initialize_database()
            self.check_tables()
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
            if pe.errno == 1049:  # Código de error para base de datos desconocida
                self.create_database()
                return self.attempt_connection()
            logger.error(f"Error de programación en SQL: {pe}")
        except DatabaseError as de:
            logger.error(f"Error de base de datos: {de}")
        except Error as e:
            logger.error(f"Error general de conexión a la base de datos: {e}")
        return None

    def create_database(self):
        """Crea la base de datos si no existe."""
        try:
            conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {self.db_name}")
            cursor.close()
            conn.close()
            logger.info(f"Base de datos '{self.db_name}' creada exitosamente.")
        except Error as e:
            logger.error(f"No se pudo crear la base de datos '{self.db_name}': {e}")

    def initialize_database(self):
        """Verifica y crea tablas si es necesario utilizando un nuevo cursor para evitar conflictos de resultados no consumidos."""
        logger.debug("Inicializando la base de datos.")
        with self.conn.cursor() as cursor:
            logger.debug("Ejecutando SHOW TABLES para verificar las tablas existentes.")
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()  # Asegúrate de consumir todos los resultados

            logger.debug(f"Tablas encontradas: {tables}")

            if not tables:  # Si no hay tablas, procede a crearlas
                logger.info("No se encontraron tablas en la base de datos. Creando tablas...")
                TableManager(self.conn).create_tables()

    def check_tables(self):
        """Check and create tables if they do not exist."""
        logger.debug("Verificando y creando tablas si es necesario.")
        table_manager = TableManager(self.conn)
        with self.conn.cursor() as cursor:
            if not table_manager.table_exists(cursor, 'presupuestos'):
                logger.info("The 'presupuestos' table was not found. Creating tables...")
                table_manager.create_tables()
                logger.info("Tables created successfully.")

    def insert_budget_into_db(self, cursor, conn, budget_data):
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
            logger.info("Presupuesto creado con éxito.")
        except mysql.connector.Error as error:
            logger.error(f"Error al crear presupuesto: {error}")
            conn.rollback()

    def table_exists(self, cursor, table_name):
        """Verifica si una tabla existe en la base de datos."""
        cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
        return cursor.fetchone() is not None

