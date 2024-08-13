"""
Presupuestador/tests/test_project_installer.py
Módulo de pruebas para la clase ProjectInstaller en 'src/install/project_installer.py'.
"""

import unittest
from unittest.mock import patch, MagicMock
from src.install.project_installer import ProjectInstaller

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

if __name__ == '__main__':
    unittest.main()
