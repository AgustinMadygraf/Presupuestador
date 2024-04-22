#src/main.py
import os
from datetime import datetime
from colorama import Fore, init
from pdf_generator import handle_generate_pdf
from database import create_connection, create_tables, table_exists, get_next_budget_id
from client import select_client
from menu import main_menu
from logs.config_logger import configurar_logging
import csv
import tabulate

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
