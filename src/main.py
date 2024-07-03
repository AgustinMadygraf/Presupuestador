# src/main.py

import os
from colorama import Fore, init
from generated_reports import handle_generate_pdf
from database import create_connection, insert_budget_into_db, check_and_create_tables
from menu import main_menu
from budget_management import collect_budget_data
from logs.config_logger import LoggerConfigurator

init(autoreset=True)

class PresupuestadorApp:
    def __init__(self):
        self.logger = LoggerConfigurator().get_logger()
        self.conn = None
        self.primera_vez = True

    def iniciar(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.info("Iniciando la aplicación")
        self.conn = create_connection()

        while True:
            self.mostrar_bienvenida()
            choice = main_menu()
            self.procesar_opcion(choice)

    def mostrar_bienvenida(self):
        if self.primera_vez:
            print(Fore.GREEN + "¡Bienvenido al Presupuestador de Proyectos!")
            print("")
            self.primera_vez = False
        else:
            input("Presione Enter para Reiniciar:\n")
            os.system('cls' if os.name == 'nt' else 'clear')

    def procesar_opcion(self, choice):
        if choice == '1':
            self.handle_new_presupuesto()
        elif choice == '2':
            handle_generate_pdf()
        elif choice == '0':
            print("Saliendo del programa")
            self.logger.info("Saliendo del programa")
            return
        else:
            print("Opción no válida. Intente de nuevo.")
            self.logger.warning(f"Opción no válida seleccionada: {choice}")

    def handle_new_presupuesto(self):
        try:
            cursor = self.conn.cursor()
            try:
                check_and_create_tables(cursor, self.conn)
                budget_data = collect_budget_data(cursor, self.conn)
                if budget_data:
                    insert_budget_into_db(cursor, self.conn, budget_data)
            finally:
                cursor.close()
        except AttributeError as e:
            self.logger.error(f"Error: {e}. Verifique la conexión a la base de datos.")
        except Exception as e:
            self.logger.error(f"Se produjo un error: {e}")

if __name__ == "__main__":
    app = PresupuestadorApp()
    app.iniciar()
