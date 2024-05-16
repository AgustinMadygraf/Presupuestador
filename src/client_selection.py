import tabulate
from database import create_connection
from colorama import Fore
from client_management import agregar_cliente, get_all_clients, print_client_list



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
            conn = create_connection()
            return agregar_cliente()  
        else:
            return None