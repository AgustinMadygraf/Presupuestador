#AnalizadorDeProyectos\run.py
import sys
import os

# Asegúrate de que el directorio `src` esté en el `PYTHONPATH`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.main import PresupuestadorApp

if __name__ == "__main__":
    app = PresupuestadorApp()
    input("Presione Enter para Iniciar:\n")
    app.iniciar()

