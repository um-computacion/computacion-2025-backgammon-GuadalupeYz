from typing import List
from codigo.fichas import Ficha

class Tablero:
    #cada punto es una lista donde se colocan las fichas.

    def __init__(self) -> None:
        #lista de 24 puntos, inicialmente vacios
        self.__points: List[List[Ficha]] = [[] for _ in range(24)]

    def get_points(self) -> List[List[Ficha]]:
        return self.__points

    def set_points(self, nuevo_tablero: List[List[Ficha]]) -> None:
        if len(nuevo_tablero) != 24:
            raise ValueError("El tablero debe tener exactamente 24 puntos.")
        self.__points = nuevo_tablero

    def colocar_ficha(self, punto: int, ficha: Ficha) -> None:
        #coloca una ficha en un punto del tablero.
        if not 0 <= punto < 24:
            raise ValueError("El punto debe estar entre 0 y 23.")
        self.__points[punto].append(ficha)

    def obtener_tablero(self) -> List[List[Ficha]]:
        #Devuelve la situaciOn actual del tablero.
        return self.__points


  
