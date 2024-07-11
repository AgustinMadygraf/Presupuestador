#AnalizadorDeProyectos\run.py
import sys
import os

# Asegúrate de que el directorio `src` esté en el `PYTHONPATH`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
input("Presione Enter para salir...")

from src.main import PresupuestadorApp
input("Presione Enter para salir...")

if __name__ == "__main__":
    input("Presione Enter para salir...")

    app = PresupuestadorApp()
    input("Presione Enter para salir...")

    app.iniciar()
    input("Presione Enter para salir...")

