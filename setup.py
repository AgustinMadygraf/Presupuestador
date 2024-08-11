# Presupuestador/setup.py
import subprocess
import sys
import os
import glob
from src.install.dependency_manager import PipUpdater, DependencyVerifier, PipDependencyInstaller, DependencyInstallerManager

def is_pipenv_updated(python_executable: str) -> bool:
    """
    Verifica si pipenv está actualizado con Pipfile y Pipfile.lock.
    
    :param python_executable: Ruta del intérprete de Python a utilizar.
    """
    print("Verificando si pipenv está actualizado...")
    try:
        result = subprocess.run([python_executable, '-m', 'pipenv', 'sync', '--dry-run'], capture_output=True, text=True)
        if result.returncode == 0:
            print("pipenv está actualizado.")
            return True
        else:
            print("pipenv no está actualizado.")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Error al verificar pipenv. Error: {e}")
        return False

def list_python_interpreters():
    """
    Lista los intérpretes de Python instalados en el sistema, eliminando duplicados.
    """
    possible_locations = []
    
    if os.name == "nt":  # Windows
        possible_locations += glob.glob("C:\\Python*\\python.exe")
        possible_locations += glob.glob("C:\\Users\\*\\AppData\\Local\\Programs\\Python\\Python*\\python.exe")
    else:  # Unix-based systems
        possible_locations += glob.glob("/usr/bin/python*")
        possible_locations += glob.glob("/usr/local/bin/python*")
        possible_locations += glob.glob("/opt/*/bin/python*")
    
    python_paths = set()  # Utilizamos un set para eliminar duplicados
    python_paths.add(os.path.normcase(os.path.normpath(sys.executable)))  # Incluye el intérprete actual

    for path in possible_locations:
        normalized_path = os.path.normcase(os.path.normpath(path))
        if os.path.exists(normalized_path):
            python_paths.add(normalized_path)
    
    return sorted(python_paths)

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
    selected_index = input("Selecciona el número del intérprete de Python a utilizar (o deja en blanco para usar el actual): ")
    python_executable = python_interpreters[int(selected_index)] if selected_index else sys.executable

    # Lista de dependencias que se requiere verificar e instalar
    dependencies = ["pipenv", "winshell", "win32com.client", "pywintypes", "colorlog"]
    
    # Crear instancias de las clases necesarias
    pip_updater = PipUpdater()
    verifier = DependencyVerifier(dependencies)
    installer_manager = DependencyInstallerManager(PipDependencyInstaller(), pip_updater, max_retries=3)
    
    # Verifica e instala las dependencias faltantes
    missing_dependencies = verifier.get_missing_dependencies()
    if missing_dependencies:
        pip_updater.update_pip()
        installer_manager.install_missing_dependencies(missing_dependencies)
    else:
        print("Todas las dependencias están instaladas.")
    
    # Verifica si pipenv está actualizado
    if not is_pipenv_updated(python_executable):
        print("Actualizando dependencias con pipenv...")
        subprocess.check_call([python_executable, '-m', 'pipenv', 'install'])

    try:
        # Intento de importar y ejecutar el instalador del proyecto
        from src.install.installer_utils import ProjectInstaller
        installer = ProjectInstaller()
        installer.main()
    except ImportError as e:
        print(f"Error al importar ProjectInstaller: {e}")
