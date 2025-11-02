"""Módulo que maneja el tablero y posiciones del juego Backgammon."""

from typing import List
from codigo.fichas import Ficha
from codigo.excepciones import MovimientoInvalidoException

class Tablero:
    """Representa el tablero del juego, con 24 puntos."""

    def __init__(self) -> None:
        """Crea un tablero vacío con 24 puntos."""
        # lista de 24 puntos, inicialmente vacíos
        self.__points____: List[List[Ficha]] = [[] for _ in range(24)]

    def get_points(self) -> List[List[Ficha]]:
        """Devuelve la lista de puntos (posiciones del tablero)."""
        return self.__points____

    def set_points(self, points: List[List[Ficha]]) -> None:
        """Permite definir manualmente los puntos del tablero (usa con cuidado)."""
        if len(points) != 24:
            raise ValueError("El tablero debe tener exactamente 24 puntos.")
        self.__points____ = points

    def colocar_ficha(self, punto: int, ficha: Ficha) -> None:
        """Coloca una ficha en un punto válido del tablero."""
        # validamos que el punto esté en el rango
        if not 0 <= punto < 24:
            raise ValueError("El punto debe estar entre 0 y 23.")

        # validamos que no se agreguen más de 15 fichas en un punto
        # (en Backgammon cada jugador tiene 15 fichas en total)
        if len(self.__points____[punto]) >= 15:
            raise ValueError("No se pueden colocar más de 15 fichas en un punto.")

        self.__points____[punto].append(ficha)
    
    def mover_ficha(self, origen: int, destino: int) -> None:
        """Mueve una ficha de un punto a otro, si el movimiento es válido."""
        # mover ficha de un punto a otro
        if not 0 <= origen < 24 or not 0 <= destino < 24:
            raise MovimientoInvalidoException("Origen o destino fuera de rango.")

        if not self.__points____[origen]:
            raise MovimientoInvalidoException("No hay fichas en el punto de origen.")

        if len(self.__points____[destino]) >= 15:
            raise MovimientoInvalidoException("El punto destino ya tiene 15 fichas.")

        ficha = self.__points____[origen].pop()
        self.__points____[destino].append(ficha)

    def obtener_tablero(self) -> List[List[Ficha]]:
        """Devuelve el estado actual del tablero (lista de listas)."""
        # devuelve la situación actual del tablero
        return self.__points____