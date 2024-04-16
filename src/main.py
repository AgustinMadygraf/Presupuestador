import sqlite3
import os
import sys
from datetime import datetime
from pdf_generator import create_pdf
from database import create_connection, add_project,  get_presupuesto_restante, setup_database
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from logs.config_logger import configurar_logging

logger = configurar_logging()  # Asumimos que esta función está disponible globalmente


def main_menu():
    print("\nPresupuestador de Proyectos")
    print("1. Confeccionar un nuevo presupuesto")
    print("2. Generar archivo PDF del presupuesto")
    print("0. Salir")
    choice = input("Elija una opción: ") or "2"
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
    # Detecta el directorio base del proyecto de manera dinámica
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    output_dir = os.path.join(base_dir, 'Presupuestador\generated_pdfs')
    # Crea el directorio si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

def generate_pdf(data, file_path):
    create_pdf(data, file_path)
    print(f"PDF generado con éxito y guardado en {file_path}.")

def handle_generate_pdf(conn):
    try:
        presupuesto_id = get_presupuesto_id()
        file_path = prepare_output_directory()

        # Verificar si es el modo test y generar el nombre del archivo en consecuencia.
        if presupuesto_id is None:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # Formato de fecha y hora
            file_name = f"test_{current_time}.pdf"
            data = {'nombre_proyecto': 'N/A', 'presupuesto_total': 'N/A', 'presupuesto_gastado': 'N/A'}
            logger.info("Modo TEST activado: Generando PDF vacío.")
        else:
            data = get_presupuesto_restante(conn, presupuesto_id)
            if data is None:
                data = {'nombre_proyecto': 'N/A', 'presupuesto_total': 'N/A', 'presupuesto_gastado': 'N/A'}
                logger.warning(f"No se encontraron datos para el proyecto con ID: {presupuesto_id}")
            file_name = 'presupuesto.pdf'

        full_file_path = os.path.join(file_path, file_name)
        logger.debug(f"Ruta del archivo configurada: {full_file_path}")
        print(f"Generando PDF en {full_file_path}...")
        generate_pdf(data, full_file_path)
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
            handle_generate_pdf(conn)
        elif choice == '0':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
