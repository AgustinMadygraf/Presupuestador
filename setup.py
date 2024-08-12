"""
Setup script for Presupuestador.
"""

import subprocess
import sys
import os
from src.install.dependency_manager import (
    PipUpdater, DependencyVerifier, PipDependencyInstaller, DependencyInstallerManager
)
from src.install.installer_utils import is_pipenv_updated, list_python_interpreters

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
    PYTHON_EXECUTABLE = python_interpreters[int(selected_index)] 
    if selected_index:
        PYTHON_EXECUTABLE = python_interpreters[int(selected_index)]
    else:
        PYTHON_EXECUTABLE = sys.executable

    # Lista de dependencias que se requiere verificar e instalar
    dependencies = [
        "pipenv", "winshell", "win32com.client", "pywintypes", "colorlog"
    ]

    # Crear instancias de las clases necesarias
    pip_updater = PipUpdater()
    verifier = DependencyVerifier(dependencies)
    installer_manager = DependencyInstallerManager(
        PipDependencyInstaller(), pip_updater, max_retries=3
    )

    # Verifica e instala las dependencias faltantes
    missing_dependencies = verifier.get_missing_dependencies()
    if missing_dependencies:
        pip_updater.update_pip()
        installer_manager.install_missing_dependencies(missing_dependencies)
    else:
        print("Todas las dependencias están instaladas.")

    # Verifica si pipenv está actualizado
    if not is_pipenv_updated(PYTHON_EXECUTABLE):
        print("Actualizando dependencias con pipenv...")
        subprocess.check_call([PYTHON_EXECUTABLE, '-m', 'pipenv', 'install'])

    try:
        # Intento de importar y ejecutar el instalador del proyecto
        from src.install.installer_utils import ProjectInstaller
        installer = ProjectInstaller()
        installer.main()
    except ImportError as e:
        print(f"Error al importar ProjectInstaller: {e}")