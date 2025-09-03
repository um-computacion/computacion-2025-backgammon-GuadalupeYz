import unittest
from codigo.jugadores import Jugador
from codigo.fichas import Ficha

class TestJugador(unittest.TestCase):

    def test_crear_jugador(self):
        jugador = Jugador("Guada", "blanco")
        self.assertEqual(jugador.get_nombre(), "Guada")
        self.assertEqual(jugador.get_color(), "blanco")
        self.assertEqual(jugador.cantidad_fichas(), 0)

    def test_setters(self):
        jugador = Jugador("Lupita", "negro")
        jugador.set_nombre("Ana")
        jugador.set_color("blanco")
        self.assertEqual(jugador.get_nombre(), "Ana")
        self.assertEqual(jugador.get_color(), "blanco")

    def test_agregar_ficha(self):
        jugador = Jugador("Lupita", "negro")
        ficha1 = Ficha("negro")
        ficha2 = Ficha("negro")
        jugador.agregar_ficha(ficha1)
        jugador.agregar_ficha(ficha2)
        self.assertEqual(jugador.cantidad_fichas(), 2)
        self.assertEqual(jugador.get_fichas(), [ficha1, ficha2])

    def test_set_fichas(self):
        jugador = Jugador("Guada", "blanco")
        ficha1 = Ficha("blanco")
        ficha2 = Ficha("blanco")
        jugador.set_fichas([ficha1, ficha2])
        self.assertEqual(jugador.get_fichas(), [ficha1, ficha2])
        self.assertEqual(jugador.cantidad_fichas(), 2)

if __name__ == "__main__":
    unittest.main()
