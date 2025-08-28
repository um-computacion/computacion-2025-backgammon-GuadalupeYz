#Interfaz de texto para jugar Backgammon

def start():
    print("¡¡¡Bienvenido al juego Backgammon!!!")
    print("Menu principal:")
    print("1. Inicio partida")
    print("2. Salir")

    opcion = input("Elegí una opción: ")
    if opcion == "1":
        print("Iniciando partida...")
        #aca luego llamo a backgammon
    elif opcion == "2":
        print("Saliendo del juego...")
    else:
        print("Opción inválida")

if __name__ == "__main__":
    start()

