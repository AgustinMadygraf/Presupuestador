"""Test module for PresupuestadorApp."""

import unittest
from unittest.mock import patch, MagicMock
from src.main import PresupuestadorApp

class TestPresupuestadorApp(unittest.TestCase):
    """Tests for the PresupuestadorApp class."""

    def setUp(self):
        """Set up the test case with mocked dependencies."""
        self._setUp_mocks()

    @patch('src.main.mysql.connector.connect', autospec=True)
    @patch('src.main.LoggerConfigurator', autospec=True)
    @patch('src.main.UserInterface', autospec=True)
    @patch('src.main.DatabaseManager', autospec=True)
    @patch('src.main.PDFGenerator', autospec=True)
    def _setUp_mocks(self, mock_pdf_generator, mock_db_manager, mock_ui, mock_logger_configurator, mock_mysql_connect):
        """Helper method to set up mocks and initialize the app."""
        # Mocking the database connection
        self.mock_conn = MagicMock()
        mock_mysql_connect.return_value = self.mock_conn

        # Mocking the logger
        self.mock_logger = MagicMock()
        mock_logger_configurator.return_value.configure.return_value = self.mock_logger

        # Initialize the app with the mocked dependencies
        self.app = PresupuestadorApp()

        # Mocking other components
        self.mock_ui = mock_ui.return_value
        self.mock_db_manager = mock_db_manager.return_value
        self.mock_pdf_generator = mock_pdf_generator.return_value

    def test_iniciar_run_once(self):
        """Test the iniciar method with run_once=True."""
        with patch.object(self.app, 'main_menu', return_value='0'):
            self.app.iniciar(run_once=True)
            self.mock_ui.mostrar_bienvenida.assert_called_once()
            self.mock_logger.debug.assert_any_call("Iniciando la aplicación")

    def test_main_menu_option_1(self):
        """Test that option 1 triggers handle_new_invoice."""
        with patch.object(self.app, 'main_menu', return_value='1'), \
             patch.object(self.app, 'handle_new_invoice') as mock_handle_new_invoice:
            self.app.iniciar(run_once=True)
            mock_handle_new_invoice.assert_called_once()

    def test_main_menu_option_2(self):
        """Test that option 2 triggers handle_generate_pdf."""
        with patch.object(self.app, 'main_menu', return_value='2'), \
             patch.object(self.app.pdf_generator, 'handle_generate_pdf') as mock_generate_pdf:
            self.app.iniciar(run_once=True)
            mock_generate_pdf.assert_called_once()

    def test_main_menu_option_0(self):
        """Test that option 0 triggers _salir_programa."""
        with patch.object(self.app, 'main_menu', return_value='0'), \
             patch.object(self.app, '_salir_programa') as mock_salir_programa:
            self.app.iniciar(run_once=True)
            mock_salir_programa.assert_called_once()

    def test_handle_new_invoice(self):
        """Test the handle_new_invoice method."""
        with patch('src.main.BudgetService', autospec=True) as mock_budget_service_class:
            mock_budget_service = mock_budget_service_class.return_value
            mock_budget_service.collect_budget_data.return_value = {"some": "data"}

            self.app.handle_new_invoice()

            mock_budget_service.collect_budget_data.assert_called_once()
            mock_budget_service.insert_budget_into_db.assert_called_once_with({"some": "data"})

    def test_invalid_option(self):
        """Test that an invalid option triggers _opcion_no_valida."""
        with patch.object(self.app, 'main_menu', return_value='invalid'), \
             patch.object(self.app, '_opcion_no_valida') as mock_opcion_no_valida:
            self.app.iniciar(run_once=True)
            mock_opcion_no_valida.assert_called_once_with('invalid')

if __name__ == '__main__':
    unittest.main()
