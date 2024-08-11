# src/models/user_input_handler.py
import os

class UserInputHandler:
    """
    Clase para manejar la entrada del usuario.
    """

    def wait_for_restart(self):
        input("Presione Enter para Reiniciar:\n")
        os.system('cls' if os.name == 'nt' else 'clear')