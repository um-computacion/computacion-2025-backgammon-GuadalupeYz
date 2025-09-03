from typing import List
from codigo.fichas import Ficha

class Jugador:  # representa a un jugador de Backgammon
    def __init__(self, nombre: str, color: str) -> None:
        self.__nombre: str = nombre
        self.__color: str = color   #blanco o negro
        self.__fichas: List[Ficha] = []

    def get_nombre(self) -> str:
        return self.__nombre

    def set_nombre(self, nuevo_nombre: str) -> None:
        self.__nombre = nuevo_nombre

    def get_color(self) -> str:
        return self.__color

    def set_color(self, nuevo_color: str) -> None:
        self.__color = nuevo_color

    def get_fichas(self) -> List[Ficha]:
        return self.__fichas

    def set_fichas(self, fichas: List[Ficha]) -> None:
        self.__fichas = fichas
 
    def agregar_ficha(self, ficha: Ficha) -> None:
        self.__fichas.append(ficha)                  

    def cantidad_fichas(self) -> int:
        return len(self.__fichas)
