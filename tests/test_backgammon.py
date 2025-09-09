import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador

class TestBackgammonGame(unittest.TestCase):

    def test_iniciar_sin_jugadores_lanza_error(self):
        juego = BackgammonGame()
        with self.assertRaises(ValueError):
            juego.iniciar_juego()

    def test_agregar_jugadores_y_iniciar(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")

        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)

        self.assertEqual(len(juego.get_jugadores()), 2)

        try:
            juego.iniciar_juego()
        except ValueError:
            self.fail("iniciar_juego lanzó ValueError incorrectamente")

    def test_no_pueden_haber_mas_de_dos_jugadores(self):
        juego = BackgammonGame()
        juego.agregar_jugador(Jugador("Guada", "blanco"))
        juego.agregar_jugador(Jugador("Lupita", "negro"))

        with self.assertRaises(ValueError):
            juego.agregar_jugador(Jugador("Extra", "rojo"))

    def test_setup_inicial_asigna_fichas_a_jugadores_y_tablero(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)

        juego.setup_inicial()

        #cada jugador debe tener 15 fichas
        self.assertEqual(jugador1.cantidad_fichas(), 15)
        self.assertEqual(jugador2.cantidad_fichas(), 15)

        #el tablero debe tener fichas en posiciones 0 y 23
        tablero = juego.get_tablero().get_points()
        self.assertEqual(len(tablero[0]), 15)
        self.assertEqual(len(tablero[23]), 15)

if __name__ == "__main__":
    unittest.main()

