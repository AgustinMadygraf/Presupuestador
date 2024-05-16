from client_selection import select_client, input_validado
from database import get_new_budget_id, list_salespeople, agregar_vendedor
import mysql.connector


def listar_vendedores(cursor, conn):  # Añade 'conn' como argumento
    cursor.execute("SELECT Legajo_vendedor, nombre, apellido FROM vendedores;")
    vendedores = cursor.fetchall()
    if not vendedores:
        print("No hay vendedores disponibles. Por favor, inserte un nuevo vendedor.")
        insertar_vendedor(cursor, conn)  # Llama a la función para insertar un vendedor
        return listar_vendedores(cursor, conn)  # Llama recursivamente para mostrar la lista actualizada de vendedores
    else:
        print("Listaa de vendedores:")
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
    new_id = get_new_budget_id(cursor)
    print(f"ID de presupuesto: {new_id}")

    while True:
        vendedores = list_salespeople(cursor, conn)
        if not vendedores:
            return None

        print("\nLista de veendedores:")
        for idx, vendedor in enumerate(vendedores, start=1):
            print(f"{idx}. {vendedor[2]} {vendedor[3]} (Legajo: {vendedor[1]})")
        print("0. Agregar nuevo vendedor")

        try:
            seleccion = int(input("\nSeleccione el número del vendedor (o 0 para agregar un nuevo vendedor): "))
            if seleccion == 0:
                agregar_vendedor(cursor, conn)
            elif 1 <= seleccion <= len(vendedores):
                Legajo_vendedor = vendedores[seleccion - 1][1]  # [1] para Legajo_vendedor
                break
            else:
                print("Número inválido, por favor seleccione un número de la lista.")
        except ValueError:
            print("Entrada inválida, por favor ingrese un número.")
    
    Entrega_incluido = input("Entrega incluido (S/N): ")
    Fecha_envio = input("Fecha de envío (YYYY-MM-DD): ")
    comentario = input("Comentario: ")
    Condiciones = input("Condiciones: ")
    subtotal = input_validado("Subtotal (formato numérico): ", float)
    tiempo_dias_valido = input_validado("Tiempo válido en días (solo números): ", int)

    return {
        "new_id": new_id,
        "client_id": client_id,
        "Legajo_vendedor": Legajo_vendedor,
        "Entrega_incluido": Entrega_incluido,
        "Fecha_envio": Fecha_envio,
        "comentario": comentario,
        "Condiciones": Condiciones,
        "subtotal": subtotal,
        "tiempo_dias_valido": tiempo_dias_valido
    }

def select_salesperson(salespeople):
    while True:
        try:
            selection = int(input("2 - Seleccione el número del vendedor: "))
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

def select_salesperson(salespeople,cursor, conn):
    while True:
        try:
            #mostar la lista de vendedores
            print("Seleccione un vendedor:")
            print("Si no ve el vendedor que busca, puede agregar uno nuevo con el ID 0.")
            for idx, salesperson in enumerate(salespeople, start=1):
                print(f"{idx}. {salesperson[1]} {salesperson[2]} (Legajo: {salesperson[0]})")
            
            selection = int(input("3 - Seleccione el número del vendedor: "))
            if 1 <= selection <= len(salespeople):
                return salespeople[selection - 1][0]
            elif selection == 0:
                insertar_vendedor(cursor, conn)  
                return select_salesperson(salespeople,cursor, conn)  
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