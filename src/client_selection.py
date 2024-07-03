import re
from colorama import Fore
from database import create_connection
from src.logs.config_logger import configurar_logging
import tabulate
from colorama import init
from models.cliente import Cliente


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

def select_client(cursor):
    clientes = Cliente.get_all_clients(cursor)
    have_clients = bool(clientes)
    if have_clients:
        Cliente.print_client_list(clientes)
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
                    conn = create_connection()
                    return Cliente.agregar_cliente()  # Suponiendo que agregar_cliente() retorna el ID del nuevo cliente
                else:
                    print(Fore.RED + "No se encontró un cliente con ese ID. Por favor, intente de nuevo.\n")
            else:
                print(Fore.RED + "Entrada inválida, por favor ingrese un número de ID válido.\n")
    else:
        print(Fore.RED + "No hay clientes en la lista.\n")
        response = input("¿Desea agregar un nuevo cliente? (S/N): ")
        if response.strip().upper() == 'S':
            conn = create_connection()
            return Cliente.agregar_cliente()  # Suponiendo que agregar_cliente() retorna el ID del nuevo cliente
        else:
            return None
