#Presupuestador/src/models/salesperson_manager.py
import mysql.connector
from colorama import Fore

class SalespersonManager:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def list_salespeople(self):
        """Obtiene la lista de vendedores de la base de datos y agrega un nuevo vendedor si no hay ninguno."""
        if not self.table_exists('vendedores'):
            print("La tabla 'vendedores' no existe. Creándola ahora...")
            self.create_vendedores_table()

        self.cursor.execute("SELECT ID_vendedor, Legajo_vendedor, nombre, apellido FROM vendedores;")
        vendedores = self.cursor.fetchall()

        if not vendedores:
            print("No hay vendedores disponibles.")
            response = input("¿Desea agregar un nuevo vendedor? (S/N): ")
            if response.strip().upper() == 'S':
                new_vendedor_id = self.add_salesperson()
                if new_vendedor_id:
                    self.cursor.execute("SELECT ID_vendedor, Legajo_vendedor, nombre, apellido FROM vendedores;")
                    vendedores = self.cursor.fetchall()
                else:
                    return []
            else:
                return []
        return vendedores

    def create_vendedores_table(self):
        """Crea la tabla 'vendedores' si no existe."""
        try:
            self.cursor.execute("""
            CREATE TABLE vendedores (
                ID_vendedor INT AUTO_INCREMENT PRIMARY KEY,
                Legajo_vendedor INT NOT NULL,
                nombre VARCHAR(255) NOT NULL,
                apellido VARCHAR(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """)
            self.conn.commit()
            print("Tabla 'vendedores' creada exitosamente.")
        except mysql.connector.Error as e:
            self.conn.rollback()
            print(f"Error al crear la tabla 'vendedores': {e}")

    def add_salesperson(self):
        """Añade un nuevo vendedor a la base de datos."""
        print("Ingrese los datos del nuevo vendedor:")
        legajo = input("Legajo: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")

        try:
            sql = """
            INSERT INTO vendedores (nombre, apellido, Legajo_vendedor)
            VALUES (%s, %s, %s);
            """
            self.cursor.execute(sql, (nombre, apellido, legajo))
            self.conn.commit()
            new_vendedor_id = self.cursor.lastrowid
            print(Fore.GREEN + f"Vendedor agregado con éxito. ID asignado: {new_vendedor_id}")
            return new_vendedor_id
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error al añadir vendedor: {error}")
            self.conn.rollback()
            return None
