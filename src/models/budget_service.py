#Presupuestador/src/models/budget_management.py
from client_selection import select_client, input_validado
from database import get_new_budget_id
from models.salesperson_manager import SalespersonManager
from models.presupuesto import Presupuesto
import mysql.connector
from colorama import Fore

class BudgetService:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

    def collect_budget_data(self):
        client_id = self._select_client()
        if client_id is None:
            return None

        new_id = self._get_new_budget_id()
        vendedor_id = self._select_salesperson()
        if vendedor_id is None:
            return None

        entrega_incluido = self._get_entrega_incluido()
        fecha_presupuesto = input("Fecha de envío (YYYY-MM-DD): ")
        comentario = input("Comentario: ")
        condiciones = self._get_condiciones()

        subtotal = 1000
        tiempo_valido = input_validado("Tiempo válido en días (solo números): ", int)

        presupuesto = Presupuesto(
            id_presupuesto=new_id,
            client_id=client_id,
            vendedor_id=vendedor_id,
            entrega_incluido=entrega_incluido,
            fecha_presupuesto=fecha_presupuesto,
            comentario=comentario,
            condiciones=condiciones,
            subtotal=subtotal,
            tiempo_valido=tiempo_valido
        )

        return presupuesto

    def _select_client(self):
        client_id = select_client(self.cursor)
        if client_id is not None:
            print(f"Cliente seleccionado: {client_id}")
        return client_id

    def _get_new_budget_id(self):
        new_id = get_new_budget_id(self.cursor)
        print(f"ID de presupuesto: {new_id}")
        return new_id

    def _select_salesperson(self):
        manager = SalespersonManager(self.cursor, self.conn)
        while True:
            vendedores = manager.list_salespeople()
            if not vendedores:
                self.add_salesperson()
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

    def _get_entrega_incluido(self):
        entrega_incluido = input("Entrega incluido (S/N): ")
        return "Entrega incluida" if entrega_incluido.upper() == 'S' else "Entrega no incluida"

    def _get_condiciones(self):
        condiciones = input('Condiciones "50% Anticipo, 50% contra entrega" (S/N)": ')
        if condiciones.upper() == "S":
            return "50% Anticipo, 50% contra entrega"
        else:
            return input("Ingrese las condiciones: ")

    def insert_budget_into_db(self, presupuesto):
        if presupuesto is None:
            return
        try:
            sql = """
            INSERT INTO presupuestos (ID_presupuesto, Legajo_vendedor, ID_cliente, Entrega_incluido, Fecha_presupuesto, comentario, Condiciones, subtotal, tiempo_dias_valido)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            self.cursor.execute(sql, (
                presupuesto.id_presupuesto, presupuesto.vendedor_id, presupuesto.client_id, 
                presupuesto.entrega_incluido, presupuesto.fecha_presupuesto, presupuesto.comentario, 
                presupuesto.condiciones, presupuesto.subtotal, presupuesto.tiempo_valido
            ))
            self.conn.commit()
            print("Presupuesto creado con éxito.")
        except mysql.connector.Error as error:
            print(f"Error al crear presupuesto: {error}")
            self.conn.rollback()

    def add_salesperson(self):
        """
        Añade un nuevo vendedor a la base de datos.
        """
        nombre = input("Nombre del vendedor: ")
        apellido = input("Apellido del vendedor: ")
        legajo = input("Legajo del vendedor: ")
        try:
            sql = "INSERT INTO vendedores (nombre, apellido, Legajo_vendedor) VALUES (%s, %s, %s)"
            self.cursor.execute(sql, (nombre, apellido, legajo))
            self.conn.commit()
            print("Vendedor agregado con éxito.")
        except mysql.connector.Error as error:
            print(f"Error al insertar vendedor: {error}")
            self.conn.rollback()

    def listar_vendedores(self):
        """
        Lista los vendedores en la base de datos.
        """
        try:
            sql = "SELECT ID_vendedor, Legajo_vendedor, nombre, apellido FROM vendedores"
            self.cursor.execute(sql)
            vendedores = self.cursor.fetchall()
            if not vendedores:
                print("No hay vendedores disponibles.")
                self.add_salesperson()
                return []
            return vendedores
        except mysql.connector.Error as error:
            print(f"Error al listar vendedores: {error}")
            return []
