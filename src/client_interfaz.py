#src/client_interfaz.py
from database import create_connection, get_next_budget_id
from logs.config_logger import configurar_logging
from colorama import init
from client_validation import input_validado, validar_cuit

logger = configurar_logging()
init(autoreset=True)

def agregar_cliente():
    print("Ingrese los datos del cliente a continuación:")
    with create_connection() as conn:
        cursor = conn.cursor()
        ID_cliente = get_next_budget_id(cursor)
        print(f"ID_cliente: {ID_cliente}")
        CUIT = input_validado("CUIT (xx-xxxxxxxx-x): ", str, validar_cuit)
        Razon_social = input("Razon_social: ")
        Direccion = input("Direccion: ")
        Ubicacion_geografica = input("Ubicacion_geografica: ")
        N_contacto = input_validado("N_contacto (solo números): ", int)
        nombre = input("nombre: ")
        apellido = input("apellido: ")
        Unidad_de_negocio = input("Unidad_de_negocio: ")
        Legajo_vendedor = input_validado("Legajo_vendedor (solo números): ", int)
        Facturacion_anual = input_validado("Facturacion_anual (formato numérico): ", float)
        
        sql = """
        INSERT INTO clientes (ID_cliente, CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(sql, (ID_cliente, CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual))
        conn.commit()
        print("Cliente agregado con éxito")







