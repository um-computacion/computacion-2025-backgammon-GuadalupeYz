from typing import List
from codigo.jugadores import Jugador
from codigo.tablero import Tablero
from codigo.dados import Dados

class BackgammonGame:

    def __init__(self) -> None:
        self._jugadores: List[Jugador] = []  
        self._tablero: Tablero = Tablero()  #cada partida tiene su tablero y dados
        self._dados: Dados = Dados()

    def agregar_jugador(self, jugador: Jugador) -> None:
        if len(self._jugadores) < 2:
            self._jugadores.append(jugador)   # max.2 (xq backgammon es de 2 jugadores)
        else:
            raise ValueError("Ya hay 2 jugadores en la partida") 

    def iniciar_juego(self) -> None:
        if len(self._jugadores) != 2:  #entonces si hay mas debe lanzar error
            raise ValueError("Se necesitan 2 jugadores para iniciar el juego")
        print("¡¡Comienza la partida de Backgammon!!")
  

