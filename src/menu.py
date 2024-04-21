from colorama import Fore, init

def main_menu():
    print("\nPresupuestador de Proyectos")
    print("1. Confeccionar un nuevo presupuesto")
    print("2. Generar archivo PDF del presupuesto")
    print("0. Salir\n")
    choice = input(Fore.BLUE + "Elija una opción: ") or "2"
    print("")
    return choice