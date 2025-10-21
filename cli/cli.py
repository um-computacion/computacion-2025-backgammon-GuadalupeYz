from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException

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
        print("2. Ver historial de movimientos") 
        print("3. Salir")

        opcion = input("Elegi una opcion: ")
        self.set_opcion(opcion)

        if self.get_opcion() == "1":
            self.iniciar_partida()
        elif self.get_opcion() == "2":   
            self.mostrar_historial()
        elif self.get_opcion() == "3":
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

       self.jugar_turno()

    def jugar_turno(self) -> None:   
        if not self.__juego:
            print("No hay una partida activa.")
            return

        jugador_actual = self.__juego.get_turno()
        print(f"\nTurno de {jugador_actual.get_nombre()} ({jugador_actual.get_color()})")

        input("Presiona ENTER para tirar los dados...")
        dados = self.__juego.tirar_dados()
        print(f"Resultado del tiro: {dados[0]} y {dados[1]}")

        print("Ahora podes mover tus fichas con los valores obtenidos.")
        print("-------------------------------------------------------") #para separar msje

        self.loop_partida()   

    def loop_partida(self) -> None:   
        while True:
            jugador_actual = self.__juego.get_turno()
            print(f"\nTurno de {jugador_actual.get_nombre()} ({jugador_actual.get_color()})")
            input("Presiona ENTER para tirar los dados")

            dados = self.__juego.tirar_dados()
            print(f"Resultado del tiro: {dados[0]} y {dados[1]}")
            print("Ahora podes mover tus fichas segun los valores obtenidos.")
            print("-------------------------------------------------------")

            self.mostrar_tablero() #se muestra el tablero visual antes de mover

            while True:
                try:
                    origen = int(input("Elegí el punto de origen: "))
                    destino = int(input("Elegí el punto de destino: "))
                    self.__juego.mover_ficha(jugador_actual, origen, destino)
                    self.mostrar_tablero()
                    self.mostrar_historial_turno() 
                except (MovimientoInvalidoException, FichaInvalidaException, ValueError) as e:
                    print(f" Error: {e}")

                continuar = input("¿Queres mover otra ficha con el dado restante? (s/n): ")
                if continuar.lower() != "s":
                    break

            ganador = self.__juego.finalizar_jugada()
            if ganador:
                print(f"🎉 ¡{ganador.get_nombre()} ganó la partida! 🎉")
                print("La partida ha finalizado.")
                break


    def mostrar_tablero(self) -> None:   
        puntos = self.__juego.get_tablero().get_points()
        print("\n" + "=" * 70)
        print(" " * 24 + "TABLERO DE BACKGAMMON")
        print("=" * 70)

        # parte superior (puntos 12 a 23)
        print("\nZona superior:")
        fila_superior = ""
        for i in range(12, 24):
            if puntos[i]:
                color = puntos[i][-1].get_color()[0].upper()
                cantidad = len(puntos[i])
                fila_superior += f"{i:2d}[{color}{cantidad}] "
            else:
                fila_superior += f"{i:2d}[  ] "
        print(fila_superior)

        # parte inferior (puntos 11 a 0)
        print("\nZona inferior:")
        fila_inferior = ""
        for i in range(11, -1, -1):
            if puntos[i]:
                color = puntos[i][-1].get_color()[0].upper()
                cantidad = len(puntos[i])
                fila_inferior += f"{i:2d}[{color}{cantidad}] "
            else:
                fila_inferior += f"{i:2d}[  ] "
        print(fila_inferior)

        print("\n" + "=" * 70)

    def mostrar_historial_turno(self) -> None:   
        historial = self.__juego.get_historial()
        if historial:
            print("\nÚltimos movimientos:")
            for linea in historial[-3:]:  #muestra los ultimos 3
                print("-", linea)
        print("-------------------------------------------------------")

    def mostrar_historial(self) -> None:   
        if not self.__juego:
            print("Todavia no hay una partida iniciada.")
            return
        historial = self.__juego.get_historial()
        if not historial:
            print("No hay movimientos registrados aun.")
        else:
            print("\nHistorial completo de la partida:")
            for mov in historial:
                print("-", mov)
        print("-------------------------------------------------------")

if __name__ == "__main__":
    cli = CLI()
    cli.start()
