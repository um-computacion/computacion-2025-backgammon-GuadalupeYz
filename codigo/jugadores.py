from typing import List
from codigo.fichas import Ficha

class Jugador:  # representa a un jugador de Backgammon
    def __init__(self, nombre: str, color: str) -> None:
        self._nombre: str = nombre
        self._color: str = color   # blanco o negro
        self._fichas: List[Ficha] = []  # lista de objetos Ficha

    def obtener_nombre(self) -> str:
        return self._nombre

    def obtener_color(self) -> str:
        return self._color

    def agregar_ficha(self, ficha: Ficha) -> None:
        self._fichas.append(ficha)

    def cantidad_fichas(self) -> int:
        return len(self._fichas)

    def obtener_fichas(self) -> List[Ficha]:
        return self._fichas
