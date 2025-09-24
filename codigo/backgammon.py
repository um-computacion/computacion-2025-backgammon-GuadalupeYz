from typing import List
from codigo.jugadores import Jugador
from codigo.tablero import Tablero
from codigo.dados import Dados
from codigo.fichas import Ficha
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException
from typing import Tuple

class BackgammonGame:
    def __init__(self) -> None:
        self.__jugadores: List[Jugador] = []
        self.__tablero: Tablero = Tablero()
        self.__dados: Dados = Dados()

    def get_jugadores(self) -> List[Jugador]:
        return self.__jugadores

    def get_tablero(self) -> Tablero:
        return self.__tablero

    def get_dados(self) -> Dados:
        return self.__dados

    def set_tablero(self, tablero: Tablero) -> None:
        self.__tablero = tablero

    def set_dados(self, dados: Dados) -> None:
        self.__dados = dados

    def agregar_jugador(self, jugador: Jugador) -> None:
        if len(self.__jugadores) < 2:
            self.__jugadores.append(jugador)
        else:
            raise ValueError("Ya hay 2 jugadores en la partida") 

    def iniciar_juego(self) -> None:
        if len(self.__jugadores) != 2:
            raise ValueError("Se necesitan 2 jugadores para iniciar el juego")
        print("¡¡Comienza la partida de Backgammon!!")

    def setup_inicial(self) -> None:
        #cada jugador recibe 15 fichas y se colocan todas en el punto 0 (blanco) 
        # y 23 (negro) del tablero
        if len(self.__jugadores) != 2:
            raise ValueError("Se necesitan 2 jugadores para preparar el tablero inicial")

        jugador1, jugador2 = self.__jugadores

        # jugador1 (blanco): punto 0        #primero lo voy a plantear asi como 0 el primero 
        #del blanco y 23 el primero del negro, ya despues reparto bien las fichas 
        for _ in range(15):
            ficha = Ficha(jugador1.get_color())
            jugador1.agregar_ficha(ficha)
            self.__tablero.colocar_ficha(0, ficha)

        #jugador2 (negro): punto 23
        for _ in range(15):
            ficha = Ficha(jugador2.get_color())
            jugador2.agregar_ficha(ficha)
            self.__tablero.colocar_ficha(23, ficha)

    def tirar_dados(self) -> Tuple[int, int]:
        self.__ultima_tirada = self.__dados.roll()
        return self.__ultima_tirada

    def mover_ficha(self, jugador: Jugador, origen: int, destino: int) -> None:
        puntos = self.__tablero.get_points()

        #me fijo que el origen sea valido para el juego
        if not puntos[origen]:
            raise MovimientoInvalidoException("No hay fichas en el punto de origen")

        ficha = puntos[origen][-1]

        #aca valido que la ficha sea del jugador
        if ficha.get_color() != jugador.get_color():
            raise FichaInvalidaException("La ficha no pertenece al jugador")

        #sacamos la ficha del origen y la ponemos en el destino
        puntos[origen].pop()
        self.__tablero.colocar_ficha(destino, ficha)

    def get_turno(self) -> Jugador:
        if not self.__jugadores:
            raise ValueError("No hay jugadores en la partida")
        return self.__jugadores[self.__turno_actual]

    def cambiar_turno(self) -> None:
        if len(self.__jugadores) != 2:
            raise ValueError("Se necesitan 2 jugadores para cambiar turno")
        self.__turno_actual = 1 - self.__turno_actual

