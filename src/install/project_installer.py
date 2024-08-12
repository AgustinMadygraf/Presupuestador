"""
Este módulo proporciona utilidades para la instalación del proyecto.
"""

from pathlib import Path
import winshell
from src.logs.config_logger import LoggerConfigurator
from src.install.shortcut_creation_strategy import (
    ShortcutCreationStrategy, DefaultShortcutCreationStrategy
)
from src.install.project_name_utils import ProjectNameRetriever


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
        ShortcutManager(
            self.project_dir, self.name_proj, self.logger, shortcut_strategy
        ).create_shortcut(ruta_archivo_bat)


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
        """
        Verifica si el archivo de ícono existe.

        :param ruta_icono: Ruta al archivo de ícono.
        :return: True si el archivo existe, False en caso contrario.
        """
        if not ruta_icono.is_file():
            self.logger.error(f"El archivo de icono '{ruta_icono}' no existe.")
            return False
        return True

    def create_shortcut(self, ruta_archivo_bat):
        """
        Crea un acceso directo en el escritorio para el archivo BAT.

        :param ruta_archivo_bat: Ruta al archivo BAT.
        :return: True si el acceso directo se creó exitosamente, False en caso contrario.
        """
        escritorio = Path(winshell.desktop())
        ruta_acceso_directo = escritorio / f"{self.name_proj}.lnk"
        ruta_icono = self.project_dir / "static" / "favicon.ico"

        if not self.verificar_icono(ruta_icono):
            return False

        return self.strategy.create_shortcut(
            ruta_acceso_directo, ruta_archivo_bat, ruta_icono, self.logger
        )


class BatFileCreator:
    """
    Clase encargada de crear archivos BAT para la ejecución del proyecto.
    """
    def __init__(self, project_dir, name_proj, logger):
        self.project_dir = project_dir
        self.name_proj = name_proj
        self.logger = logger

    def crear_archivo_bat_con_pipenv(self):
        """
        Crea un archivo BAT que ejecuta el proyecto utilizando pipenv.
        """
        ruta_app_py = self.project_dir / 'run.py'
        ruta_archivo_bat = self.project_dir / f"{self.name_proj}.bat"
