# src/models/budget_management.py
import mysql.connector
from database import get_new_budget_id, list_salespeople, agregar_vendedor
from client_selection import select_client, input_validado

class BudgetManager:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def listar_vendedores(self, retry=False):
        self.cursor.execute("SELECT Legajo_vendedor, nombre, apellido FROM vendedores;")
        vendedores = self.cursor.fetchall()
        if not vendedores:
            if not retry:
                print("No hay vendedores disponibles. Por favor, inserte un nuevo vendedor.")
                self.insertar_vendedor()
                return self.listar_vendedores(retry=True)
            else:
                return []
        else:
            print("Lista de vendedores:")
            for idx, vendedor in enumerate(vendedores, start=1):
                print(f"{idx}. {vendedor[1]} {vendedor[2]} (Legajo: {vendedor[0]})")
        return vendedores

    def insertar_vendedor(self):
        nombre = input("Ingrese el nombre del vendedor: ")
        apellido = input("Ingrese el apellido del vendedor: ")
        try:
            self.cursor.execute("INSERT INTO vendedores (nombre, apellido) VALUES (%s, %s)", (nombre, apellido))
            self.conn.commit()
            print("Vendedor insertado exitosamente.")
        except mysql.connector.Error as err:
            print("Error al insertar vendedor:", err)
            self.conn.rollback()

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
        while True:
            vendedores = list_salespeople(self.cursor, self.conn)
            if not vendedores:
                return None

            print("\nLista de vendedores:")
            for idx, vendedor in enumerate(vendedores, start=1):
                print(f"{idx}. {vendedor[2]} {vendedor[3]} (Legajo: {vendedor[1]})")
            print("0. Agregar nuevo vendedor")

            try:
                seleccion = int(input("\nSeleccione el número del vendedor (o 0 para agregar un nuevo vendedor): "))
                if seleccion == 0:
                    agregar_vendedor(self.cursor, self.conn)
                elif 1 <= seleccion <= len(vendedores):
                    return vendedores[seleccion - 1][1]  # [1] para Legajo_vendedor
                else:
                    print("Número inválido, por favor seleccione un número de la lista.")
            except ValueError:
                print("Entrada inválida, por favor ingrese un número.")
