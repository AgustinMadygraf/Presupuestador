"""
tests/test_python_interpreter_utils.py 
Módulo de prueba para el módulo python_interpreter_utils.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import subprocess
from src.install.python_interpreter_utils import is_pipenv_updated, list_python_interpreters

class TestPythonInterpreterUtils(unittest.TestCase):
    """Clase de prueba para las utilidades del intérprete de Python."""

    @patch('subprocess.run')
    def test_is_pipenv_updated_success(self, mock_subprocess_run):
        """Prueba si pipenv está actualizado cuando el comando se ejecuta correctamente."""
        mock_subprocess_run.return_value = MagicMock(returncode=0)

        self.assertTrue(is_pipenv_updated(sys.executable))
        mock_subprocess_run.assert_called_once_with(
            [sys.executable, '-m', 'pipenv', 'sync', '--dry-run'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_is_pipenv_updated_failure(self, mock_subprocess_run):
        """Prueba si pipenv no está actualizado cuando el comando falla."""
        mock_subprocess_run.return_value = MagicMock(returncode=1)

        self.assertFalse(is_pipenv_updated(sys.executable))
        mock_subprocess_run.assert_called_once_with(
            [sys.executable, '-m', 'pipenv', 'sync', '--dry-run'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_is_pipenv_updated_error(self, mock_subprocess_run):
        """Prueba si se maneja correctamente un error en la ejecución del comando pipenv."""
        mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, 'cmd')

        self.assertFalse(is_pipenv_updated(sys.executable))
        mock_subprocess_run.assert_called_once_with(
            [sys.executable, '-m', 'pipenv', 'sync', '--dry-run'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('glob.glob')
    @patch('os.path.exists')
    def test_list_python_interpreters(self, mock_exists, mock_glob):
        """Prueba la lista de intérpretes de Python encontrados en el sistema."""
        mock_glob.return_value = [
            '/usr/bin/python3.8',
            '/usr/bin/python3.9',
            '/usr/local/bin/python3.9',
        ]
        mock_exists.side_effect = lambda path: True

        expected = sorted({
            os.path.normcase(os.path.normpath('/usr/bin/python3.8')),
            os.path.normcase(os.path.normpath('/usr/bin/python3.9')),
            os.path.normcase(os.path.normpath('/usr/local/bin/python3.9')),
            os.path.normcase(os.path.normpath(sys.executable)),
        })

        self.assertEqual(list_python_interpreters(), expected)


if __name__ == '__main__':
    unittest.main()
