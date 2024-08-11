"""
Este módulo maneja la interfaz de usuario para el Presupuestador de Proyectos.
"""

from colorama import Fore, init
from .user_input_handler import UserInputHandler

init(autoreset=True)

class UserInterface:
    """
    Clase para manejar la interacción con el usuario.
    """

    def __init__(self, logger):
        self.logger = logger
        self.primera_vez = True
        self.input_handler = UserInputHandler()

    def mostrar_bienvenida(self):
        """
        Muestra el mensaje de bienvenida al usuario.
        """
        if self.primera_vez:
            self.logger.debug("Mostrando mensaje de bienvenida por primera vez.")
            print(Fore.GREEN + "¡Bienvenido al Presupuestador de Proyectos!\n")
            self.primera_vez = False
        else:
            self.logger.debug("Reiniciando la aplicación por solicitud del usuario.")
            self.input_handler.wait_for_restart()

    def despedida(self):
        """
        Muestra el mensaje de despedida al usuario.
        """
        self.logger.debug("Mostrando mensaje de despedida.")
        print(Fore.GREEN + "¡Gracias por usar el Presupuestador de Proyectos!\n")