#src/main.py
import os
from datetime import datetime
from colorama import Fore, init
from pdf_generator import handle_generate_pdf
from database import create_connection, create_tables, table_exists, get_next_budget_id
from client import agregar_cliente, print_client_list
from menu import main_menu
from logs.config_logger import configurar_logging
import csv
import tabulate

logger = configurar_logging()
init(autoreset=True)

def handle_new_presupuesto(conn):
    """
    Creates a new budget in the database and returns its ID.
    """
    cursor = conn.cursor() 

    # Check if the 'presupuestos' or 'clientes' table exists in the database
    if not table_exists(cursor, 'presupuestos'):
        print("The 'presupuestos' table was not found. Creating tables...")
        create_tables(conn)
        print("Tables created successfully.")

    new_id = get_next_budget_id(cursor)
    print(f"\nCreando un nuevo presupuesto con ID {new_id}\n")

    # Insert the new budget into the database, with the corresponding ID. through inputs
    clientes = get_all_clients(cursor)

    # Create a boolean variable to identify whether I have a client list or not
    have_clients = bool(clientes)

    if have_clients:
        print_client_list(clientes)
        print("\nSeleccione el ID del cliente al que desea asignar el presupuesto:")
        client_id = input("ID del cliente: ")
        cursor.execute("SELECT * FROM clientes WHERE ID_cliente = %s;", (client_id,))
        Razon_social = cursor.fetchone()[2]
        print(f"Cliente seleccionado: {Razon_social}")
        #tabla del cliente seleccionado con sus respectivos valores        
        

        client = cursor.fetchone()
        if client is None:
            print(Fore.RED + "Cliente no encontrado. Por favor, inténtelo de nuevo.")
            return
        
    else:
        print(Fore.RED + "No hay clientes en la lista.\n")
        print("Te gustaría importar clientes desde un archivo CSV?")
        importar = input("S/N: ")
        if importar.upper() == 'S':
            clientes = importar_clientes()
            print_client_list(clientes)
        else:
            print("No se importaron clientes.")
            agregar_cliente()

def get_all_clients(cursor):
    if not table_exists(cursor, 'clientes'):
        print("The 'clientes' table does not exist. Please create it before proceeding.")
        return []
    cursor.execute("SELECT * FROM clientes;")
    return cursor.fetchall()

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Configurar el sistema de logging
    logger.info("Iniciando la aplicación")
    conn = create_connection()
    primera_vez = True
    while True:
        if primera_vez:
            print(Fore.GREEN +"¡Bienvenido al Presupuestador de Proyectos!")
            print("")
            primera_vez = False
        else:
            input("Presione Enter para Reiniciar:\n")
            os.system('cls' if os.name == 'nt' else 'clear')

        choice = main_menu()
        if choice == '1':
            handle_new_presupuesto(conn)
        elif choice == '2':
            handle_generate_pdf()
        elif choice == '0':
            print("Saliendo del programa")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

def importar_clientes():
    clientes = []
    try:
        logger.info("Importando clientes desde el archivo 'clientes.csv'")
        with open('database/clientes.csv', 'r') as file:
            logger.debug("Abriendo el archivo 'clientes.csv'")
            reader = csv.reader(file)
            #abrir conexion con Mysql
            conn = create_connection()
            cursor = conn.cursor()
            try:
                logger.debug("Leyendo la cabecera del archivo 'clientes.csv'")
                row_cabecera = next(reader)
                logger.debug(f"Cabecera: {row_cabecera}")

                next(reader)  
                row = next(reader)
                logger.debug("Descartando la primera fila del archivo 'clientes.csv'")
                logger.debug("Leyendo los clientes del archivo 'clientes.csv'")
                logger.debug(f"{row_cabecera[0]}: {row[0]}, {row_cabecera[1]}: {row[1]}, {row_cabecera[2]}: {row[2]}, {row_cabecera[3]}: {row[3]}, {row_cabecera[4]}: {row[4]}, {row_cabecera[5]}: {row[5]}, {row_cabecera[6]}: {row[6]}, {row_cabecera[7]}: {row[7]}")
                logger.debug("Insertando los clientes en la base de datos")
                sql = "INSERT INTO clientes (ID_cliente,CUIT,Razon_social,Direccion,Ubicacion_geografica,N_contacto,nombre,apellido,Unidad_de_negocio,Legajo_vendedor,Facturacion_anual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])                
                cursor.execute(sql)
                conn.commit()
                
            except StopIteration:
                logger.warning("El archivo 'clientes.csv' está vacío.")
                return clientes
            for row in reader:
                clientes.append(row)
    except FileNotFoundError:
        logger.error("No se pudo abrir el archivo 'clientes.csv'.")
    except Exception as e: #mayor detalle de este error
        logger.error(f"Error al importar clientes desde el archivo 'clientes.csv': {e}")
    return clientes

if __name__ == "__main__":
    main()
