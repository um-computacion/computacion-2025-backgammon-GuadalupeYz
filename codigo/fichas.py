"""Módulo que define la clase Ficha usada en el juego Backgammon."""

class Ficha:
    """Representa una ficha del juego con su color (blanco o negro)."""

    def __init__(self, color: str) -> None:
        """Crea una ficha con el color indicado (blanco o negro)."""
        self.__color____: str = color  # blanco o negro

    def get_color(self) -> str:
        """Devuelve el color actual de la ficha."""
        return self.__color____

    def set_color(self, nuevo_color: str) -> None:
        """Cambia el color de la ficha."""
        self.__color____ = nuevo_color
