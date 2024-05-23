#src/main.py
import os
from colorama import Fore, init
from generated_reports import handle_generate_pdf
from database import create_connection, create_tables, table_exists, insert_budget_into_db
from menu import main_menu
from config_logger import configurar_logging
from budget_management import collect_budget_data

logger = configurar_logging()
init(autoreset=True)

def check_and_create_tables(cursor, conn):
    if not table_exists(cursor, 'presupuestos'):
        logger.info("The 'presupuestos' table was not found. Creating tables...")
        create_tables(conn)
        logger.info("Tables created successfully.")

def handle_new_presupuesto(conn):
    try:
        cursor = conn.cursor()
        try:
            check_and_create_tables(cursor, conn)
            budget_data = collect_budget_data(cursor, conn)
            if budget_data:
                insert_budget_into_db(cursor, conn, budget_data)
        finally:
            cursor.close()
    except AttributeError as e:
        logger.error(f"Error: {e}. Verifique la conexión a la base de datos.")
    except Exception as e:
        logger.error(f"Se produjo un error: {e}")

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