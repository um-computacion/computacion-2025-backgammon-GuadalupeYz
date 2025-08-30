import unittest
from codigo.jugadores import Jugador
from codigo.fichas import Ficha

class TestJugador(unittest.TestCase):

    def test_crear_jugador(self):
        jugador = Jugador("Guada", "blanco")
        self.assertEqual(jugador.obtener_nombre(), "Guada")
        self.assertEqual(jugador.obtener_color(), "blanco")

    def test_agregar_ficha(self):
        jugador = Jugador("Lupita", "negro")
        ficha1 = Ficha("negro")
        ficha2 = Ficha("negro")
        jugador.agregar_ficha(ficha1)
        self.assertEqual(jugador.cantidad_fichas(), 1)
        jugador.agregar_ficha(ficha2)
        self.assertEqual(jugador.cantidad_fichas(), 2)

    def test_lista_fichas_inicia_vacia(self):
        jugador = Jugador("Guada", "blanco")
        self.assertEqual(jugador.cantidad_fichas(), 0)

    def test_obtener_fichas(self):
        jugador = Jugador("Guada", "blanco")
        ficha1 = Ficha("blanco")
        ficha2 = Ficha("blanco")
        jugador.agregar_ficha(ficha1)
        jugador.agregar_ficha(ficha2)
        self.assertEqual(jugador.obtener_fichas(), [ficha1, ficha2])

if __name__ == "__main__":
    unittest.main()
