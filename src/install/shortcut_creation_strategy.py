"""
Este módulo define las estrategias para la creación de accesos directos.
"""

from abc import ABC, abstractmethod
from win32com.client import Dispatch
from pywintypes import com_error


class ShortcutCreationStrategy(ABC):
    """
    Clase abstracta que define la interfaz para la creación de accesos directos.
    """
    # pylint: disable=too-few-public-methods
    @abstractmethod
    def create_shortcut(self, ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger):
        """
        Método abstracto para crear un acceso directo.
        """
        pass


class DefaultShortcutCreationStrategy(ShortcutCreationStrategy):
    """
    Estrategia por defecto para la creación de accesos directos utilizando Windows Script Host.
    """
    # pylint: disable=too-few-public-methods
    def create_shortcut(self, ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger):
        """
        Crea un acceso directo en el escritorio apuntando al archivo BAT especificado.

        :param ruta_acceso_directo: Ruta donde se creará el acceso directo.
        :param ruta_archivo_bat: Ruta al archivo BAT que será el objetivo del acceso directo.
        :param ruta_icono: Ruta al archivo de icono que se usará para el acceso directo.
        :param logger: Logger para registrar el proceso.
        :return: True si la creación del acceso directo fue exitosa, False en caso de error.
        """
        try:
            shell = Dispatch('WScript.Shell')
            acceso_directo = shell.CreateShortCut(str(ruta_acceso_directo))
            acceso_directo.Targetpath = str(ruta_archivo_bat)
            acceso_directo.WorkingDirectory = str(ruta_archivo_bat.parent)
            acceso_directo.IconLocation = str(ruta_icono)
            acceso_directo.save()
            logger.debug(
                f"Acceso directo {'actualizado' if ruta_acceso_directo.exists() else 'creado'} exitosamente."
            )
            return True
        except com_error as e:
            logger.error(
                "No se pudo crear/actualizar el acceso directo debido a un error de COM: {e}",
                exc_info=True
            )
            return False
        except OSError as e:
            logger.error(
                "No se pudo crear/actualizar el acceso directo debido a un error del sistema operativo: {e}",
                exc_info=True
            )
            return False
