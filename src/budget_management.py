from client_selection import select_client, input_validado
from database import get_new_budget_id

import mysql.connector
from client_selection import select_client, input_validado
from database import get_new_budget_id

def listar_vendedores(cursor):
    cursor.execute("SELECT Legajo_vendedor, nombre, apellido FROM vendedores;")
    vendedores = cursor.fetchall()
    if not vendedores:
        print("No hay vendedores disponibles.")
        return []
    
    print("Lista de vendedores:")
    for idx, vendedor in enumerate(vendedores, start=1):
        print(f"{idx}. {vendedor[1]} {vendedor[2]} (Legajo: {vendedor[0]})")
    
    return vendedores

def collect_budget_data(cursor):
    client_id = select_client(cursor)
    if client_id is None:
        return None
    print(f"Cliente seleccionado: {client_id}")
    new_id = get_new_budget_id(cursor)
    print(f"ID de presupuesto: {new_id}")

    vendedores = listar_vendedores(cursor)
    if not vendedores:
        return None
    
    while True:
        try:
            seleccion = int(input("Seleccione el número del vendedor: "))
            if 1 <= seleccion <= len(vendedores):
                Legajo_vendedor = vendedores[seleccion - 1][0]
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

