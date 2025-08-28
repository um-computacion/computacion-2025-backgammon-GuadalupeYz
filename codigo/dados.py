
import random
from typing import Tuple

class Dados:
    
    #representa los dos dados del juego.

    def __init__(self) -> None:
        self._ultimo: Tuple[int, int] = (0, 0)

    def roll(self) -> Tuple[int, int]:
    
        #lanza los dos dados y devuelve el resultado.
        #guarda el ultimo resultado (en self.__ultimo__).
        
        self._ultimo = (random.randint(1, 6), random.randint(1, 6))
        return self._ultimo

    def get_ultimo(self) -> Tuple[int, int]:
        return self._ultimo
    
        #devuelve la ultima tirada dados registrada.
    
        