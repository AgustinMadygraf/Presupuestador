#presupuestador/tests/test_database.py
import unittest
from unittest.mock import patch, MagicMock
import mysql.connector
from src.database import create_and_connect_db, create_database, list_salespeople, create_vendedores_table, agregar_vendedor, get_next_budget_id, get_new_budget_id

class TestDatabase(unittest.TestCase):

    @patch('mysql.connector.connect')
    def test_create_and_connect_db_success(self, mock_connect):
        # Configurar el mock para simular una conexión exitosa
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        conn = create_and_connect_db('localhost', 'user', 'password', 'test_db')
        
        self.assertTrue(conn.is_connected())
        mock_connect.assert_called_with(host='localhost', user='user', password='password', database='test_db')
        mock_conn.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_create_and_connect_db_error(self, mock_connect):
        # Configurar el mock para simular un error de conexión
        mock_connect.side_effect = mysql.connector.Error
        
        conn = create_and_connect_db('localhost', 'user', 'password', 'test_db')
        
        self.assertIsNone(conn)
        mock_connect.assert_called_with(host='localhost', user='user', password='password')

    @patch('mysql.connector.connect')
    def test_create_database(self, mock_connect):
        # Configurar el mock para simular una conexión exitosa
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        
        create_database(mock_conn, 'test_db')
        
        mock_conn.cursor.return_value.execute.assert_called_with("CREATE DATABASE IF NOT EXISTS test_db;")
        mock_conn.cursor.return_value.close.assert_called_once()

    @patch('mysql.connector.connect')
    def test_list_salespeople(self, mock_connect):
        # Configurar el mock para simular una conexión exitosa y una tabla existente
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 123, 'John', 'Doe')]
        
        vendedores = list_salespeople(mock_cursor, mock_conn)
        
        self.assertEqual(len(vendedores), 1)
        self.assertEqual(vendedores[0], (1, 123, 'John', 'Doe'))
    
    @patch('mysql.connector.connect')
    def test_create_vendedores_table(self, mock_connect):
        # Configurar el mock para simular una conexión exitosa
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        create_vendedores_table(mock_cursor, mock_conn)
        
        mock_cursor.execute.assert_called_with("""
        CREATE TABLE vendedores (
            ID_vendedor INT AUTO_INCREMENT PRIMARY KEY,
            Legajo_vendedor INT NOT NULL,
            nombre VARCHAR(255) NOT NULL,
            apellido VARCHAR(255) NOT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
        """)
        mock_conn.commit.assert_called_once()
    
    @patch('mysql.connector.connect')
    def test_agregar_vendedor(self, mock_connect):
        # Configurar el mock para simular una conexión exitosa
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        with patch('builtins.input', side_effect=['123', 'John', 'Doe']):
            new_vendedor_id = agregar_vendedor(mock_cursor, mock_conn)
        
        self.assertIsNotNone(new_vendedor_id)
        mock_cursor.execute.assert_called_with("""
        INSERT INTO vendedores (nombre, apellido, Legajo_vendedor)
        VALUES (%s, %s, %s);
        """, ('John', 'Doe', '123'))
        mock_conn.commit.assert_called_once()

    @patch('mysql.connector.connect')
    def test_get_next_budget_id(self, mock_connect):
        # Configurar el mock para simular una conexión exitosa
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (10,)
        
        next_id = get_next_budget_id(mock_cursor)
        
        self.assertEqual(next_id, 11)
        mock_cursor.execute.assert_called_with("SELECT MAX(ID_presupuesto) FROM presupuestos;")
    
    @patch('mysql.connector.connect')
    def test_get_new_budget_id(self, mock_connect):
        # Configurar el mock para simular una conexión exitosa
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (10,)
        
        new_id = get_new_budget_id(mock_cursor)
        
        self.assertEqual(new_id, 11)
        mock_cursor.execute.assert_called_with("SELECT MAX(ID_presupuesto) FROM presupuestos;")
    
if __name__ == '__main__':
    unittest.main()
