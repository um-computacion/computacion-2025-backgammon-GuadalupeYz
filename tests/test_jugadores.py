import unittest
from codigo.jugadores import Jugador
from codigo.fichas import Ficha
from codigo.excepciones import FichaInvalidaException

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

    def test_agregar_ficha_valida(self):
        jugador = Jugador("Lupita", "negro")
        ficha = Ficha("negro")
        jugador.agregar_ficha(ficha)
        self.assertEqual(jugador.cantidad_fichas(), 1)
        self.assertEqual(jugador.get_fichas(), [ficha])

    def test_agregar_ficha_invalida(self):
        jugador = Jugador("Guada", "blanco")
        ficha = Ficha("negro")
        with self.assertRaises(FichaInvalidaException):
            jugador.agregar_ficha(ficha)

    def test_set_fichas(self):
        jugador = Jugador("Guada", "blanco")
        ficha1 = Ficha("blanco")
        ficha2 = Ficha("blanco")
        jugador.set_fichas([ficha1, ficha2])
        self.assertEqual(jugador.get_fichas(), [ficha1, ficha2])
        self.assertEqual(jugador.cantidad_fichas(), 2)

    def test_eliminar_ficha(self):
        jugador = Jugador("Lupita", "negro")
        ficha1 = Ficha("negro")
        ficha2 = Ficha("negro")
        jugador.set_fichas([ficha1, ficha2])
        jugador.eliminar_ficha(ficha1)
        self.assertEqual(jugador.get_fichas(), [ficha2])
        self.assertEqual(jugador.cantidad_fichas(), 1)

    def test_eliminar_ficha_inexistente(self):
        jugador = Jugador("Guada", "blanco")
        ficha = Ficha("blanco")
        with self.assertRaises(ValueError):
            jugador.eliminar_ficha(ficha)

if __name__ == "__main__":
    unittest.main()
