# src/models/budget_repository.py
from src.models.presupuesto import Presupuesto
import mysql.connector


class BudgetRepository:
    def __init__(self, cursor, conn):
        self.cursor = cursor
        self.conn = conn

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