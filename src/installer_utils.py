# /src/installer_utils.py
from pathlib import Path
from src.logs.config_logger import LoggerConfigurator
import winshell
from win32com.client import Dispatch
from pywintypes import com_error

class ProjectInstaller:
    def __init__(self):
        self.logger = LoggerConfigurator().configure()
        self.project_dir = Path(__file__).parent.parent.resolve()
        self.name_proj = self.get_project_name()

    def get_project_name(self):
        """
        Recupera el nombre del proyecto basado en el nombre del directorio principal o un archivo específico.
        """
        try:
            project_name = self.project_dir.name
            self.logger.debug(f"Nombre del proyecto detectado: {project_name}")
            return project_name
        except Exception as e:
            self.logger.error(f"Error al obtener el nombre del proyecto: {e}")
            return "Unknown_Project"

    def main(self):
        print("Iniciando instalador")
        print(f"Directorio del script: {self.project_dir}")
        print(f"Nombre del proyecto: {self.name_proj}")

        ruta_archivo_bat = self.project_dir / f"{self.name_proj}.bat"
        print(f"Ruta del archivo BAT: {ruta_archivo_bat}")
        if not ruta_archivo_bat.is_file():
            print(f"Creando archivo '{self.name_proj}.bat'")
            BatFileCreator(self.project_dir, self.name_proj, self.logger).crear_archivo_bat_con_pipenv()

        ShortcutManager(self.project_dir, self.name_proj, self.logger).create_shortcut(ruta_archivo_bat)


class ShortcutManager:
    def __init__(self, project_dir, name_proj, logger):
        self.project_dir = project_dir
        self.name_proj = name_proj
        self.logger = logger

    def verificar_icono(self, ruta_icono):
        """
        Verifica la existencia del archivo de icono.
        """
        if not ruta_icono.is_file():
            self.logger.error(f"El archivo de icono '{ruta_icono}' no existe.")
            return False
        return True

    def create_shortcut(self, ruta_archivo_bat):
        escritorio = Path(winshell.desktop())
        ruta_acceso_directo = escritorio / f"{self.name_proj}.lnk"
        ruta_icono = self.project_dir / "config" / f"{self.name_proj}.ico"

        if not self.verificar_icono(ruta_icono):
            return False

        try:
            shell = Dispatch('WScript.Shell')
            acceso_directo = shell.CreateShortCut(str(ruta_acceso_directo))
            acceso_directo.Targetpath = str(ruta_archivo_bat)
            acceso_directo.WorkingDirectory = str(self.project_dir)
            acceso_directo.IconLocation = str(ruta_icono)
            acceso_directo.save()
            self.logger.debug(f"Acceso directo {'actualizado' if ruta_acceso_directo.exists() else 'creado'} exitosamente.")
            return True
        except com_error as e:
            self.logger.error(f"No se pudo crear/actualizar el acceso directo debido a un error de COM: {e}", exc_info=True)
            return False
        except OSError as e:
            self.logger.error(f"No se pudo crear/actualizar el acceso directo debido a un error del sistema operativo: {e}", exc_info=True)
            return False


class BatFileCreator:
    def __init__(self, project_dir, name_proj, logger):
        self.project_dir = project_dir
        self.name_proj = name_proj
        self.logger = logger

    def crear_archivo_bat_con_pipenv(self):
        ruta_app_py = self.project_dir / 'run.py'
        ruta_archivo_bat = self.project_dir / f"{self.name_proj}.bat"

        contenido_bat = f"""
        pipenv run python "{ruta_app_py}"
        """

        with open(ruta_archivo_bat, 'w') as archivo_bat:
            archivo_bat.write(contenido_bat.strip())
        self.logger.debug(f"Archivo '{self.name_proj}.bat' creado exitosamente.")
        self.logger.debug(f"La dirección del archivo .bat es {ruta_archivo_bat}")
