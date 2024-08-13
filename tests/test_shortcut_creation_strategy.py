"""
tests/test_shortcut_creation_strategy.py
Tests for the shortcut creation strategy.
"""

import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from src.install.shortcut_creation_strategy import DefaultShortcutCreationStrategy

class TestDefaultShortcutCreationStrategy(unittest.TestCase):
    """Test cases for DefaultShortcutCreationStrategy."""

    @patch('src.install.shortcut_creation_strategy.Dispatch')
    def test_create_shortcut_success(self, mock_dispatch):
        """Test creating a shortcut successfully."""
        # Arrange
        strategy = DefaultShortcutCreationStrategy()
        mock_shell = MagicMock()
        mock_shortcut = MagicMock()
        mock_dispatch.return_value = mock_shell
        mock_shell.CreateShortCut.return_value = mock_shortcut

        ruta_acceso_directo = Path("C:/fakepath/shortcut.lnk")
        ruta_archivo_bat = Path("C:/fakepath/script.bat")
        ruta_icono = Path("C:/fakepath/icon.ico")
        logger = MagicMock()

        # Act
        result = strategy.create_shortcut(ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger)

        # Assert
        mock_dispatch.assert_called_once_with('WScript.Shell')
        mock_shell.CreateShortCut.assert_called_once_with(str(ruta_acceso_directo))
        mock_shortcut.Targetpath = str(ruta_archivo_bat)
        mock_shortcut.WorkingDirectory = str(ruta_archivo_bat.parent)
        mock_shortcut.IconLocation = str(ruta_icono)
        mock_shortcut.save.assert_called_once()
        logger.debug.assert_called_once()
        self.assertTrue(result)

    @patch('src.install.shortcut_creation_strategy.Dispatch')
    def test_create_shortcut_failure(self, mock_dispatch):
        """Test failure in creating a shortcut."""
        # Arrange
        strategy = DefaultShortcutCreationStrategy()
        mock_shell = MagicMock()
        mock_dispatch.return_value = mock_shell
        mock_shell.CreateShortCut.side_effect = OSError("System error")

        ruta_acceso_directo = Path("C:/fakepath/shortcut.lnk")
        ruta_archivo_bat = Path("C:/fakepath/script.bat")
        ruta_icono = Path("C:/fakepath/icon.ico")
        logger = MagicMock()

        # Act
        result = strategy.create_shortcut(ruta_acceso_directo, ruta_archivo_bat, ruta_icono, logger)

        # Assert
        mock_dispatch.assert_called_once_with('WScript.Shell')
        mock_shell.CreateShortCut.assert_called_once_with(str(ruta_acceso_directo))
        logger.error.assert_called_once()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
