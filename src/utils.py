#Presupuestos/src/utils.py
import re
from colorama import Fore

def input_validado(prompt, tipo=str, validacion=None):
    """Solicita al usuario una entrada y valida su tipo y formato."""
    while True:
        entrada = input(prompt)
        try:
            entrada = tipo(entrada)
            if validacion and not validacion(entrada):
                raise ValueError
            return entrada
        except ValueError:
            print(Fore.RED + f"Entrada inválida, por favor ingrese un valor correcto para {tipo.__name__}.")

def validar_cuit(cuit):
    """Valida que el CUIT tenga el formato correcto (xx-xxxxxxxx-x)."""
    pattern = r'^\d{2}-\d{8}-\d{1}$'
    return re.match(pattern, cuit) is not None

def table_exists(cursor, table_name):
    """Verifica si una tabla existe en la base de datos."""
    cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
    return cursor.fetchone() is not None
