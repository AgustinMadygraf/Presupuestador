#Presupuestador/src/models/table_manager.py
from mysql.connector import Error, ProgrammingError, DatabaseError, IntegrityError
from dotenv import load_dotenv
from src.logs.config_logger import LoggerConfigurator

load_dotenv()

logger = LoggerConfigurator().configure()

class TableManager:
    def __init__(self, conn):
        self.conn = conn

    def create_tables(self):
        """Create tables in the specified database."""
        try:
            with self.conn.cursor() as cursor:
                logger.debug("Creando tablas en la base de datos")
                table_definitions = {
                    'presupuestos': """
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
                    """,
                    'vendedores': """
                        CREATE TABLE IF NOT EXISTS vendedores (
                            ID_vendedor INT AUTO_INCREMENT PRIMARY KEY,
                            Legajo_vendedor INT NOT NULL,
                            nombre VARCHAR(255) NOT NULL,
                            apellido VARCHAR(255) NOT NULL
                        );
                    """,
                    'clientes': """
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
                    """,
                    'items': """
                        CREATE TABLE IF NOT EXISTS items (
                            ID_items INT AUTO_INCREMENT PRIMARY KEY,
                            ID_presupuesto INT,
                            Cantidad INT,
                            precio_por_unidad FLOAT,
                            importe FLOAT GENERATED ALWAYS AS (Cantidad * precio_por_unidad) STORED,
                            FOREIGN KEY (ID_presupuesto) REFERENCES presupuestos(ID_presupuesto)
                        );
                    """
                }
                
                for table_name, table_sql in table_definitions.items():
                    cursor.execute(table_sql)
                    logger.info(f"Tabla '{table_name}' creada exitosamente.")
        except (IntegrityError, ProgrammingError, DatabaseError, Error) as e:
            self.conn.rollback()
            logger.error(f"Error al crear las tablas: {e}")
