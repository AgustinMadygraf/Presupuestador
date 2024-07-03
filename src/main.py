import os
from colorama import Fore, init
from generated_reports import handle_generate_pdf
from database import create_connection, insert_budget_into_db, check_and_create_tables
from menu import main_menu
from budget_management import collect_budget_data
from logs.config_logger import LoggerConfigurator

init(autoreset=True)

class PresupuestadorApp:
    """
    Clase principal para la aplicación de Presupuestador de Proyectos.
    Maneja la inicialización, el ciclo principal y las opciones del menú.
    """

    def __init__(self):
        """
        Inicializa la aplicación, configurando el logger y la conexión a la base de datos.
        """
        self.logger = LoggerConfigurator().get_logger()
        self.conn = None
        self.primera_vez = True

    def iniciar(self):
        """
        Inicia la aplicación y maneja el ciclo principal.
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        self.logger.debug("Iniciando la aplicación")
        self.conn = create_connection()

        while True:
            self.mostrar_bienvenida()
            choice = main_menu()
            self.procesar_opcion(choice)

    def mostrar_bienvenida(self):
        """
        Muestra el mensaje de bienvenida al usuario.
        """
        if self.primera_vez:
            self.logger.debug("Mostrando mensaje de bienvenida por primera vez.")
            print(Fore.GREEN + "¡Bienvenido al Presupuestador de Proyectos!")
            print("")
            self.primera_vez = False
        else:
            self.logger.debug("Reiniciando la aplicación por solicitud del usuario.")
            input("Presione Enter para Reiniciar:\n")
            os.system('cls' if os.name == 'nt' else 'clear')

    def procesar_opcion(self, choice):
        """
        Procesa la opción seleccionada por el usuario en el menú principal.

        Args:
            choice (str): La opción seleccionada por el usuario.
        """
        self.logger.debug(f"Procesando opción seleccionada: {choice}")
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
        """
        Maneja la creación de un nuevo presupuesto, incluyendo la verificación y creación
        de tablas, recolección de datos e inserción en la base de datos.
        """
        try:
            self.logger.debug("Iniciando proceso para manejar un nuevo presupuesto.")
            cursor = self.conn.cursor()
            try:
                self.logger.debug("Verificando y creando tablas si es necesario.")
                check_and_create_tables(cursor, self.conn)
                self.logger.debug("Recolectando datos del presupuesto.")
                budget_data = collect_budget_data(cursor, self.conn)
                if budget_data:
                    self.logger.debug(f"Datos del presupuesto recolectados: {budget_data}")
                    insert_budget_into_db(cursor, self.conn, budget_data)
            finally:
                cursor.close()
                self.logger.debug("Cursor cerrado.")
        except AttributeError as e:
            self.logger.error(f"Error: {e}. Verifique la conexión a la base de datos.")
        except Exception as e:
            self.logger.error(f"Se produjo un error: {e}")

if __name__ == "__main__":
    app = PresupuestadorApp()
    app.iniciar()
