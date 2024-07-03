# tests/test_main.py

import unittest
from unittest.mock import patch, MagicMock
from src.main import PresupuestadorApp
from src.models.user_interface import UserInterface

class TestPresupuestadorApp(unittest.TestCase):

    @patch('src.main.create_connection')
    @patch('src.main.LoggerConfigurator')
    def setUp(self, MockLoggerConfigurator, mock_create_connection):
        # Mock del logger
        self.mock_logger = MagicMock()
        MockLoggerConfigurator().get_logger.return_value = self.mock_logger

        # Mock de la conexión a la base de datos
        self.mock_conn = MagicMock()
        mock_create_connection.return_value = self.mock_conn

        # Instancia de la aplicación
        self.app = PresupuestadorApp()

    def test_mostrar_bienvenida_primera_vez(self):
        ui = UserInterface(self.mock_logger)
        ui.mostrar_bienvenida()
        self.assertFalse(ui.primera_vez)

    def test_mostrar_bienvenida_reinicio(self):
        ui = UserInterface(self.mock_logger)
        ui.primera_vez = False
        with patch('builtins.input', return_value='\n'), patch('os.system'):
            ui.mostrar_bienvenida()
            self.mock_logger.debug.assert_called_with("Reiniciando la aplicación por solicitud del usuario.")

if __name__ == '__main__':
    unittest.main()

