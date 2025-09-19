class CLI:
    def __init__(self) -> None:
        self.__opcion: str = ""

    def set_opcion(self, opcion: str) -> None:
        self.__opcion = opcion

    def get_opcion(self) -> str:
        return self.__opcion

    def start(self) -> None:
        print("¡¡¡Bienvenido al juego Backgammon!!!")
        print("Menu principal:")
        print("1. Inicio partida")
        print("2. Salir")

        opcion = input("Elegi una opcion: ")
        self.set_opcion(opcion)

        if self.get_opcion() == "1":
            print("Iniciando partida...")
        elif self.get_opcion() == "2":
            print("Saliendo del juego...")
        else:
            print("Opcion invalida")

if __name__ == "__main__":
    cli = CLI()
    cli.start()
