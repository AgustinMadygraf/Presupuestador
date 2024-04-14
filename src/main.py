import sqlite3
import os
import sys
from pdf_generator import create_pdf
from database import create_connection, add_project,  get_presupuesto_restante, setup_database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logs.config_logger import configurar_logging

logger = configurar_logging()  # Asumimos que esta función está disponible globalmente


def main_menu():
    print("\nPresupuestador de Proyectos")
    print("1. Confeccionar un nuevo presupuesto")
    print("2. Añadir KPIs a un proyecto")
    print("3. Incorporar costos fijos")
    print("4. Incorporar costos variables")
    print("5. Generar archivo PDF del presupuesto")
    print("6. Salir")
    choice = input("Elija una opción: ")
    return choice

def handle_new_project(conn):
    nombre = input("Nombre del proyecto: ")
    presupuesto_total = float(input("Presupuesto total: "))
    add_project(conn, nombre, presupuesto_total)

def get_presupuesto_id():
    try:
        return int(input("ID del proyecto para el PDF: "))
    except ValueError:
        print("Se activó modo TEST, a continuación se generará un PDF vacío.")
        return None

def prepare_output_directory():
    output_dir = os.path.join('..', 'generated_pdfs')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return os.path.join(output_dir, 'presupuesto.pdf')

def generate_pdf(data, file_path):
    create_pdf(data, file_path)
    print(f"PDF generado con éxito y guardado en {file_path}.")


def handle_generate_pdf(conn):

    try:
        presupuesto_id = get_presupuesto_id()
        if presupuesto_id is None:
            logger.info("Modo TEST activado: Generando PDF vacío.")
            data = {'nombre_proyecto': 'N/A', 'presupuesto_total': 'N/A', 'presupuesto_gastado': 'N/A'}
        else:
            data = get_presupuesto_restante(conn, presupuesto_id)
            if data is None:
                data = {'nombre_proyecto': 'N/A', 'presupuesto_total': 'N/A', 'presupuesto_gastado': 'N/A'}
                logger.warning(f"No se encontraron datos para el proyecto con ID: {presupuesto_id}")

        file_path = prepare_output_directory()
        logger.debug(f"Ruta del archivo configurada: {file_path}")

        print(f"Generando PDF en {file_path}...")
        generate_pdf(data, file_path)
        logger.info("PDF generado exitosamente.")
    except Exception as e:
        logger.error(f"Error al generar el PDF: {e}", exc_info=True)
        print(f"Se produjo un error al generar el PDF: {e}")


def handle_add_kpi(conn):
    # Implementar lógica para añadir KPIs a un proyecto existente
    pass

def handle_fixed_costs(conn):
    # Implementar lógica para añadir costos fijos a un proyecto
    pass

def handle_variable_costs(conn):
    # Implementar lógica para añadir costos variables a un proyecto
    pass

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    # Configurar el sistema de logging
    conn = create_connection()
    setup_database(conn)  
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
            handle_new_project(conn)
        elif choice == '2':
            handle_add_kpi(conn)
        elif choice == '3':
            handle_fixed_costs(conn)
        elif choice == '4':
            handle_variable_costs(conn)
        elif choice == '5':
            handle_generate_pdf(conn)
        elif choice == '6':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
