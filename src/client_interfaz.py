#src/client_interfaz.py
from database import create_connection, get_next_budget_id, table_exists
from logs.config_logger import configurar_logging
from colorama import init, Fore
import tabulate
import re
import mysql.connector

logger = configurar_logging()
init(autoreset=True)

def validar_cuit(cuit):
    """Valida que el CUIT tenga el formato correcto (xx-xxxxxxxx-x)."""
    pattern = r'^\d{2}-\d{8}-\d{1}$'
    return re.match(pattern, cuit) is not None

def input_validado(prompt, tipo=str, validacion=None):
    """Solicita al usuario una entrada y valida su tipo y formato."""
    while True:
        entrada = input(prompt)
        try:
            entrada = tipo(entrada)
            if validacion and not validacion(entrada):
                raise ValueError
            return entrada
        except ValueError:
            print(Fore.RED + f"Entrada inválida, por favor ingrese un valor correcto para {tipo.__name__}.")

def agregar_cliente():
    print("Ingrese los datos del cliente a continuación:")
    with create_connection() as conn:
        cursor = conn.cursor()
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
        
        sql = """
        INSERT INTO clientes (ID_cliente, CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
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
        response = input("¿Desea agregar un nuevo cliente? (S/N): ")
        if response.strip().upper() == 'S':
            return agregar_cliente(cursor)  # Suponiendo que agregar_cliente() retorna el ID del nuevo cliente
        else:
            return None

def agregar_cliente(cursor):
    print("Ingrese los datos del nuevo cliente:")
    CUIT = input_validado("CUIT (xx-xxxxxxxx-x): ", str, validar_cuit)
    Razon_social = input("Razon social: ")
    Direccion = input("Direccion: ")
    Ubicacion_geografica = input("Ubicacion geografica: ")
    N_contacto = input_validado("Número de contacto (solo números): ", int)
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    Unidad_de_negocio = input("Unidad de negocio: ")
    Legajo_vendedor = input_validado("Legajo del vendedor (solo números): ", int)
    Facturacion_anual = input_validado("Facturación anual (formato numérico): ", float)

    # Verificar que los datos esenciales no estén vacíos
    if not (CUIT and Razon_social and nombre and apellido):
        print(Fore.RED + "Error: Faltan datos esenciales.")
        return None

    try:
        # Inserción de los datos en la base de datos
        sql = """
        INSERT INTO clientes (CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual))
        cursor.connection.commit()

        # Obtener el ID del cliente recién insertado
        new_client_id = cursor.lastrowid
        print(Fore.GREEN + f"Cliente agregado con éxito. ID asignado: {new_client_id}")
        return new_client_id
    except mysql.connector.Error as error:
        print(Fore.RED + f"Error al añadir cliente: {error}")
        cursor.connection.rollback()
        return None


