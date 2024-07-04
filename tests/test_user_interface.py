#Presupuestador/tests/test_user_interface.py
import unittest
from unittest.mock import patch, MagicMock
from src.models.user_interface import UserInterface  # Verifica que la ruta sea correcta
import os
import re

class TestUserInterface(unittest.TestCase):

    def setUp(self):
        self.mock_logger = MagicMock()
        self.ui = UserInterface(self.mock_logger)

    @patch('builtins.print')
    def test_mostrar_bienvenida_primera_vez(self, mock_print):
        self.ui.primera_vez = True
        self.ui.mostrar_bienvenida()
        # Capturamos los argumentos pasados a print
        print_args = mock_print.call_args_list[0][0][0]
        # Eliminamos las secuencias de escape de color para comparar el texto
        stripped_text = re.sub(r'\x1b\[.*?m', '', print_args)
        self.assertEqual(stripped_text, "¡Bienvenido al Presupuestador de Proyectos!\n")
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
