"""
This module sets up the environment and runs the PresupuestadorApp.
"""

import sys
import os
from src.main import PresupuestadorApp

# Asegúrate de que el directorio `src` esté en el `PYTHONPATH`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

if __name__ == "__main__":
    app = PresupuestadorApp()
    app.iniciar()
