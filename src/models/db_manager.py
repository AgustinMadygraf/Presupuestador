"""
This module provides a DatabaseManager class to handle database operations
such as creating databases and checking tables.
"""

import mysql.connector
from dotenv import load_dotenv
from src.logs.config_logger import LoggerConfigurator
from src.models.table_manager import TableManager

load_dotenv()

logger = LoggerConfigurator().configure()

class DatabaseManager:
    """
    A class to manage database operations.
    
    Attributes:
        conn: A MySQL connection object.
    """

    def __init__(self, conn):
        """
        Initializes the DatabaseManager with a database connection.

        Args:
            conn: A MySQL connection object.
        """
        self.conn = conn

    def create_database(self, db_name):
        """
        Creates a new database.

        Args:
            db_name: The name of the database to create.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_name}")
            logger.info("Base de datos '%s' creada exitosamente.", db_name)
        except mysql.connector.Error as err:
            if err.errno == 3678:  # Error code for schema directory already exists
                logger.error("No se pudo crear la base de datos '%s': %s", db_name, err)
                # Handle the error, e.g., by renaming or moving the existing schema directory
                # os.rename(f".\\{db_name}", f".\\{db_name}_backup")
            else:
                logger.error("Error al crear la base de datos '%s': %s", db_name, err)
            raise

    def check_tables(self):
        """
        Verifies and creates tables if necessary.
        """
        logger.debug("Verificando y creando tablas si es necesario.")
        table_manager = TableManager(self.conn)
        table_manager.check_and_create_tables()
