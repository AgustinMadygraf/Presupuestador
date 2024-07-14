#Presupuestador/src/main.py
import os
from colorama import Fore, init
from models.db_manager import DatabaseManager
from models.user_interface import UserInterface
from models.budget_service import BudgetService
from models.pdf_generator import PDFGenerator
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
        self.ui = UserInterface(self.logger)
        self.db_manager = DatabaseManager()
        self.pdf_generator = PDFGenerator()  

    def iniciar(self, run_once=False):
        """
        Inicia la aplicación y muestra el menú principal.
        """
        self._clear_screen()
        self.logger.debug("Iniciando la aplicación")
        self.conn = self.db_manager.create_connection()

        while True:
            self.ui.mostrar_bienvenida()
            choice = self.main_menu()
            self.procesar_opcion(choice)
            if run_once:
                break

    def _clear_screen(self):
        """
        Limpia la pantalla de la terminal.
        """
        os.system('cls' if os.name == 'nt' else 'clear')

    def main_menu(self):
        """
        Muestra el menú principal y obtiene la opción seleccionada por el usuario.
        """
        print("\nPresupuestador de Proyectos")
        print("1. Confeccionar un nuevo presupuesto")
        print("2. Generar archivo PDF del presupuesto")
        print("0. Salir\n")
        choice = input(Fore.BLUE + "Elija una opción: ") or "2"
        print("")
        return choice

    def procesar_opcion(self, choice):
        """
        Procesa la opción seleccionada del menú.
        """
        self.logger.debug(f"Procesando opción seleccionada: {choice}")
        if choice == '1':
            self.handle_new_invoice()   
        elif choice == '2':
            self.pdf_generator.handle_generate_pdf()
        elif choice == '0':
            self._salir_programa()
        else:
            self._opcion_no_valida(choice)

    def handle_new_invoice(self):
        """
        Maneja el proceso de creación de un nuevo presupuesto.
        """
        try:
            self.logger.debug("Iniciando proceso para manejar un nuevo presupuesto.")
            cursor = self.conn.cursor()
            budget_service = BudgetService(cursor, self.conn)
            try:
                self.logger.debug("Recolectando datos del presupuesto.")
                presupuesto = budget_service.collect_budget_data()
                if presupuesto:
                    self.logger.debug(f"Datos del presupuesto recolectados: {presupuesto}")
                    budget_service.insert_budget_into_db(presupuesto)
            finally:
                cursor.close()
                self.logger.debug("Cursor cerrado.")
        except AttributeError as e:
            self.logger.error(f"Error: {e}.")
        except Exception as e:
            self.logger.error(f"Se produjo un error: {e}")

    def _salir_programa(self):
        """
        Sale del programa.
        """
        print("Saliendo del programa")
        self.logger.info("Saliendo del programa")

    def _opcion_no_valida(self, choice):
        """
        Maneja la selección de una opción no válida.
        """
        print("Opción no válida. Intente de nuevo.")
        self.logger.warning(f"Opción no válida seleccionada: {choice}")