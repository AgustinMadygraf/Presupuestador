"""
VisionArtificial/tests/test_dependency_manager.py
Módulo de pruebas para la gestión de dependencias en el proyecto Presupuestador.
Este módulo contiene pruebas unitarias para las clases en 'src/install/dependency_manager.py'.
"""

import unittest
import sys
from unittest.mock import patch
from src.install.dependency_manager import (
    PipUpdater, PipDependencyInstaller, DependencyInstallerManager
)

class TestPipUpdater(unittest.TestCase):
    """
    Clase para probar la actualización de pip.
    """
    @patch('subprocess.check_call')
    def test_update_pip(self, mock_run):
        """
        Prueba que PipUpdater actualice pip correctamente.
        """
        pip_updater = PipUpdater()
        pip_updater.update_pip()
        mock_run.assert_called_with([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip'])

class TestPipDependencyInstaller(unittest.TestCase):
    """
    Clase para probar la instalación de dependencias usando pip.
    """
    @patch('subprocess.check_call')
    def test_install(self, mock_run):
        """
        Prueba que PipDependencyInstaller instale una dependencia correctamente.
        """
        installer = PipDependencyInstaller()
        installer.install('some-package')
        mock_run.assert_called_with([sys.executable, '-m', 'pip', 'install', 'some-package'])

class TestDependencyInstallerManager(unittest.TestCase):
    """
    Clase para probar la gestión de instalación de dependencias.
    """
    def test_install_missing_dependencies(self):
        """
        Prueba la instalación de dependencias faltantes.
        """
        installer = PipDependencyInstaller()  # Usar la subclase concreta
        pip_updater = PipUpdater()
        manager = DependencyInstallerManager(installer, pip_updater)
        manager.install_missing_dependencies()


if __name__ == '__main__':
    unittest.main()
