from logs.config_logger import configurar_logging
from database import create_connection
import csv

logger = configurar_logging()

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

#        print("¿Te gustaría importar clientes desde un archivo CSV?")
#        importar = input("S/N: ")
#        if importar.upper() == 'S':
#            clientes = importar_clientes()
#            print_client_list(clientes)
#        else:
#            print("No se importaron clientes.")
#            agregar_cliente()
