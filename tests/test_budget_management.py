#Presupuestador/tests/test_budget_management.py
import unittest
from unittest.mock import MagicMock, patch
from src.models.budget_management import BudgetService
import mysql.connector

class TestBudgetService(unittest.TestCase):

    def setUp(self):
        # Mock del cursor y la conexión
        self.mock_cursor = MagicMock()
        self.mock_conn = MagicMock()
        self.budget_manager = BudgetService(self.mock_cursor, self.mock_conn)

    def test_listar_vendedores_sin_vendedores(self):
        # Simula que no hay vendedores en la base de datos
        self.mock_cursor.fetchall.return_value = []

        with patch('builtins.input', return_value=''):
            self.budget_manager.add_salesperson = MagicMock()
            vendedores = self.budget_manager.listar_vendedores()

        self.assertEqual(vendedores, [])
        self.budget_manager.add_salesperson.assert_called_once()
        self.mock_cursor.execute.assert_called_with("SELECT Legajo_vendedor, nombre, apellido FROM vendedores;")

    def test_listar_vendedores_con_vendedores(self):
        # Simula que hay vendedores en la base de datos
        vendedores_mock = [(1, 'Juan', 'Perez'), (2, 'Ana', 'Gomez')]
        self.mock_cursor.fetchall.return_value = vendedores_mock

        vendedores = self.budget_manager.listar_vendedores()

        self.assertEqual(vendedores, vendedores_mock)
        self.mock_cursor.execute.assert_called_with("SELECT Legajo_vendedor, nombre, apellido FROM vendedores;")

    def test_add_salesperson(self):
        with patch('builtins.input', side_effect=['Juan', 'Perez']):
            self.budget_manager.add_salesperson()

        self.mock_cursor.execute.assert_called_with("INSERT INTO vendedores (nombre, apellido) VALUES (%s, %s)", ('Juan', 'Perez'))
        self.mock_conn.commit.assert_called_once()

    def test_add_salesperson_error(self):
        self.mock_cursor.execute.side_effect = mysql.connector.Error()

        with patch('builtins.input', side_effect=['Juan', 'Perez']), patch('builtins.print') as mock_print:
            self.budget_manager.add_salesperson()

        mock_print.assert_called_with("Error al insertar vendedor:", self.mock_cursor.execute.side_effect)
        self.mock_conn.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()
