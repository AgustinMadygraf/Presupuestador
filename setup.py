import subprocess
import sys

def check_dependencies():
    dependencies = ["subprocess", "os", "pathlib", "winshell", "win32com.client", "pywintypes"]
    missing_dependencies = []
    for dependency in dependencies:
        try:
            __import__(dependency)
        except ImportError:
            missing_dependencies.append(dependency)

    if missing_dependencies:
        print(f"Las siguientes dependencias están faltantes: {', '.join(missing_dependencies)}")
        print("Intentando instalar dependencias faltantes...")
        for dep in missing_dependencies:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
                print(f"{dep} instalado correctamente.")
            except subprocess.CalledProcessError as e:
                print(f"No se pudo instalar {dep}. Error: {e}")
    else:
        print("Todas las dependencias están instaladas.")

check_dependencies()


from src.installer_utils import main
main()

