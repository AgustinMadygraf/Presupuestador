# VisionArtificial/src/install/installer_utils.py

from pathlib import Path
from src.logs.config_logger import LoggerConfigurator
from src.install.shortcut_strategy import ShortcutCreationStrategy, DefaultShortcutCreationStrategy  
from src.install.project_name_retriever import ProjectNameRetriever
import winshell
import subprocess
import os
import glob
import sys
from pywintypes import com_error

class ProjectInstaller:
    """
    Clase principal encargada de la instalación del proyecto.
    """
    def __init__(self):
        """
        Inicializa el instalador del proyecto.
        """
        self.logger = LoggerConfigurator().configure()
        self.project_dir = Path(__file__).parent.parent.parent.resolve()
        self.name_proj = ProjectNameRetriever(self.project_dir).get_project_name()

    def main(self):
        """
        Método principal que inicia el proceso de instalación del proyecto.
        """
        print("Iniciando instalador")
        print(f"Directorio del script: {self.project_dir}")
        print(f"Nombre del proyecto: {self.name_proj}")

        ruta_archivo_bat = self.project_dir / f"{self.name_proj}.bat"
        print(f"Ruta del archivo BAT: {ruta_archivo_bat}")
        if not ruta_archivo_bat.is_file():
            print(f"Creando archivo '{self.name_proj}.bat'")
            BatFileCreator(self.project_dir, self.name_proj, self.logger).crear_archivo_bat_con_pipenv()

        shortcut_strategy = DefaultShortcutCreationStrategy()
        ShortcutManager(self.project_dir, self.name_proj, self.logger, shortcut_strategy).create_shortcut(ruta_archivo_bat)

class ShortcutManager:
    """
    Clase responsable de gestionar la creación de accesos directos.
    """
    def __init__(self, project_dir, name_proj, logger, strategy: ShortcutCreationStrategy):
        self.project_dir = project_dir
        self.name_proj = name_proj
        self.logger = logger
        self.strategy = strategy

    def verificar_icono(self, ruta_icono):
        if not ruta_icono.is_file():
            self.logger.error(f"El archivo de icono '{ruta_icono}' no existe.")
            return False
        return True

    def create_shortcut(self, ruta_archivo_bat):
        escritorio = Path(winshell.desktop())
        ruta_acceso_directo = escritorio / f"{self.name_proj}.lnk"
        ruta_icono = self.project_dir / "config" / f"{self.name_proj}.ico"
        ruta_icono = self.project_dir / "static" / "favicon.ico"

        if not self.verificar_icono(ruta_icono):
            return False

        return self.strategy.create_shortcut(ruta_acceso_directo, ruta_archivo_bat, ruta_icono, self.logger)

class BatFileCreator:
    """
    Clase encargada de crear archivos BAT para la ejecución del proyecto.
    """
    def __init__(self, project_dir, name_proj, logger):
        self.project_dir = project_dir
        self.name_proj = name_proj
        self.logger = logger

    def crear_archivo_bat_con_pipenv(self):
        ruta_app_py = self.project_dir / 'run.py'
        ruta_archivo_bat = self.project_dir / f"{self.name_proj}.bat"

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
