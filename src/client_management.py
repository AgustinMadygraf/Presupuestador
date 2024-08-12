#presupuestador/src/client_management.py
import tabulate
from src.database import create_connection, get_next_budget_id, table_exists
from colorama import Fore
import mysql.connector
from utils import input_validado, validar_cuit, table_exists

def add_client():
    """
    Añade un nuevo cliente a la base de datos.
    """
    print("Ingrese los datos del cliente a continuación:")
    with create_connection() as conn:
        if conn is None:
            print("No se pudo establecer conexión con la base de datos.")
            return None
        cursor = conn.cursor()
        try:
            client_data = _get_client_data(cursor)
            sql = """
            INSERT INTO clientes (ID_cliente, CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(sql, client_data)
            conn.commit()
            print("Cliente agregado con éxito")
            return client_data[0]
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error al añadir cliente: {error}")
            conn.rollback()
        finally:
            cursor.close()

def _get_client_data(cursor):
    """
    Obtiene los datos del cliente desde la entrada del usuario.
    """
    ID_cliente = get_next_budget_id(cursor)
    print(f"ID_cliente: {ID_cliente}")
    CUIT = input_validado("CUIT (xx-xxxxxxxx-x): ", str, validar_cuit)
    Razon_social = input("Razon_social: ")
    Direccion = input("Direccion: ")
    Ubicacion_geografica = input("Ubicacion_geografica: ")
    N_contacto = input_validado("N_contacto (solo números): ", int)
    nombre = input("nombre: ")
    apellido = input("apellido: ")
    Unidad_de_negocio = input("Unidad_de_negocio: ")
    Legajo_vendedor = input_validado("Legajo_vendedor (solo números): ", int)
    Facturacion_anual = input_validado("Facturacion_anual (formato numérico): ", float)
    return (ID_cliente, CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual)

def print_client_list(clientes):
    headers = ["ID_cliente", "CUIT", "Razon_social", "Direccion", "Ubicacion_geografica", "N_contacto", "nombre", "apellido", "Unidad_de_negocio", "Legajo_vendedor", "Facturacion_anual"]
    table = [headers] + clientes
    print(tabulate.tabulate(table, headers="firstrow"))

def get_all_clients(cursor):
    if not table_exists(cursor, 'clientes'):
        print("La tabla 'clientes' no existe. Por favor, créela antes de continuar.")
        return []
    cursor.execute("SELECT * FROM clientes;")
    return cursor.fetchall()

