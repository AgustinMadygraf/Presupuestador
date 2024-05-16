from client_selection import select_client, input_validado
from database import get_new_budget_id

def collect_budget_data(cursor):
    client_id = select_client(cursor)
    if client_id is None:
        return None
    print(f"Cliente seleccionado: {client_id}")
    new_id = get_new_budget_id(cursor)
    print(f"ID de presupuesto: {new_id}")
    Legajo_vendedor = input_validado("Legajo del vendedor (solo números): ", int)
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
