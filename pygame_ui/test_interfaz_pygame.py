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


class TestInterfazPygameVictoria(unittest.TestCase):
    def setUp(self):
        pygame.display.init()
        self.juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        self.juego.agregar_jugador(j1)
        self.juego.agregar_jugador(j2)
        self.juego.setup_inicial()
        self.interfaz = InterfazPygame(self.juego)

    def tearDown(self):
        pygame.display.quit()

    def test_mostrar_victoria_no_lanza_errores(self): 
        #Verifica que mostrar_victoria se pueda ejecutar sin errores
        try:
            self.interfaz.mostrar_victoria()
        except Exception as e:
            self.fail(f"mostrar_victoria lanzó una excepción: {e}")

    def test_manejar_click_finaliza_partida_si_hay_ganador(self):
        #Simula que el juego tiene ganador y verifica que la interfaz lo marque
        # Forzamos un ganador
        self.juego.get_ganador = lambda: self.juego.get_jugadores()[0]

        # Simula clic válido
        self.interfaz.hitmap = {0: pygame.Rect(0, 0, 100, 100)}
        self.interfaz.manejar_click((10, 10))

        self.assertTrue(self.interfaz.juego_terminado)

    def test_no_error_al_dibujar_tablero_con_partida_terminada(self):
        #Dibuja tablero luego de terminar partida (debe mostrar mensaje sin errores)
        self.interfaz.juego_terminado = True
        try:
            self.interfaz.dibujar_tablero()
        except Exception as e:
            self.fail(f"dibujar_tablero falló con juego terminado: {e}")

def test_instancia_inicial(self):
    """La interfaz se crea correctamente"""
    self.assertIsInstance(self.interfaz, InterfazPygame)
    self.assertFalse(self.interfaz.juego_terminado)

def test_victoria_muestra_mensaje(self):
    """Simula que el juego tiene un ganador y muestra el mensaje"""
    class DummyJugador:
        def __init__(self):
            self.nombre = "Ganador"
        def get_nombre(self):
            return self.nombre

    # Simulamos un ganador forzado
    self.interfaz.juego.get_ganador = lambda: DummyJugador()
    self.interfaz.juego_terminado = True

    try:
        self.interfaz.mostrar_victoria()
    except Exception as e:
        self.fail(f"mostrar_victoria lanzó una excepción: {e}")

def test_manejar_click_bloquea_despues_de_victoria(self):
    """No debe permitir más clicks una vez terminado el juego"""
    self.interfaz.juego_terminado = True
    before = self.interfaz.punto_seleccionado
    self.interfaz.manejar_click((100, 100))  # simulamos click
    after = self.interfaz.punto_seleccionado
    self.assertEqual(before, after, "El click no debe modificar el estado si el juego terminó")


if __name__ == "__main__":
    unittest.main()
