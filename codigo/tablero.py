
from typing import List
from codigo.fichas import Ficha

class Tablero:
    # Representa el tablero de Backgammon con 24 puntos

    def __init__(self) -> None:
        # Lista de 24 puntos, inicialmente vacios
        self.__points: List[List[Ficha]] = [[] for _ in range(24)]

    def get_points(self) -> List[List[Ficha]]:
        return self.__points

    def set_points(self, points: List[List[Ficha]]) -> None:
        if len(points) != 24:
            raise ValueError("El tablero debe tener exactamente 24 puntos.")
        self.__points = points

    def colocar_ficha(self, punto: int, ficha: Ficha) -> None:
        # validamos que el punto este en el rango
        if not 0 <= punto < 24:
            raise ValueError("El punto debe estar entre 0 y 23.")

        # validamos que no se agreguen mas de 15 fichas en un punto
        # (ej en Backgammon cada jugador tiene 15 fichas en total)

        if len(self.__points[punto]) >= 15:
            raise ValueError("No se pueden colocar mas de 15 fichas en un punto.")

        self.__points[punto].append(ficha)

    def obtener_tablero(self) -> List[List[Ficha]]:
        # devuelve la situacion actual del tablero
        return self.__points    