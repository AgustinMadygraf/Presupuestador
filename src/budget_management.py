from client_selection import select_client, input_validado
from database import get_new_budget_id
from database import list_salespeople
import mysql.connector


def listar_vendedores(cursor, conn):  # Añade 'conn' como argumento
    cursor.execute("SELECT Legajo_vendedor, nombre, apellido FROM vendedores;")
    vendedores = cursor.fetchall()
    if not vendedores:
        print("No hay vendedores disponibles. Por favor, inserte un nuevo vendedor.")
        insertar_vendedor(cursor, conn)  # Llama a la función para insertar un vendedor
        return listar_vendedores(cursor, conn)  # Llama recursivamente para mostrar la lista actualizada de vendedores
    else:
        print("Lista de vendedores:")
        for idx, vendedor in enumerate(vendedores, start=1):
            print(f"{idx}. {vendedor[1]} {vendedor[2]} (Legajo: {vendedor[0]})")
    return vendedores

def insertar_vendedor(cursor, conn):
    nombre = input("Ingrese el nombre del vendedor: ")
    apellido = input("Ingrese el apellido del vendedor: ")
    try:
        cursor.execute("INSERT INTO vendedores (nombre, apellido) VALUES (%s, %s)", (nombre, apellido))
        conn.commit()
        print("Vendedor insertado exitosamente.")
    except mysql.connector.Error as err:
        print("Error al insertar vendedor:", err)
        conn.rollback()

def collect_budget_data(cursor, conn):
    client_id = select_client(cursor)
    if client_id is None:
        return None
    print(f"Cliente seleccionado: {client_id}")

    budget_id = get_new_budget_id(cursor)
    print(f"ID de presupuesto: {budget_id}")

    salespeople = list_salespeople(cursor, conn)
    if not salespeople:
        return None

    salesperson_record_number = select_salesperson(salespeople)
    delivery_included = collect_yes_no_input("Entrega incluido (S/N): ")
    shipping_date = collect_input("Fecha de envío (YYYY-MM-DD): ")
    comment = collect_input("Comentario: ")
    terms = collect_input("Condiciones: ")
    subtotal = collect_numeric_input("Subtotal (formato numérico): ", float)
    valid_days = collect_numeric_input("Tiempo válido en días (solo números): ", int)

    return {
        "new_id": budget_id,
        "client_id": client_id,
        "Legajo_vendedor": salesperson_record_number,
        "Entrega_incluido": delivery_included,
        "Fecha_envio": shipping_date,
        "comentario": comment,
        "Condiciones": terms,
        "subtotal": subtotal,
        "tiempo_dias_valido": valid_days
    }

def select_salesperson(salespeople):
    while True:
        try:
            selection = int(input("Seleccione el número del vendedor: "))
            if 1 <= selection <= len(salespeople):
                return salespeople[selection - 1][0]
            else:
                print("Número inválido, por favor seleccione un número de la lista.")
        except ValueError:
            print("Entrada inválida, por favor ingrese un número.")

def collect_yes_no_input(prompt):
    while True:
        response = input(prompt).upper()
        if response in ['S', 'N']:
            return response
        print("Respuesta inválida, por favor ingrese 'S' o 'N'.")

def collect_input(prompt):
    return input(prompt)

def collect_numeric_input(prompt, value_type):
    while True:
        try:
            return value_type(input(prompt))
        except ValueError:
            print(f"Entrada inválida, por favor ingrese un valor de tipo {value_type.__name__}.")

def select_salesperson(salespeople):
    while True:
        try:
            #mostar la lista de vendedores
            print("Seleccione un vendedor:")
            for idx, salesperson in enumerate(salespeople, start=1):
                print(f"{idx}. {salesperson[1]} {salesperson[2]} (Legajo: {salesperson[0]})")
            
            selection = int(input("Seleccione el número del vendedor: "))
            if 1 <= selection <= len(salespeople):
                return salespeople[selection - 1][0]
            else:
                print("Número inválido, por favor seleccione un número de la lista.")
        except ValueError:
            print("Entrada inválida, por favor ingrese un número.")

def collect_yes_no_input(prompt):
    while True:
        response = input(prompt).upper()
        if response in ['S', 'N']:
            return response
        print("Respuesta inválida, por favor ingrese 'S' o 'N'.")

def collect_input(prompt):
    return input(prompt)

def collect_numeric_input(prompt, value_type):
    while True:
        try:
            return value_type(input(prompt))
        except ValueError:
            print(f"Entrada inválida, por favor ingrese un valor de tipo {value_type.__name__}.")