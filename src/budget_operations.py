#Presupuestador/src/budget_operations.py
from src.client_selection import select_client, input_validado
from src.database import get_new_budget_id
from src.models.salesperson_manager import SalespersonManager

def collect_budget_data(cursor, conn):
    """
    Recolecta los datos necesarios para un nuevo presupuesto.
    """
    client_id = select_client(cursor)
    if client_id is None:
        return None
    print(f"Cliente seleccionado: {client_id}")
    
    new_id = get_new_budget_id(cursor)
    print(f"ID de presupuesto: {new_id}")

    Legajo_vendedor = select_salesperson(cursor, conn)
    if Legajo_vendedor is None:
        return None
    
    Entrega_incluido = input("Entrega incluido (S/N): ")
    Entrega_incluido = "Entrega incluida" if Entrega_incluido.upper() == 'S' else "Entrega no incluida"
    
    Fecha_presupuesto = input("Fecha de envío (YYYY-MM-DD): ")
    comentario = input("Comentario: ")
    
    Condiciones = input('Condiciones "50% Anticipo, 50% contra entrega" (S/N)": ')
    if Condiciones.upper() == "S":
        Condiciones = "50% Anticipo, 50% contra entrega"
    else:
        Condiciones = input("Ingrese las condiciones: ")
    
    subtotal = 1000
    tiempo_dias_valido = input_validado("Tiempo válido en días (solo números): ", int)

    return {
        "new_id": new_id,
        "client_id": client_id,
        "Legajo_vendedor": Legajo_vendedor,
        "Entrega_incluido": Entrega_incluido,
        "Fecha_presupuesto": Fecha_presupuesto,
        "comentario": comentario,
        "Condiciones": Condiciones,
        "subtotal": subtotal,
        "tiempo_dias_valido": tiempo_dias_valido
    }

def select_salesperson(cursor, conn):
    """
    Selecciona un vendedor de la base de datos o permite agregar uno nuevo.
    """
    manager = SalespersonManager(cursor, conn)
    while True:
        vendedores = manager.list_salespeople()
        if not vendedores:
            return None

        print("\nLista de vendedores:")
        for idx, vendedor in enumerate(vendedores, start=1):
            print(f"{idx}. {vendedor[2]} {vendedor[3]} (Legajo: {vendedor[1]})")
        print("0. Agregar nuevo vendedor")

        try:
            seleccion = int(input("\nSeleccione el número del vendedor (o 0 para agregar un nuevo vendedor): "))
            if seleccion == 0:
                manager.add_salesperson()
            elif 1 <= seleccion <= len(vendedores):
                return vendedores[seleccion - 1][1]  # [1] para Legajo_vendedor
            else:
                print("Número inválido, por favor seleccione un número de la lista.")
        except ValueError:
            print("Entrada inválida, por favor ingrese un número.")
