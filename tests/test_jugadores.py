
import unittest
from codigo.jugadores import Jugador

class TestPlayer(unittest.TestCase):

    def test_crear_jugador(self):
        jugador = Jugador("Guada", "blanco")
        self.assertEqual(jugador.obtener_nombre(), "Guada")
        self.assertEqual(jugador.obtener_color(), "blanco")

    def test_agregar_ficha(self):
        jugador = Jugador("Lupita", "negro")
        jugador.agregar_ficha("O")
        self.assertEqual(jugador.cantidad_fichas(), 1)
        jugador.agregar_ficha("O")
        self.assertEqual(jugador.cantidad_fichas(), 2)

    def test_lista_fichas_inicia_vacia(self):
        jugador = Jugador("Guada", "blanco")
        self.assertEqual(jugador.cantidad_fichas(), 0)

if __name__ == "__main__":
    unittest.main()
