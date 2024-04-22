#src/client_interfaz.py
from database import create_connection, get_next_budget_id, table_exists
#from cliente_importacion import importar_clientes
from logs.config_logger import configurar_logging
from colorama import init, Fore
import tabulate

logger = configurar_logging()
init(autoreset=True)

def agregar_cliente():
    print("Ingrese los datos del cliente a continuación:")
    with create_connection() as conn:
        cursor = conn.cursor()
        ID_cliente = get_next_budget_id(cursor)
        print(f"ID_cliente: {ID_cliente}")
        CUIT = input("CUIT: ")
        Razon_social = input("Razon_social: ")
        Direccion = input("Direccion: ")
        Ubicacion_geografica = input("Ubicacion_geografica: ")
        N_contacto = input("N_contacto: ")
        nombre = input("nombre: ")
        apellido = input("apellido: ")
        Unidad_de_negocio = input("Unidad_de_negocio: ")
        Legajo_vendedor = input("Legajo_vendedor: ")
        Facturacion_anual = input("Facturacion_anual: ")
        sql = "INSERT INTO clientes (ID_cliente,CUIT,Razon_social,Direccion,Ubicacion_geografica,N_contacto,nombre,apellido,Unidad_de_negocio,Legajo_vendedor,Facturacion_anual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        cursor.execute(sql, (ID_cliente, CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual))
        conn.commit()
        print("Cliente agregado con éxito")

def print_client_list(clientes):
    headers = ["ID_cliente", "CUIT", "Razon_social", "Direccion", "Ubicacion_geografica", "N_contacto", "nombre", "apellido", "Unidad_de_negocio", "Legajo_vendedor", "Facturacion_anual"]
    table = [headers] + clientes
    print(tabulate.tabulate(table, headers="firstrow"))

def get_all_clients(cursor):
    if not table_exists(cursor, 'clientes'):
        print("The 'clientes' table does not exist. Please create it before proceeding.")
        return []
    cursor.execute("SELECT * FROM clientes;")
    return cursor.fetchall()

def select_client(cursor):
    clientes = get_all_clients(cursor)
    have_clients = bool(clientes)
    if have_clients:
        print_client_list(clientes)
        print("\nSeleccione el ID del cliente al que desea asignar el presupuesto:")
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
                else:
                    print(Fore.RED + "No se encontró un cliente con ese ID. Por favor, intente de nuevo.\n")
            else:
                print(Fore.RED + "Entrada inválida, por favor ingrese un número de ID válido.\n")
    else:
        print(Fore.RED + "No hay clientes en la lista.\n")
