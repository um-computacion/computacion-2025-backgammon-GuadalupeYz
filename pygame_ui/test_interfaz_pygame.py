import unittest
import pygame
from interfaz_pygame import InterfazPygame
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador

class TestInterfazPygame(unittest.TestCase):
    def setUp(self):
        pygame.display.init()
        juego = BackgammonGame()
        jugador1 = Jugador("Alice", "blanco")
        jugador2 = Jugador("Bob", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()
        self.interfaz = InterfazPygame(juego)

    def test_instancia_inicial(self):
        self.assertIsNotNone(self.interfaz)
        self.assertIsInstance(self.interfaz, InterfazPygame)

    def test_metodos_basicos_existen(self):
        self.assertTrue(hasattr(self.interfaz, "dibujar_tablero"))
        self.assertTrue(hasattr(self.interfaz, "dibujar_fichas"))
        self.assertTrue(hasattr(self.interfaz, "manejar_click"))

if __name__ == "__main__":
    unittest.main()
