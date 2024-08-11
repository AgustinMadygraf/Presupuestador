# src/models/directory_manager.py
import os

class DirectoryManager:
    @staticmethod
    def prepare_output_directory():
        # Detecta el directorio base del proyecto de manera dinámica
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        output_dir = os.path.join(base_dir, 'Presupuestador', 'generated_pdfs')
        # Crea el directorio si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir