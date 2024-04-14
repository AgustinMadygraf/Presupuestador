import sqlite3
from database import create_connection, add_project,  get_presupuesto_restante, setup_database
from pdf_generator import create_pdf

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

def handle_generate_pdf(conn):
    proyecto_id = int(input("ID del proyecto para el PDF: "))
    data = get_presupuesto_restante(conn, proyecto_id)
    create_pdf(data, 'presupuesto.pdf')
    print("PDF generado con éxito.")

def handle_add_kpi(conn):
    # Implementar lógica para añadir KPIs a un proyecto existente
    pass

def handle_fixed_costs(conn):
    # Implementar lógica para añadir costos fijos a un proyecto
    pass

def handle_variable_costs(conn):
    # Implementar lógica para añadir costos variables a un proyecto
    pass

def handle_generate_pdf(conn):
    proyecto_id = int(input("ID del proyecto para el PDF: "))
    data = get_presupuesto_restante(conn, proyecto_id)
    create_pdf(data, 'presupuesto.pdf')
    print("PDF generado con éxito.")

def main():
    conn = create_connection()
    setup_database(conn)  # Asegúrate de que las tablas están creadas antes de proceder.
    while True:
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
