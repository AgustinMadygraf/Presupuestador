#Presupuestador/src/client_selection.py
from colorama import Fore
from models.db_manager import DatabaseManager
from logs.config_logger import LoggerConfigurator
import tabulate
import mysql.connector
from colorama import init
from utils import input_validado, validar_cuit, table_exists


logger = LoggerConfigurator().get_logger()
init(autoreset=True)

db_manager = DatabaseManager()

def select_client(cursor):
    clientes = get_all_clients(cursor)
    have_clients = bool(clientes)
    if have_clients:
        print_client_list(clientes)
        print("\nSeleccione el ID del cliente al que desea asignar el presupuesto:")
        print("Si no ve el cliente que busca, puede agregar uno nuevo con el ID 0.")
        while True:
            client_id = input("ID del cliente: ")
            if client_id.isdigit():  # Asegura que el ID es numérico
                cursor.execute("SELECT * FROM clientes WHERE ID_cliente = %s;", (client_id,))
                selected_client = cursor.fetchone()
                if selected_client:  # Verifica que se encontró un cliente
                    print("Cliente seleccionado:")
                    headers = ["ID_cliente", "CUIT", "Razon_social", "Direccion", "Ubicacion_geografica", "N_contacto", "nombre", "apellido", "Unidad_de_negocio", "Legajo_vendedor", "Facturacion_anual"]
                    print(tabulate.tabulate([selected_client], headers=headers))
                    print("\n")
                    return client_id
                elif client_id == '0':  # Agregar nuevo cliente con ID 0
                    conn = db_manager.create_connection()
                    return add_client(cursor, conn)  # Suponiendo que add_client() retorna el ID del nuevo cliente
                else:
                    print(Fore.RED + "No se encontró un cliente con ese ID. Por favor, intente de nuevo.\n")
            else:
                print(Fore.RED + "Entrada inválida, por favor ingrese un número de ID válido.\n")
    else:
        print(Fore.RED + "No hay clientes en la lista.\n")
        response = input("¿Desea agregar un nuevo cliente? (S/N): ")
        if response.strip().upper() == 'S':
            conn = db_manager.create_connection()
            return add_client(cursor, conn)  # Suponiendo que add_client() retorna el ID del nuevo cliente
        else:
            return None

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

def add_client(cursor, conn):
    print("Ingrese los datos del nuevo cliente:")
    CUIT = input_validado("CUIT (xx-xxxxxxxx-x): ", str, validar_cuit)
    Razon_social = input("Razon social: ")
    Direccion = input("Direccion: ")
    Ubicacion_geografica = input("Ubicacion geografica: ")
    N_contacto = input_validado("Número de contacto (solo números): ", int)
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    Unidad_de_negocio = "Bolsas"
    Legajo_vendedor = input_validado("Legajo del vendedor (solo números): ", int)
    Facturacion_anual = input_validado("Facturación anual (formato numérico): ", float)

    if not (CUIT and Razon_social and nombre and apellido):
        print(Fore.RED + "Error: Faltan datos esenciales.")
        return None

    try:
        sql = """
        INSERT INTO clientes (CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual))
        conn.commit()  # Usar conn para commit, no cursor.connection
        new_client_id = cursor.lastrowid
        print(Fore.GREEN + f"Cliente agregado con éxito. ID asignado: {new_client_id}")
        return new_client_id
    except mysql.connector.Error as error:
        print(Fore.RED + f"Error al añadir cliente: {error}")
        conn.rollback()  # Usar conn para rollback, no cursor.connection
        return None
