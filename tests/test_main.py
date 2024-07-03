#Presupuestador/tests/test_main.py
import unittest
from unittest.mock import patch, MagicMock
from src.main import PresupuestadorApp

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

    @patch('src.main.main_menu', return_value='0')
    def test_iniciar_salida(self, mock_main_menu):
        with patch('builtins.print'):
            self.app.iniciar()
        self.mock_logger.info.assert_called_with("Saliendo del programa")

    @patch('src.main.main_menu', return_value='1')
    @patch('src.main.PresupuestadorApp.handle_new_presupuesto')
    def test_iniciar_nuevo_presupuesto(self, mock_handle_new_presupuesto, mock_main_menu):
        with patch('builtins.print'):
            self.app.iniciar()
        mock_handle_new_presupuesto.assert_called_once()

    @patch('src.main.main_menu', return_value='2')
    @patch('src.main.handle_generate_pdf')
    def test_iniciar_generar_pdf(self, mock_handle_generate_pdf, mock_main_menu):
        with patch('builtins.print'):
            self.app.iniciar()
        mock_handle_generate_pdf.assert_called_once()

    @patch('src.main.PresupuestadorApp.mostrar_bienvenida')
    def test_mostrar_bienvenida_primera_vez(self, mock_mostrar_bienvenida):
        self.app.mostrar_bienvenida()
        mock_mostrar_bienvenida.assert_not_called()
        self.assertFalse(self.app.primera_vez)

    @patch('src.main.collect_budget_data')
    @patch('src.main.insert_budget_into_db')
    @patch('src.main.check_and_create_tables')
    def test_handle_new_presupuesto(self, mock_check_and_create_tables, mock_insert_budget_into_db, mock_collect_budget_data):
        mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = mock_cursor
        mock_collect_budget_data.return_value = {'dummy_data': 'value'}

        self.app.handle_new_presupuesto()

        mock_check_and_create_tables.assert_called_once_with(mock_cursor, self.mock_conn)
        mock_collect_budget_data.assert_called_once_with(mock_cursor, self.mock_conn)
        mock_insert_budget_into_db.assert_called_once_with(mock_cursor, self.mock_conn, {'dummy_data': 'value'})
        mock_cursor.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
