import random
from typing import Tuple

class Dados:
    def __init__(self) -> None:
        self.__ultimo: Tuple[int, int] = (0, 0)

    def roll(self) -> Tuple[int, int]:
        # lanza los dos dados y devuelve el resultado.
        # guarda el ultimo resultado (en self.__ultimo).
        self.__ultimo = (random.randint(1, 6), random.randint(1, 6))
        return self.__ultimo

    def get_ultimo(self) -> Tuple[int, int]:
        # devuelve la ultima tirada registrada
        return self.__ultimo

    def set_ultimo(self, valores: Tuple[int, int]) -> None:
        # permite modificar manualmente la ultima tirada (ej: para tests)
        self.__ultimo = valores

    
        