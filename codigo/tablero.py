from typing import List

class Tablero:
    
    #Representa el tablero de Backgammon con 24 puntos

    def __init__(self) -> None:
        #lista de 24 puntos,inicialmente vacio
        self.__points__: List[List[str]] = [[] for _ in range(24)]

    pass

