#src/main.py
import os
from colorama import Fore, init
from pdf_generator import handle_generate_pdf
from database import create_connection, create_tables, table_exists, get_next_budget_id
from menu import main_menu
from logs.config_logger import configurar_logging
from client_selection import select_client
from client_validation import input_validado
import mysql.connector

logger = configurar_logging()
init(autoreset=True)

def check_and_create_tables(cursor, conn):
    if not table_exists(cursor, 'presupuestos'):
        print("The 'presupuestos' table was not found. Creating tables...")
        create_tables(conn)
        print("Tables created successfully.")

def get_new_budget_id(cursor):
    new_id = get_next_budget_id(cursor)
    print(f"\nCreando un nuevo presupuesto con ID {new_id}\n")
    return new_id

def handle_new_presupuesto(conn):
    cursor = conn.cursor() 
    check_and_create_tables(cursor, conn)
    new_id = get_new_budget_id(cursor)
    client_id = select_client(cursor)
    if client_id is None:
        return
    print(f"Cliente seleccionado: {client_id}")
    print(f"ID de presupuesto: {new_id}")
    # Recopilar datos del nuevo presupuesto
    Legajo_vendedor = input_validado("Legajo del vendedor (solo números): ", int)
    Entrega_incluido = input("Entrega incluido (S/N): ")
    Fecha_envio = input("Fecha de envío (YYYY-MM-DD): ")
    comentario = input("Comentario: ")
    Condiciones = input("Condiciones: ")
    subtotal = input_validado("Subtotal (formato numérico): ", float)
    tiempo_dias_valido = input_validado("Tiempo válido en días (solo números): ", int)

    try:
        # Insertar el nuevo presupuesto en la base de datos
        sql = """
        INSERT INTO presupuestos (ID_presupuesto, Legajo_vendedor, ID_cliente, Entrega_incluido, Fecha_envio, comentario, Condiciones, subtotal, tiempo_dias_valido)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (new_id, Legajo_vendedor, client_id, Entrega_incluido, Fecha_envio, comentario, Condiciones, subtotal, tiempo_dias_valido))
        conn.commit()
        print(Fore.GREEN + "Presupuesto creado con éxito.")
    except mysql.connector.Error as error:
        print(Fore.RED + f"Error al crear presupuesto: {error}")
        conn.rollback()
    finally:
        cursor.close()

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

if __name__ == "__main__":
    main()
