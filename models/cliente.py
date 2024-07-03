# models/cliente.py

from database import create_connection, table_exists
import mysql.connector
from colorama import Fore
import tabulate
from src.client_validation import input_validado, validar_cuit

class Cliente:
    def __init__(self, id_cliente=None, cuit=None, razon_social=None, direccion=None, ubicacion_geografica=None, n_contacto=None, nombre=None, apellido=None, unidad_de_negocio=None, legajo_vendedor=None, facturacion_anual=None):
        self.id_cliente = id_cliente
        self.cuit = cuit
        self.razon_social = razon_social
        self.direccion = direccion
        self.ubicacion_geografica = ubicacion_geografica
        self.n_contacto = n_contacto
        self.nombre = nombre
        self.apellido = apellido
        self.unidad_de_negocio = unidad_de_negocio
        self.legajo_vendedor = legajo_vendedor
        self.facturacion_anual = facturacion_anual

    @staticmethod
    def agregar_cliente():
        print("Ingrese los datos del cliente a continuación:")
        with create_connection() as conn:
            if conn is None:
                print("No se pudo establecer conexión con la base de datos.")
                return None
            cursor = conn.cursor()
            id_cliente = Cliente.get_next_cliente_id(cursor)
            print(f"ID_cliente: {id_cliente}")
            cuit = input_validado("CUIT (xx-xxxxxxxx-x): ", str, validar_cuit)
            razon_social = input("Razon_social: ")
            direccion = input("Direccion: ")
            ubicacion_geografica = input("Ubicacion_geografica: ")
            n_contacto = input_validado("N_contacto (solo números): ", int)
            nombre = input("nombre: ")
            apellido = input("apellido: ")
            unidad_de_negocio = input("Unidad_de_negocio: ")
            legajo_vendedor = input_validado("Legajo_vendedor (solo números): ", int)
            facturacion_anual = input_validado("Facturacion_anual (formato numérico): ", float)
            
            cliente = Cliente(id_cliente, cuit, razon_social, direccion, ubicacion_geografica, n_contacto, nombre, apellido, unidad_de_negocio, legajo_vendedor, facturacion_anual)
            return cliente.guardar(cursor, conn)

    @staticmethod
    def get_next_cliente_id(cursor):
        cursor.execute("SELECT MAX(ID_cliente) FROM clientes;")
        max_id = cursor.fetchone()[0]
        return max_id + 1 if max_id is not None else 1

    def guardar(self, cursor, conn):
        sql = """
        INSERT INTO clientes (ID_cliente, CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        try:
            cursor.execute(sql, (self.id_cliente, self.cuit, self.razon_social, self.direccion, self.ubicacion_geografica, self.n_contacto, self.nombre, self.apellido, self.unidad_de_negocio, self.legajo_vendedor, self.facturacion_anual))
            conn.commit()
            print("Cliente agregado con éxito")
            return self.id_cliente
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error al añadir cliente: {error}")
            conn.rollback()
        finally:
            cursor.close()

    @staticmethod
    def get_all_clients(cursor):
        if not table_exists(cursor, 'clientes'):
            print("The 'clientes' table does not exist. Please create it before proceeding.")
            return []
        cursor.execute("SELECT * FROM clientes;")
        return cursor.fetchall()

    @staticmethod
    def print_client_list(clientes):
        headers = ["ID_cliente", "CUIT", "Razon_social", "Direccion", "Ubicacion_geografica", "N_contacto", "nombre", "apellido", "Unidad_de_negocio", "Legajo_vendedor", "Facturacion_anual"]
        table = [headers] + clientes
        print(tabulate.tabulate(table, headers="firstrow"))

