#Presupuestador/tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
import os
from src.main import PresupuestadorApp

class TestPresupuestadorApp(unittest.TestCase):

    @patch('os.system')
    @patch('src.main.create_connection')
    @patch('src.main.main_menu', return_value='0')
    @patch('src.main.UserInterface.mostrar_bienvenida')
    @patch('src.main.LoggerConfigurator.get_logger')
    def test_iniciar(self, mock_get_logger, mock_mostrar_bienvenida, mock_main_menu, mock_create_connection, mock_os_system):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        mock_conn = MagicMock()
        mock_create_connection.return_value = mock_conn
        
        app = PresupuestadorApp()
        app.iniciar(run_once=True)
        
        mock_os_system.assert_called_once_with('cls' if os.name == 'nt' else 'clear')
        mock_create_connection.assert_called_once()
        mock_mostrar_bienvenida.assert_called()
        mock_main_menu.assert_called()
        mock_logger.debug.assert_any_call("Iniciando la aplicación")
        mock_logger.info.assert_any_call("Saliendo del programa")

if __name__ == '__main__':
    unittest.main()
