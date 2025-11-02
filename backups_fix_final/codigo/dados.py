"""Módulo que maneja la lógica de los dados del juego Backgammon."""

import random
from typing import Tuple

class Dados:
    """Tira y guarda el resultado de los dados del juego."""

    def __init__(self) -> None:
        """Inicializa los dados con la última tirada en (0, 0)."""
        self.__ultimo__: Tuple[int, int] = (0, 0)

    def roll(self) -> Tuple[int, int]:
        """Lanza los dos dados y guarda el resultado."""
        # lanza los dos dados y devuelve el resultado
        # guarda el último resultado (en self.__ultimo__)
        self.__ultimo__ = (random.randint(1, 6), random.randint(1, 6))
        return self.__ultimo__

    def get_ultimo(self) -> Tuple[int, int]:
        """Devuelve la última tirada registrada."""
        # devuelve la última tirada registrada
        return self.__ultimo__

    def set_ultimo(self, valores: Tuple[int, int]) -> None:
        """Permite setear manualmente la última tirada (por ejemplo en tests)."""
        # permite modificar manualmente la última tirada (ej: para tests)
        self.__ultimo__ = valores
