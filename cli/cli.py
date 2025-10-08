from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador

class CLI:
    def __init__(self) -> None:
        self.__opcion: str = ""
        self.__juego: BackgammonGame | None = None

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
           self.iniciar_partida() 
        elif self.get_opcion() == "2":
            print("Saliendo del juego...")
        else:
            print("Opción inválida")

def iniciar_partida(self) -> None: 
       self.__juego = BackgammonGame()

       print("Cargando jugadores...")
       nombre1 = input("Nombre del jugador 1 (blanco): ")
       nombre2 = input("Nombre del jugador 2 (negro): ")

       jugador1 = Jugador(nombre1, "blanco")
       jugador2 = Jugador(nombre2, "negro")

       self.__juego.agregar_jugador(jugador1)
       self.__juego.agregar_jugador(jugador2)
       self.__juego.iniciar_juego()
       self.__juego.setup_inicial()

       print(f"Partida iniciada entre {nombre1} y {nombre2}. ¡A jugar!")

if __name__ == "__main__":
    cli = CLI()
    cli.start()
