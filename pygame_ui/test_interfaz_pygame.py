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

    def tearDown(self):
        pygame.display.quit()

    def test_instancia_inicial(self):
        #La interfaz se crea correctamente
        self.assertIsNotNone(self.interfaz)
        self.assertIsInstance(self.interfaz, InterfazPygame)

    def test_metodos_basicos_existen(self):
        #Verifica que los métodos principales existen
        self.assertTrue(hasattr(self.interfaz, "dibujar_tablero"))
        self.assertTrue(hasattr(self.interfaz, "dibujar_fichas"))
        self.assertTrue(hasattr(self.interfaz, "manejar_click"))

    def test_dibujar_tablero_no_falla(self):
        #Ejecuta dibujar_tablero y verifica que no lance errores
        try:
            self.interfaz.dibujar_tablero()
        except Exception as e:
            self.fail(f"dibujar_tablero lanzó una excepción: {e}")

    def test_seleccionar_y_deseleccionar_punto(self):
        #Simula seleccionar y limpiar punto
        self.assertIsNone(self.interfaz.punto_seleccionado)
        self.interfaz.punto_seleccionado = 3
        self.assertEqual(self.interfaz.punto_seleccionado, 3)
        self.interfaz.punto_seleccionado = None
        self.assertIsNone(self.interfaz.punto_seleccionado)


if __name__ == "__main__":
    unittest.main()
