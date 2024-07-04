#Presupuestador/tests/test_budget_management.py
import unittest
from unittest.mock import MagicMock, patch
from src.models.budget_management import BudgetManager
import mysql.connector

class TestBudgetManager(unittest.TestCase):

    def setUp(self):
        # Mock del cursor y la conexión
        self.mock_cursor = MagicMock()
        self.mock_conn = MagicMock()
        self.budget_manager = BudgetManager(self.mock_cursor, self.mock_conn)

    def test_listar_vendedores_sin_vendedores(self):
        # Simula que no hay vendedores en la base de datos
        self.mock_cursor.fetchall.return_value = []

        with patch('builtins.input', return_value=''):
            self.budget_manager.insertar_vendedor = MagicMock()
            vendedores = self.budget_manager.listar_vendedores()

        self.assertEqual(vendedores, [])
        self.budget_manager.insertar_vendedor.assert_called_once()
        self.mock_cursor.execute.assert_called_with("SELECT Legajo_vendedor, nombre, apellido FROM vendedores;")

    def test_listar_vendedores_con_vendedores(self):
        # Simula que hay vendedores en la base de datos
        vendedores_mock = [(1, 'Juan', 'Perez'), (2, 'Ana', 'Gomez')]
        self.mock_cursor.fetchall.return_value = vendedores_mock

        vendedores = self.budget_manager.listar_vendedores()

        self.assertEqual(vendedores, vendedores_mock)
        self.mock_cursor.execute.assert_called_with("SELECT Legajo_vendedor, nombre, apellido FROM vendedores;")

    def test_insertar_vendedor(self):
        with patch('builtins.input', side_effect=['Juan', 'Perez']):
            self.budget_manager.insertar_vendedor()

        self.mock_cursor.execute.assert_called_with("INSERT INTO vendedores (nombre, apellido) VALUES (%s, %s)", ('Juan', 'Perez'))
        self.mock_conn.commit.assert_called_once()

    def test_insertar_vendedor_error(self):
        self.mock_cursor.execute.side_effect = mysql.connector.Error()

        with patch('builtins.input', side_effect=['Juan', 'Perez']), patch('builtins.print') as mock_print:
            self.budget_manager.insertar_vendedor()

        mock_print.assert_called_with("Error al insertar vendedor:", self.mock_cursor.execute.side_effect)
        self.mock_conn.rollback.assert_called_once()

    @patch('src.client_selection.select_client', return_value=1)
    @patch('src.database.get_new_budget_id', return_value=123)
    @patch('src.models.budget_management.BudgetManager.select_salesperson', return_value=456)
    @patch('src.client_selection.input_validado', return_value=30)
    def test_collect_budget_data(self, mock_input_validado, mock_select_salesperson, mock_get_new_budget_id, mock_select_client):
        with patch('builtins.input', side_effect=['S', '2024-07-03', 'Comentario', 'S']):
            budget_data = self.budget_manager.collect_budget_data()

        expected_data = {
            "new_id": 123,
            "client_id": 1,
            "Legajo_vendedor": 456,
            "Entrega_incluido": "Entrega incluida",
            "Fecha_presupuesto": '2024-07-03',
            "comentario": "Comentario",
            "Condiciones": "50% Anticipo, 50% contra entrega",
            "subtotal": 1000,
            "tiempo_dias_valido": 30
        }

        self.assertEqual(budget_data, expected_data)

    def test_select_salesperson(self):
        vendedores_mock = [(1, 123, 'Juan', 'Perez'), (2, 456, 'Ana', 'Gomez')]
        self.mock_cursor.fetchall.return_value = vendedores_mock

        with patch('builtins.input', side_effect=['2']):
            Legajo_vendedor = self.budget_manager.select_salesperson()

        self.assertEqual(Legajo_vendedor, 456)

if __name__ == '__main__':
    unittest.main()
