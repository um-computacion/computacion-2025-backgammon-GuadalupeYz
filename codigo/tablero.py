from typing import List

class Tablero:
    
    #Representa el tablero de Backgammon con 24 puntos.
    #cada punto vendria siendo una lista donde se colocan las fichas.

    def __init__(self) -> None:
        # lista de 24 puntos, inicialmente vacios
        self._points: List[List[str]] = [[] for _ in range(24)]

    def colocar_ficha(self, punto: int, ficha: str) -> None:
        
        #coloca una ficha en un punto del tablero.
        #punto: indice entre 0 y 23
        #ficha: simbolo de la ficha, por ejemplo "X" o "O"
        
        if not 0 <= punto < 24:
            raise ValueError("El punto debe estar entre 0 y 23.")
        self.__points__[punto].append(ficha)

    def obtener_tablero(self) -> List[List[str]]:
        
        return self._points    #devuelve situacion actual del tablero.
        
        


  
