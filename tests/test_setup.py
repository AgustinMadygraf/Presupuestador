"""
VisionArtificial/tests/test_setup.py
Módulo de pruebas para la configuración e instalación del proyecto Presupuestador.
Este módulo contiene pruebas unitarias para el script de configuración 'setup.py'.
"""

import unittest
import os
import sys
from unittest.mock import patch
from setup import iniciar

class TestSetup(unittest.TestCase):
    """
    Clase para probar el módulo de configuración.
    Prueba las funciones principales de configuración y manejo de dependencias.
    """

    def setUp(self):
        """
        Configura los objetos mock necesarios para las pruebas.
        """
        self.mock_os_system = patch('setup.os.system').start()
        self.mock_print = patch('setup.print').start()
        self.mock_input = patch('setup.input', return_value='').start()
        self.mock_list_python_interpreters = patch('setup.list_python_interpreters',
                                                   return_value=['/usr/bin/python3']).start()
        self.mock_update_pip = patch('setup.PipUpdater.update_pip').start()
        self.mock_install_missing_dependencies = patch('setup.DependencyInstallerManager.'
                                                      'install_missing_dependencies') \
            .start()
        self.mock_path_exists = patch('setup.os.path.exists')\
            .start()

    def tearDown(self):
        """
        Detiene todos los patches iniciados.
        """
        patch.stopall()

    def test_iniciar(self):
        """
        Prueba el flujo básico de la función iniciar para asegurar que se invocan
        las funciones de sistema y dependencias correctamente.
        """
        iniciar()

        self.mock_os_system.assert_called_once_with("cls" if os.name == "nt" else "clear")
        expected_calls = [
            "Iniciando instalador...",
            f"Versión de Python: {sys.version}",
            "Intérpretes de Python encontrados:",
            "[0] /usr/bin/python3"
        ]
        for call in expected_calls:
            self.mock_print.assert_any_call(call)

        self.mock_update_pip.assert_called_once()
        self.mock_install_missing_dependencies.assert_called_once_with(
            'requirements.txt'
        )

    def test_iniciar_no_requirements(self):
        """
        Verifica que se maneje correctamente la ausencia del archivo requirements.txt.
        """
        self.mock_path_exists.return_value = False

        iniciar()

        self.mock_print.assert_any_call(
            "El archivo requirements.txt no fue encontrado. No se pueden verificar "
            "las dependencias."
        )

if __name__ == '__main__':
    unittest.main()
