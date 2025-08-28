
import random
from typing import Tuple

class Dados:
    
    #representa los dos dados del juego.

    def __init__(self) -> None:
        self.__ultimo__: Tuple[int, int] = (0, 0)

    def roll(self) -> Tuple[int, int]:
    
        #lanza los dos dados y devuelve el resultado.
        #guarda el ultimo resultado (en self.__ultimo__).
        
        self.__ultimo__ = (random.randint(1, 6), random.randint(1, 6))
        return self.__ultimo__

    def ultimo(self) -> Tuple[int, int]:
    
        #devuelve la ultima tirada dados registrada.
    
        return self.__ultimo__
