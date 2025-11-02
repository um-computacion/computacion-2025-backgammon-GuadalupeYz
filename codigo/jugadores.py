"""Módulo que define la clase Jugador para el juego Backgammon."""

from typing import List
from codigo.fichas import Ficha
from codigo.excepciones import FichaInvalidaException


class Jugador:
    """Representa a un jugador del juego con su color y sus fichas."""

    def __init__(self, nombre: str, color: str) -> None:
        """Inicializa un jugador con nombre, color y lista vacía de fichas."""
        self.__nombre: str = nombre
        self.__color: str = color  # blanco o negro
        self.__fichas: List[Ficha] = []

    def get_nombre(self) -> str:
        """Devuelve el nombre del jugador."""
        return self.__nombre

    def set_nombre(self, nuevo_nombre: str) -> None:
        """Permite cambiar el nombre del jugador."""
        self.__nombre = nuevo_nombre

    def get_color(self) -> str:
        """Devuelve el color asignado al jugador."""
        return self.__color

    def set_color(self, nuevo_color: str) -> None:
        """Permite cambiar el color del jugador."""
        self.__color = nuevo_color

    def get_fichas(self) -> List[Ficha]:
        """Devuelve la lista de fichas que tiene el jugador."""
        return self.__fichas

    def set_fichas(self, fichas: List[Ficha]) -> None:
        """Permite asignar manualmente las fichas del jugador."""
        self.__fichas = fichas

    def agregar_ficha(self, ficha: Ficha) -> None:
        """Agrega una ficha al jugador si coincide el color."""
        if ficha.get_color() != self.__color:
            raise FichaInvalidaException("La ficha no coincide con el color del jugador")
        self.__fichas.append(ficha)

    def eliminar_ficha(self, ficha: Ficha) -> None:
        """Elimina la ficha indicada si existe en la lista.
        Si no la encuentra por identidad, elimina una del mismo color.
        """
        try:
            self.__fichas.remove(ficha)
        except ValueError as exc:
            # Buscar una ficha del mismo color y eliminarla
            for f in list(self.__fichas):
                if f.get_color() == ficha.get_color():
                    self.__fichas.remove(f)
                    break
            else:
                raise ValueError("La ficha no pertenece a este jugador") from exc

    def cantidad_fichas(self) -> int:
        """Devuelve cuántas fichas tiene actualmente el jugador."""
        return len(self.__fichas)
