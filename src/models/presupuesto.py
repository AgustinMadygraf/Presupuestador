#Presupuesto/src/models/presupuesto.py

class Presupuesto:
    def __init__(self, id_presupuesto, client_id, vendedor_id, entrega_incluido, fecha_presupuesto, comentario, condiciones, subtotal, tiempo_valido):
        self.id_presupuesto = id_presupuesto
        self.client_id = client_id
        self.vendedor_id = vendedor_id
        self.entrega_incluido = entrega_incluido
        self.fecha_presupuesto = fecha_presupuesto
        self.comentario = comentario
        self.condiciones = condiciones
        self.subtotal = subtotal
        self.tiempo_valido = tiempo_valido
        self.iva = self.calcular_iva()
        self.total = self.calcular_total()

    def calcular_iva(self):
        return self.subtotal * 0.21

    def calcular_total(self):
        return self.subtotal * 1.21

    def es_valido(self):
        # Implementar lógica para verificar si el presupuesto es válido
        pass

    def __str__(self):
        return f"Presupuesto ID: {self.id_presupuesto}, Cliente ID: {self.client_id}, Total: {self.total}"
