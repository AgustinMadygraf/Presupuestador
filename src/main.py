#src/main.py
import os
from datetime import datetime
from colorama import Fore, init
from pdf_generator import create_pdf
from database import create_connection, create_tables
from logs.config_logger import configurar_logging
import csv


logger = configurar_logging()
init(autoreset=True)

def main_menu():
    print("\nPresupuestador de Proyectos")
    print("1. Confeccionar un nuevo presupuesto")
    print("2. Generar archivo PDF del presupuesto")
    print("0. Salir\n")
    choice = input(Fore.BLUE + "Elija una opción: ") or "2"
    print("")
    return choice

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

def agregar_cliente():
    print("Agregando un nuevo cliente")


def table_exists(cursor, table_name):
    cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
    return cursor.fetchone() is not None

def get_next_budget_id(cursor):
    cursor.execute("SELECT MAX(ID_presupuesto) FROM presupuestos;")
    max_id = cursor.fetchone()[0]
    return max_id + 1 if max_id is not None else 1

def get_all_clients(cursor):
    if not table_exists(cursor, 'clientes'):
        print("The 'clientes' table does not exist. Please create it before proceeding.")
        return []
    cursor.execute("SELECT * FROM clientes;")
    return cursor.fetchall()

def print_client_list(clientes):
    print("Client list:")
    for cliente in clientes:
        print(f"{cliente[0]}. {cliente[1]}")
    


def get_presupuesto_id():
    try:
        return int(input("ID del presupuesto para generar el PDF: "))
    except ValueError:
        logger.info("Modo TEST activado: Generando PDF vacío.")
        return None

def prepare_output_directory():
    # Detecta el directorio base del proyecto de manera dinámica
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    output_dir = os.path.join(base_dir, 'Presupuestador\generated_pdfs')
    # Crea el directorio si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def handle_generate_pdf():
    try:
        presupuesto_id = get_presupuesto_id()
        file_path = prepare_output_directory()

        # Verificar si es el modo test y generar el nombre del archivo en consecuencia.´
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        if presupuesto_id is None:
            file_name = f"test_{current_time}.pdf"
            data = None
        else:
            file_name = (f"presupuesto_N{presupuesto_id}_{current_time}.pdf")
            data = None # Provisorio. Obtener los datos del presupuesto desde la base de datos
        full_file_path = os.path.join(file_path, file_name)
        logger.debug(f"Ruta del archivo configurada: {full_file_path}")
        print(f"Generando PDF en {full_file_path}")
        create_pdf(data, full_file_path)
        logger.info("PDF generado exitosamente.")
        
        # Abrir el PDF automáticamente después de crearlo
        os.startfile(full_file_path)
        print(f"Abriendo el archivo {full_file_path}")
        
    except Exception as e:
        logger.error(f"Error al generar el PDF: {e}", exc_info=True)
        print(f"Se produjo un error al generar el PDF: {e}")


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
            input("Presione Enter para continuar")
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
