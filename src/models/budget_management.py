#Presupuestador/src/models/budget_management.py
from client_selection import select_client, input_validado
from database import get_new_budget_id
from models.salesperson_manager import SalespersonManager
import mysql.connector
from colorama import Fore

class BudgetService:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def listar_vendedores(self, retry=False):
        manager = SalespersonManager(self.cursor, self.conn)
        return manager.list_salespeople()

    def insertar_vendedor(self):
        manager = SalespersonManager(self.cursor, self.conn)
        return manager.add_salesperson()

    def collect_budget_data(self):
        client_id = select_client(self.cursor)
        if client_id is None:
            return None
        print(f"Cliente seleccionado: {client_id}")
        
        new_id = get_new_budget_id(self.cursor)
        print(f"ID de presupuesto: {new_id}")

        Legajo_vendedor = self.select_salesperson()
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

    def select_salesperson(self):
        manager = SalespersonManager(self.cursor, self.conn)
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

    def insert_budget_into_db(self, budget_data):
        if budget_data is None:
            return
        try:
            sql = """
            INSERT INTO presupuestos (ID_presupuesto, Legajo_vendedor, ID_cliente, Entrega_incluido, Fecha_presupuesto, comentario, Condiciones, subtotal, tiempo_dias_valido)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            self.cursor.execute(sql, (
                budget_data["new_id"], budget_data["Legajo_vendedor"], budget_data["client_id"], 
                budget_data["Entrega_incluido"], budget_data["Fecha_presupuesto"], budget_data["comentario"], 
                budget_data["Condiciones"], budget_data["subtotal"], budget_data["tiempo_dias_valido"]
            ))
            self.conn.commit()
            print(Fore.GREEN + "Presupuesto creado con éxito.")
        except mysql.connector.Error as error:
            print(Fore.RED + f"Error al crear presupuesto: {error}")
            self.conn.rollback()
