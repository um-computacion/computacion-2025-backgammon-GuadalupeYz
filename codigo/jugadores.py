from typing import List
from codigo.fichas import Ficha
from codigo.excepciones import FichaInvalidaException


class Jugador:  # representa a un jugador de Backgammon
    def __init__(self, nombre: str, color: str) -> None:
        self.__nombre: str = nombre
        self.__color: str = color  # blanco o negro
        self.__fichas: List[Ficha] = []

    # getters y setters
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

    #logica de fichas
    def agregar_ficha(self, ficha: Ficha) -> None:
        if ficha.get_color() != self.__color:
            raise FichaInvalidaException("La ficha no coincide con el color del jugador")
        self.__fichas.append(ficha)

    def eliminar_ficha(self, ficha: Ficha) -> None:
        if ficha in self.__fichas:
            self.__fichas.remove(ficha)
        else:
            raise ValueError("La ficha no pertenece a este jugador")

    def cantidad_fichas(self) -> int:
        return len(self.__fichas)
