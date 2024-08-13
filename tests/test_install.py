"""
Presupuestador/tests/test_setup.py
Módulo de pruebas para la configuración e instalación del proyecto Presupuestador.
Este módulo contiene pruebas unitarias para el script de configuración 'setup.py'.
"""

import unittest
import os
import sys
import tempfile
import subprocess
from pathlib import Path
from unittest.mock import patch, MagicMock
from setup import iniciar
from src.install.dependency_manager import (
    PipUpdater, PipDependencyInstaller, DependencyInstallerManager
)
from src.install.project_installer import ProjectInstaller
from src.install.project_name_utils import ProjectNameRetriever
from src.install.python_interpreter_utils import is_pipenv_updated, list_python_interpreters
from src.install.shortcut_creation_strategy import DefaultShortcutCreationStrategy


class TestSetup(unittest.TestCase):
    """
    Clase para probar el módulo de configuración.
    Prueba las funciones principales de configuración y manejo de dependencias.
    """

    def setUp(self):
        """
        Configura los objetos mock necesarios para las pruebas.
        """
        self.mock_os_system = patch('setup.os.system').start()
        self.mock_print = patch('setup.print').start()
        self.mock_input = patch('setup.input', return_value='').start()
        self.mock_list_python_interpreters = patch('setup.list_python_interpreters',
                                                   return_value=['/usr/bin/python3']).start()
        self.mock_update_pip = patch('setup.PipUpdater.update_pip').start()
        self.mock_install_missing_dependencies = patch('setup.DependencyInstallerManager.'
                                                      'install_missing_dependencies') \
            .start()
        self.mock_path_exists = patch('setup.os.path.exists')\
            .start()

    def tearDown(self):
        """
        Detiene todos los patches iniciados.
        """
        patch.stopall()

    def test_iniciar(self):
        """
        Prueba el flujo básico de la función iniciar para asegurar que se invocan
        las funciones de sistema y dependencias correctamente.
        """
        iniciar()

        self.mock_os_system.assert_called_once_with("cls" if os.name == "nt" else "clear")
        expected_calls = [
            "Iniciando instalador...",
            f"Versión de Python: {sys.version}",
            "Intérpretes de Python encontrados:",
            "[0] /usr/bin/python3"
        ]
        for call in expected_calls:
            self.mock_print.assert_any_call(call)

        self.mock_update_pip.assert_called_once()
        self.mock_install_missing_dependencies.assert_called_once_with(
            'requirements.txt'
        )

    def test_iniciar_no_requirements(self):
        """
        Verifica que se maneje correctamente la ausencia del archivo requirements.txt.
        """
        self.mock_path_exists.return_value = False

        iniciar()

        self.mock_print.assert_any_call(
            "El archivo requirements.txt no fue encontrado. No se pueden verificar "
            "las dependencias."
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

class TestProjectInstaller(unittest.TestCase):
    """
    Clase para probar la instalación del proyecto.
    """

    @patch('src.install.project_installer.LoggerConfigurator')
    @patch('src.install.project_installer.ProjectNameRetriever')
    def setUp(self, MockProjectNameRetriever, MockLoggerConfigurator):  # pylint: disable=arguments-differ
        """
        Configuración inicial para las pruebas.
        """
        self.mock_logger = MagicMock()
        MockLoggerConfigurator.return_value.configure.return_value = self.mock_logger

        self.mock_project_name_retriever = MagicMock()
        MockProjectNameRetriever.return_value = self.mock_project_name_retriever
        self.mock_project_name_retriever.get_project_name.return_value = "TestProject"

        self.installer = ProjectInstaller()

    def test_initialization(self):
        """
        Prueba la inicialización del instalador del proyecto.
        """
        self.assertEqual(self.installer.name_proj, "TestProject")
        self.mock_logger.info.assert_called_with("Logger configurado correctamente.")

    @patch('src.install.project_installer.print')
    def test_main(self, mock_print):
        """
        Prueba el método principal de instalación.
        """
        self.installer.main()
        mock_print.assert_any_call("Iniciando instalador")
        mock_print.assert_any_call(f"Directorio del script: {self.installer.project_dir}")
        mock_print.assert_any_call(f"Nombre del proyecto: {self.installer.name_proj}")

class TestProjectNameRetriever(unittest.TestCase):
    """Clase de prueba para la clase ProjectNameRetriever."""

    def test_get_project_name(self):
        """Prueba el método get_project_name."""
        retriever = ProjectNameRetriever(Path("/some/path/to/project"))
        self.assertEqual(retriever.get_project_name(), "project")

    def test_get_project_name_from_file(self):
        """Prueba el método get_project_name_from_file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir_path = Path(temp_dir)
            temp_file = temp_dir_path / "project_name.txt"
            temp_file.write_text("expected_project_name")

            retriever = ProjectNameRetriever(temp_dir_path)
            self.assertEqual(
                retriever.get_project_name_from_file("project_name.txt"),
                "expected_project_name"
            )

class TestPythonInterpreterUtils(unittest.TestCase):
    """Clase de prueba para las utilidades del intérprete de Python."""

    @patch('subprocess.run')
    def test_is_pipenv_updated_success(self, mock_subprocess_run):
        """Prueba si pipenv está actualizado cuando el comando se ejecuta correctamente."""
        mock_subprocess_run.return_value = MagicMock(returncode=0)

        self.assertTrue(is_pipenv_updated(sys.executable))
        mock_subprocess_run.assert_called_once_with(
            [sys.executable, '-m', 'pipenv', 'sync', '--dry-run'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_is_pipenv_updated_failure(self, mock_subprocess_run):
        """Prueba si pipenv no está actualizado cuando el comando falla."""
        mock_subprocess_run.return_value = MagicMock(returncode=1)

        self.assertFalse(is_pipenv_updated(sys.executable))
        mock_subprocess_run.assert_called_once_with(
            [sys.executable, '-m', 'pipenv', 'sync', '--dry-run'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_is_pipenv_updated_error(self, mock_subprocess_run):
        """Prueba si se maneja correctamente un error en la ejecución del comando pipenv."""
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'cmd')

        self.assertFalse(is_pipenv_updated(sys.executable))
        mock_subprocess_run.assert_called_once_with(
            [sys.executable, '-m', 'pipenv', 'sync', '--dry-run'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('glob.glob')
    @patch('os.path.exists')
    def test_list_python_interpreters(self, mock_exists, mock_glob):
        """Prueba la lista de intérpretes de Python encontrados en el sistema."""
        mock_glob.return_value = [
            '/usr/bin/python3.8',
            '/usr/bin/python3.9',
            '/usr/local/bin/python3.9',
        ]
        mock_exists.side_effect = lambda path: True

        expected = sorted({
            os.path.normcase(os.path.normpath('/usr/bin/python3.8')),
            os.path.normcase(os.path.normpath('/usr/bin/python3.9')),
            os.path.normcase(os.path.normpath('/usr/local/bin/python3.9')),
            os.path.normcase(os.path.normpath(sys.executable)),
        })

        self.assertEqual(list_python_interpreters(), expected)

class TestDefaultShortcutCreationStrategy(unittest.TestCase):
    """Test cases for DefaultShortcutCreationStrategy."""

    @patch('src.install.shortcut_creation_strategy.Dispatch')
    def test_create_shortcut_success(self, mock_dispatch):
        """Test creating a shortcut successfully."""
        # Arrange
        strategy = DefaultShortcutCreationStrategy()
        mock_shell = MagicMock()
        mock_shortcut = MagicMock()
        mock_dispatch.return_value = mock_shell
        mock_shell.CreateShortCut.return_value = mock_shortcut

        ruta_acceso_directo = Path("C:/fakepath/shortcut.lnk")
        ruta_archivo_bat = Path("C:/fakepath/script.bat")
        ruta_icono = Path("C:/fakepath/icon.ico")
        logger = MagicMock()

        # Act
        result = strategy.create_shortcut(ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger)

        # Assert
        mock_dispatch.assert_called_once_with('WScript.Shell')
        mock_shell.CreateShortCut.assert_called_once_with(str(ruta_acceso_directo))
        mock_shortcut.Targetpath = str(ruta_archivo_bat)
        mock_shortcut.WorkingDirectory = str(ruta_archivo_bat.parent)
        mock_shortcut.IconLocation = str(ruta_icono)
        mock_shortcut.save.assert_called_once()
        logger.debug.assert_called_once()
        self.assertTrue(result)

    @patch('src.install.shortcut_creation_strategy.Dispatch')
    def test_create_shortcut_failure(self, mock_dispatch):
        """Test failure in creating a shortcut."""
        # Arrange
        strategy = DefaultShortcutCreationStrategy()
        mock_shell = MagicMock()
        mock_dispatch.return_value = mock_shell
        mock_shell.CreateShortCut.side_effect = OSError("System error")

        ruta_acceso_directo = Path("C:/fakepath/shortcut.lnk")
        ruta_archivo_bat = Path("C:/fakepath/script.bat")
        ruta_icono = Path("C:/fakepath/icon.ico")
        logger = MagicMock()

        # Act
        result = strategy.create_shortcut(ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger)

        # Assert
        mock_dispatch.assert_called_once_with('WScript.Shell')
        mock_shell.CreateShortCut.assert_called_once_with(str(ruta_acceso_directo))
        logger.error.assert_called_once()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
