#Presupuestos/src/models/user_interface.py
import os
from colorama import Fore, init

init(autoreset=True)

class UserInterface:
    """
    Clase para manejar la interacción con el usuario.
    """

    def __init__(self, logger):
        self.logger = logger
        self.primera_vez = True

    def mostrar_bienvenida(self):
        """
        Muestra el mensaje de bienvenida al usuario.
        """
        if self.primera_vez:
            self.logger.debug("Mostrando mensaje de bienvenida por primera vez.")
            print(Fore.GREEN + "¡Bienvenido al Presupuestador de Proyectos!\n")  # Añadir un salto de línea al final
            self.primera_vez = False
        else:
            self.logger.debug("Reiniciando la aplicación por solicitud del usuario.")
            input("Presione Enter para Reiniciar:\n")
            os.system('cls' if os.name == 'nt' else 'clear')
