# /setup.py
input("Presiona Enter para comenzar la instalación...")
import subprocess
import sys
import os
from pathlib import Path

class DependencyChecker:
    def __init__(self):
        self.dependencies = ["subprocess", "os", "pathlib", "winshell", "win32com.client", "pywintypes","colorlog"]

    def check_dependencies(self):
        missing_dependencies = self.get_missing_dependencies()
        if missing_dependencies:
            self.install_missing_dependencies(missing_dependencies)
        else:
            print("Todas las dependencias están instaladas.")

    def get_missing_dependencies(self):
        missing_dependencies = []
        for dependency in self.dependencies:
            try:
                __import__(dependency)
            except ImportError:
                missing_dependencies.append(dependency)
        return missing_dependencies

    def install_missing_dependencies(self, missing_dependencies):
        print(f"Las siguientes dependencias están faltantes: {', '.join(missing_dependencies)}")
        print("Intentando instalar dependencias faltantes...")
        for dep in missing_dependencies:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
                print(f"{dep} instalado correctamente.")
            except subprocess.CalledProcessError as e:
                print(f"No se pudo instalar {dep}. Error: {e}")

if __name__ == "__main__":
    checker = DependencyChecker()
    checker.check_dependencies()
    from src.installer_utils import ProjectInstaller
    installer = ProjectInstaller()
    installer.main()
