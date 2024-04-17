#src/main.py
import os
from datetime import datetime
from pdf_generator import create_pdf
from database import create_connection, create_tables
from logs.config_logger import configurar_logging

logger = configurar_logging()

def main_menu():
    print("\nPresupuestador de Proyectos")
    print("1. Confeccionar un nuevo presupuesto")
    print("2. Generar archivo PDF del presupuesto")
    print("0. Salir")
    choice = input("Elija una opción: ") or "2"
    return choice

def handle_new_presupuesto(conn):
    """
    Crea un nuevo presupuesto en la base de datos y devuelve el ID del mismo.

    """
    cursor = conn.cursor() 
    cursor.execute("SHOW TABLES LIKE 'presupuestos';")
    if cursor.fetchone() is None:
        print("No se encontró la tabla 'presupuestos'. Creando las tablas...")
        # Crear las tablas en la base de datos
        create_tables(conn)
        print("Tablas creadas exitosamente.")

    cursor.execute("SELECT MAX(ID_presupuesto) FROM presupuestos;")
    max_id = cursor.fetchone()[0]
    if max_id is None:
        max_id = 0
    new_id = max_id + 1
    print(f"Creando un nuevo presupuesto con ID {new_id}...")
    # Insertar el nuevo presupuesto en la base de datos, con el ID correspondiente. por medio de inputs
    #primero ofrece una lista de los clientes, para seleccionar uno. En caso de no estar el cliente, se puede agregar uno nuevo
    cursor.execute("SELECT * FROM clientes;")
    clientes = cursor.fetchall()
    print("Lista de clientes:")
    for cliente in clientes:
        print(f"{cliente[0]}. {cliente[1]}")
    cliente_id = input("ID del cliente o 'n' para agregar uno nuevo: ")
    if cliente_id == 'n':
        nombre_cliente = input("Nombre del cliente: ")
        cursor.execute("INSERT INTO clientes (nombre) VALUES (%s);", (nombre_cliente,))
        conn.commit()
        cliente_id = cursor.lastrowid
    else:
        cliente_id = int(cliente_id)
    #luego se ofrece una lista de los productos, para seleccionar uno. 


    



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
        print(f"Generando PDF en {full_file_path}...")
        create_pdf(data, full_file_path)
        logger.info("PDF generado exitosamente.")
        
        # Abrir el PDF automáticamente después de crearlo
        os.startfile(full_file_path)
        print(f"Abriendo el archivo {full_file_path}...")
        
    except Exception as e:
        logger.error(f"Error al generar el PDF: {e}", exc_info=True)
        print(f"Se produjo un error al generar el PDF: {e}")


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Configurar el sistema de logging
    logger.info("Iniciando la aplicación...")
    conn = create_connection()
    primera_vez = True
    while True:
        if primera_vez:
            print("¡Bienvenido al Presupuestador de Proyectos!")
            primera_vez = False
        else:
            input("Presione Enter para continuar...")
            os.system('cls' if os.name == 'nt' else 'clear')

        choice = main_menu()
        if choice == '1':
            handle_new_presupuesto(conn)
        elif choice == '2':
            handle_generate_pdf()
        elif choice == '0':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
