#Presupuestador/tests/test_cliente.py
import sys
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Agregar directorios al `PYTHONPATH`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Imprimir PYTHONPATH para depuración
print("PYTHONPATH:", sys.path)

from models.cliente import Cliente
from database import create_connection

def test_get_all_clients():
    with create_connection() as conn:
        cursor = conn.cursor()
        clientes = Cliente.get_all_clients(cursor)
        assert type(clientes) is list

def test_print_client_list():
    with create_connection() as conn:
        cursor = conn.cursor()
        clientes = Cliente.get_all_clients(cursor)
        Cliente.print_client_list(clientes)
        assert True  
