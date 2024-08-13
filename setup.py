"""
setup.py
Setup script for Presupuestador.
"""

import subprocess
import sys
import os
from src.install.dependency_manager import (
    PipUpdater, PipDependencyInstaller, DependencyInstallerManager
)
from src.install.python_interpreter_utils import list_python_interpreters, is_pipenv_updated

if __name__ == "__main__":
    # Limpiar pantalla
    os.system("cls" if os.name == "nt" else "clear")

    # Imprimir mensaje de inicio
    print("Iniciando instalador...")

    # Mostrar versión de Python
    print(f"Versión de Python: {sys.version}")

    # Listar intérpretes de Python disponibles
    python_interpreters = list_python_interpreters()
    print("Intérpretes de Python encontrados:")
    for i, interpreter in enumerate(python_interpreters):
        print(f"[{i}] {interpreter}")

    # Solicitar selección de intérprete de Python
    selected_index = input(
        "Selecciona el número del intérprete de Python a utilizar "
        "(o deja en blanco para usar el actual): "
    )
    if selected_index:
        PYTHON_EXECUTABLE = python_interpreters[int(selected_index)]
    else:
        PYTHON_EXECUTABLE = sys.executable

    # Crear instancias de las clases necesarias
    pip_updater = PipUpdater()
    installer_manager = DependencyInstallerManager(
        PipDependencyInstaller(), pip_updater, max_retries=3
    )

    # Actualizar pip antes de continuar
    pip_updater.update_pip()

    # Verificar e instalar las dependencias faltantes
    REQUIREMENTS_FILE = 'requirements.txt'
    if os.path.exists(REQUIREMENTS_FILE):
        print(f"Verificando dependencias desde {REQUIREMENTS_FILE}...")
        installer_manager.install_missing_dependencies(REQUIREMENTS_FILE)
    else:
        print(f"El archivo {REQUIREMENTS_FILE} no fue encontrado. "
              "No se pueden verificar las dependencias.")

    # Verifica si pipenv está actualizado
    if not is_pipenv_updated(PYTHON_EXECUTABLE):
        print("Actualizando dependencias con pipenv...")
        subprocess.check_call([PYTHON_EXECUTABLE, '-m', 'pipenv', 'install'])

    try:
        # Intento de importar y ejecutar el instalador del proyecto
        from install.project_installer import ProjectInstaller
        installer = ProjectInstaller()
        installer.main()
    except ImportError as e:
        print(f"Error al importar ProjectInstaller: {e}")
