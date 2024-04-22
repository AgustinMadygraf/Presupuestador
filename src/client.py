from database import create_connection, get_next_budget_id, table_exists
import tabulate
import csv
from logs.config_logger import configurar_logging
from colorama import init, Fore

logger = configurar_logging()
init(autoreset=True)

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

def get_all_clients(cursor):
    if not table_exists(cursor, 'clientes'):
        print("The 'clientes' table does not exist. Please create it before proceeding.")
        return []
    cursor.execute("SELECT * FROM clientes;")
    return cursor.fetchall()

def importar_clientes():
    clientes = []
    try:
        logger.info("Importando clientes desde el archivo 'clientes.csv'")
        with open('database/clientes.csv', 'r') as file:
            logger.debug("Abriendo el archivo 'clientes.csv'")
            reader = csv.reader(file)
            #abrir conexion con Mysql
            conn = create_connection()
            cursor = conn.cursor()
            try:
                logger.debug("Leyendo la cabecera del archivo 'clientes.csv'")
                row_cabecera = next(reader)
                logger.debug(f"Cabecera: {row_cabecera}")

                next(reader)  
                row = next(reader)
                logger.debug("Descartando la primera fila del archivo 'clientes.csv'")
                logger.debug("Leyendo los clientes del archivo 'clientes.csv'")
                logger.debug(f"{row_cabecera[0]}: {row[0]}, {row_cabecera[1]}: {row[1]}, {row_cabecera[2]}: {row[2]}, {row_cabecera[3]}: {row[3]}, {row_cabecera[4]}: {row[4]}, {row_cabecera[5]}: {row[5]}, {row_cabecera[6]}: {row[6]}, {row_cabecera[7]}: {row[7]}")
                logger.debug("Insertando los clientes en la base de datos")
                sql = "INSERT INTO clientes (ID_cliente,CUIT,Razon_social,Direccion,Ubicacion_geografica,N_contacto,nombre,apellido,Unidad_de_negocio,Legajo_vendedor,Facturacion_anual) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10])                
                cursor.execute(sql)
                conn.commit()
                
            except StopIteration:
                logger.warning("El archivo 'clientes.csv' está vacío.")
                return clientes
            for row in reader:
                clientes.append(row)
    except FileNotFoundError:
        logger.error("No se pudo abrir el archivo 'clientes.csv'.")
    except Exception as e: #mayor detalle de este error
        logger.error(f"Error al importar clientes desde el archivo 'clientes.csv': {e}")
    return clientes

def select_client(cursor):
    clientes = get_all_clients(cursor)
    have_clients = bool(clientes)
    if have_clients:
        print_client_list(clientes)
        print("\nSeleccione el ID del cliente al que desea asignar el presupuesto:")
        client_id = input("ID del cliente: ")
        cursor.execute("SELECT * FROM clientes WHERE ID_cliente = %s;", (client_id,))
        Razon_social = cursor.fetchone()[2]
        print(f"Cliente seleccionado: {Razon_social}")
        return client_id
    else:
        print(Fore.RED + "No hay clientes en la lista.\n")
        print("Te gustaría importar clientes desde un archivo CSV?")
        importar = input("S/N: ")
        if importar.upper() == 'S':
            clientes = importar_clientes()
            print_client_list(clientes)
        else:
            print("No se importaron clientes.")
            agregar_cliente()