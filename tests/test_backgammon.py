import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador

class TestBackgammonGame(unittest.TestCase):

    def test_iniciar_sin_jugadores_lanza_error(self):
        juego = BackgammonGame()
        with self.assertRaises(ValueError):
            juego.iniciar_juego()            #para que no pase vacio

    def test_agregar_jugadores_y_iniciar(self):   
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")

        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)

        try:                                #pruebo q funcione bien y no lance el error
            juego.iniciar_juego()
        except ValueError:
            self.fail("iniciar_juego lanzo error mal")

    def test_no_pueden_haber_mas_de_dos_jugadores(self):  #y aca pruebo q funcione error
        juego = BackgammonGame()
        juego.agregar_jugador(Jugador("Guada", "blanco"))
        juego.agregar_jugador(Jugador("Lupita", "negro"))
        with self.assertRaises(ValueError):
            juego.agregar_jugador(Jugador("Extra", "rojo")) 

if __name__ == "__main__":
    unittest.main()
