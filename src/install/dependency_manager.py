"""
Este módulo proporciona clases para la gestión de dependencias, incluyendo la actualización de pip,
la instalación de dependencias y la verificación de dependencias faltantes.
"""

import subprocess
import sys


class PipUpdater:
    """
    Clase responsable de actualizar pip a la última versión disponible.
    """
    # pylint: disable=too-few-public-methods
    def update_pip(self) -> None:
        """
        Actualiza pip utilizando el comando `pip install --upgrade pip`.
        """
        print("Actualizando pip...")
        try:
            # Ejecuta el comando para actualizar pip
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])
            print("pip actualizado correctamente.")
        except subprocess.CalledProcessError as e:
            print(f"No se pudo actualizar pip. Error: {e}")


class DependencyInstaller:
    """
    Interfaz para la instalación de dependencias.
    Las clases que hereden de esta deberán implementar el método `install`.
    """
    def install(self, dependency: str) -> None:
        """
        Método para instalar una dependencia. Debe ser implementado por una subclase.
        """
        raise NotImplementedError("Este método debe ser implementado por una subclase")


class PipDependencyInstaller(DependencyInstaller):
    """
    Clase concreta que implementa la instalación de dependencias usando pip.
    """
    def install(self, dependency: str) -> bool:
        """
        Instala una dependencia usando pip.

        :param dependency: Nombre de la dependencia a instalar.
        :return: True si la instalación fue exitosa, False en caso contrario.
        """
        print(f"Instalando {dependency} usando pip...")
        try:
            # Ejecuta el comando pip para instalar la dependencia
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dependency])
            print(f"{dependency} instalado correctamente.")
            return True
        except subprocess.CalledProcessError as e:
            print(f"No se pudo instalar {dependency}. Error: {e}")
            return False


class DependencyVerifier:
    """
    Clase responsable de verificar las dependencias faltantes.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, dependencies: list):
        """
        Inicializa la clase DependencyVerifier con una lista de dependencias.

        :param dependencies: Lista de nombres de dependencias a verificar.
        """
        self.dependencies = dependencies

    def get_missing_dependencies(self) -> list:
        """
        Verifica qué dependencias están faltando y devuelve una lista de ellas.

        :return: Lista de dependencias que no están instaladas.
        """
        missing_dependencies = []
        for dependency in self.dependencies:
            try:
                # Intenta importar la dependencia para verificar si está instalada
                __import__(dependency)
            except ImportError:
                # Si falla la importación, agrega la dependencia a la lista de faltantes
                missing_dependencies.append(dependency)
        return missing_dependencies


class DependencyInstallerManager:
    """
    Clase responsable de instalar las dependencias faltantes.
    """
    # pylint: disable=too-few-public-methods
    def __init__(self, installer: DependencyInstaller, pip_updater: PipUpdater, max_retries: int = 3):
        """
        Inicializa la clase DependencyInstallerManager con un instalador, un actualizador de pip 
        y un número máximo de reintentos.

        :param installer: Instancia de una clase que hereda de DependencyInstaller.
        :param pip_updater: Instancia de PipUpdater para actualizar pip antes de instalar dependencias.
        :param max_retries: Número máximo de intentos para instalar cada dependencia.
        """
        self.installer = installer
        self.pip_updater = pip_updater
        self.max_retries = max_retries

    def install_missing_dependencies(self, missing_dependencies: list) -> None:
        """
        Instala las dependencias faltantes utilizando el instalador proporcionado.
        Si una instalación falla, se reintentará hasta max_retries veces.

        :param missing_dependencies: Lista de dependencias que necesitan ser instaladas.
        """
        failed_dependencies = []  # Lista para almacenar dependencias que no se pudieron instalar

        print(
            f"Las siguientes dependencias están faltantes: "
            f"{', '.join(missing_dependencies)}"
        )
        print("Intentando instalar dependencias faltantes...")

        for dep in missing_dependencies:
            success = False
            for attempt in range(self.max_retries):
                print(
                    f"Intentando instalar {dep} (intento {attempt + 1}/{self.max_retries})..."
                )
                if self.installer.install(dep):
                    success = True
                    break
                print(f"Reintentando instalación de {dep}...")

            if not success:
                print(
                    f"Fallo la instalación de {dep} después de {self.max_retries} intentos."
                )
                failed_dependencies.append(dep)

        if failed_dependencies:
            print("Las siguientes dependencias no pudieron ser instaladas:")
            print(", ".join(failed_dependencies))
        else:
            print("Todas las dependencias fueron instaladas exitosamente.")
