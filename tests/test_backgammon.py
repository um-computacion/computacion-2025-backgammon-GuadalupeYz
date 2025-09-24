import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException

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

    def test_setup_inicial_asigna_fichas(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        self.assertEqual(jugador1.cantidad_fichas(), 15)
        self.assertEqual(jugador2.cantidad_fichas(), 15)
        tablero = juego.get_tablero().get_points()
        self.assertEqual(len(tablero[0]), 15)
        self.assertEqual(len(tablero[23]), 15)

    def test_tirar_dados(self):
        juego = BackgammonGame()
        resultado = juego.tirar_dados()
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)
        for valor in resultado:
            self.assertGreaterEqual(valor, 1)
            self.assertLessEqual(valor, 6)

    def test_mover_ficha_valido(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        tablero = juego.get_tablero().get_points()
        ficha = tablero[0][-1]

        juego.mover_ficha(jugador1, 0, 5)

        self.assertEqual(len(tablero[0]), 14)  # una ficha menos en origen
        self.assertEqual(len(tablero[5]), 1)   # una ficha en destino

    def test_mover_ficha_origen_vacio_lanza_excepcion(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 10, 15)

    def test_mover_ficha_de_otro_jugador_lanza_excepcion(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        with self.assertRaises(FichaInvalidaException):
            juego.mover_ficha(jugador1, 23, 5)

    def test_turno_inicia_en_jugador1(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        self.assertEqual(juego.get_turno(), jugador1)

    def test_cambiar_turno_pasa_a_jugador2(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.cambiar_turno()
        self.assertEqual(juego.get_turno(), jugador2)

    def test_cambiar_turno_varias_veces(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.cambiar_turno()
        self.assertEqual(juego.get_turno(), jugador2)
        juego.cambiar_turno()
        self.assertEqual(juego.get_turno(), jugador1)

if __name__ == "__main__":
    unittest.main()

