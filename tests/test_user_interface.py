#Presupuestador/tests/test_user_interface.py
import unittest
from unittest.mock import patch, MagicMock
from src.models.user_interface import UserInterface
import os

class TestUserInterface(unittest.TestCase):

    def setUp(self):
        self.mock_logger = MagicMock()
        self.ui = UserInterface(self.mock_logger)

    @patch('builtins.print')
    def test_mostrar_bienvenida_primera_vez(self, mock_print):
        self.ui.primera_vez = True
        self.ui.mostrar_bienvenida()
        # Actualizamos el assert_any_call para reflejar la salida real del print con colorama
        mock_print.assert_any_call("\033[32m¡Bienvenido al Presupuestador de Proyectos!\033[39m")
        mock_print.assert_any_call("")  # Esta llamada imprime una nueva línea en blanco
        self.assertFalse(self.ui.primera_vez)

    @patch('builtins.input', return_value='\n')
    @patch('os.system')
    def test_mostrar_bienvenida_reinicio(self, mock_os_system, mock_input):
        self.ui.primera_vez = False
        self.ui.mostrar_bienvenida()
        mock_input.assert_called_once_with("Presione Enter para Reiniciar:\n")
        mock_os_system.assert_called_once_with('cls' if os.name == 'nt' else 'clear')
        self.mock_logger.debug.assert_called_with("Reiniciando la aplicación por solicitud del usuario.")

if __name__ == '__main__':
    unittest.main()
