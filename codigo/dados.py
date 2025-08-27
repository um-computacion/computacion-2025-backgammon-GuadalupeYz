import random
from typing import Tuple

class Dados:
    def roll(self) -> Tuple[int, int]:
        #Lanza los dos dados y devuelve el resultado
        return random.randint(1, 6), random.randint(1, 6)
