
Modelo utilizado
ChatGPT (GPT-4, versión Octubre 2025)

Prompt 1: test de movimiento válido
Mensaje:
Quiero hacer un test para por ej asegurarme de que el jugador puede mover una ficha blanca  
desde el punto 7 al punto 6 cuando el dado tiene valor 1.  ¿Cómo lo hago?

Respuesta:
import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.fichas import Ficha

class TestMovimientoValido(unittest.TestCase):
    def test_movimiento_valido(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()
        juego._BackgammonGame__dados_disponibles = [1]
        puntos = juego.get_tablero().get_points()
        ficha = puntos[7][-1]
        juego.mover_ficha(j1, 7, 6)
        self.assertNotIn(ficha, puntos[7])

Prompt 2: test de victoria

Mensaje:
Necesito un test que verifique que cuando un jugador saca todas sus fichas, para ver si
el método finalizar_jugada() devuelve al ganado digamos, ayudame. 

Respuesta:

def test_bearoff_y_victoria(self):
    juego = BackgammonGame()
    j1 = Jugador("Guada", "blanco")
    j2 = Jugador("Bruno", "negro")
    juego.agregar_jugador(j1)
    juego.agregar_jugador(j2)
    juego._BackgammonGame__fichas_fuera = {"blanco": 15, "negro": 0}
    ganador = juego.finalizar_jugada()
    self.assertEqual(ganador.get_color(), "blanco")

Prompt 3: test de los dados

Mensaje:
Quiero probar que el método roll() de Dados devuelve dos valores entre 1 y 6,
y que tamb si son iguales genera 4 movimientos.

Respuesta:

import unittest
from codigo.dados import Dados

class TestDados(unittest.TestCase):
    def test_tirada_y_dobles(self):
        dados = Dados()
        dados._Dados__valores = (4, 4)
        movs = dados.movimientos_disponibles()
        self.assertEqual(len(movs), 4)
        self.assertTrue(all(d == 4 for d in movs))


Prompt 4: test de CLI que abandona partida

Mensaje:
Quiero hacer un test que simule que el usuario elige abandonar la partida en la CLI,
para comprobar que se limpia el estado del juego.¿Cómo puedo hacerlo con mock de input?

Respuesta:

from unittest.mock import patch

@patch("builtins.input", side_effect=["s"])
def test_abandonar_partida(self, mock_input):
    cli = CLI()
    cli._CLI__partida_activa = True
    cli._CLI__juego = BackgammonGame()
    cli.abandonar_partida()
    self.assertFalse(cli._CLI__partida_activa)
