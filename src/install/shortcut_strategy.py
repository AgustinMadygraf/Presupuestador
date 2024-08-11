# VisionArtificial/src/install/shorcut_strategy.py
from abc import ABC, abstractmethod
from pathlib import Path
from win32com.client import Dispatch
from pywintypes import com_error

class ShortcutCreationStrategy(ABC):
    @abstractmethod
    def create_shortcut(self, ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger):
        pass

class DefaultShortcutCreationStrategy(ShortcutCreationStrategy):
    def create_shortcut(self, ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger):
        try:
            shell = Dispatch('WScript.Shell')
            acceso_directo = shell.CreateShortCut(str(ruta_acceso_directo))
            acceso_directo.Targetpath = str(ruta_archivo_bat)
            acceso_directo.WorkingDirectory = str(ruta_archivo_bat.parent)
            acceso_directo.IconLocation = str(ruta_icono)
            acceso_directo.save()
            logger.debug(f"Acceso directo {'actualizado' if ruta_acceso_directo.exists() else 'creado'} exitosamente.")
            return True
        except com_error as e:
            logger.error(f"No se pudo crear/actualizar el acceso directo debido a un error de COM: {e}", exc_info=True)
            return False
        except OSError as e:
            logger.error(f"No se pudo crear/actualizar el acceso directo debido a un error del sistema operativo: {e}", exc_info=True)
            return False
