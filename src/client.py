from database import create_connection, get_next_budget_id
import tabulate

def agregar_cliente():
    print("Ingrese los datos del cliente a continuación:")
    conn = create_connection()
    cursor = conn.cursor()
    ID_cliente = get_next_budget_id(cursor)
    print(f"ID_cliente: {ID_cliente}")
    CUIT = input("CUIT: ")
    Razon_social = input("Razon_social: ")
    Direccion = input("Direccion: ")
    Ubicacion_geografica = input("Ubicacion_geografica: ")
    N_contacto = input("N_contacto: ")
    nombre = input("nombre: ")
    apellido = input("apellido: ")
    Unidad_de_negocio = input("Unidad_de_negocio: ")
    Legajo_vendedor = input("Legajo_vendedor: ")
    Facturacion_anual = input("Facturacion_anual: ")
    conn = create_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO clientes (ID_cliente,CUIT,Razon_social,Direccion,Ubicacion_geografica,N_contacto,nombre,apellido,Unidad_de_negocio,Legajo_vendedor,Facturacion_anual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    cursor.execute(sql, (ID_cliente, CUIT, Razon_social, Direccion, Ubicacion_geografica, N_contacto, nombre, apellido, Unidad_de_negocio, Legajo_vendedor, Facturacion_anual))
    conn.commit()
    print("Cliente agregado con éxito")

def print_client_list(clientes):
    headers = ["ID_cliente", "CUIT", "Razon_social", "Direccion", "Ubicacion_geografica", "N_contacto", "nombre", "apellido", "Unidad_de_negocio", "Legajo_vendedor", "Facturacion_anual"]
    table = [headers] + clientes
    print(tabulate.tabulate(table, headers="firstrow"))
