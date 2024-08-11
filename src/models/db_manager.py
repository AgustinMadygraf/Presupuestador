#Presupuestador/src/models/db_manager.py
import os
import mysql.connector
from mysql.connector import Error, ProgrammingError, DatabaseError, IntegrityError
from dotenv import load_dotenv
from src.logs.config_logger import LoggerConfigurator
from src.models.table_manager import TableManager
from src.utils import table_exists

load_dotenv()

logger = LoggerConfigurator().configure()

class DatabaseManager:
    def __init__(self, conn):
        self.conn = conn

    def create_database(self, db_name):
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"Base de datos '{db_name}' creada exitosamente.")
        except mysql.connector.Error as err:
            if err.errno == 3678:  # Error code for schema directory already exists
                logger.error(f"No se pudo crear la base de datos '{db_name}': {err}")
                # Handle the error, e.g., by renaming or moving the existing schema directory
                # os.rename(f".\\{db_name}", f".\\{db_name}_backup")
            else:
                logger.error(f"Error al crear la base de datos '{db_name}': {err}")
            raise

    def check_tables(self):
        """Verificar y crear tablas si es necesario."""
        logger.debug("Verificando y creando tablas si es necesario.")
        table_manager = TableManager(self.conn)
        with self.conn.cursor() as cursor:
            if not table_exists(cursor, 'presupuestos'):
                logger.info("La tabla 'presupuestos' no existe. Creando tablas...")
                table_manager.create_tables()
                logger.info("Tablas creadas exitosamente.")