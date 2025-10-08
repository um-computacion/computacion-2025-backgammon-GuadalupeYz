import unittest
from cli.cli import CLI
from codigo.backgammon import BackgammonGame
from unittest.mock import patch

class TestCLI(unittest.TestCase):
    def test_set_get_opcion(self):
        cli = CLI()
        cli.set_opcion("1")
        self.assertEqual(cli.get_opcion(), "1")

    @patch("builtins.input", side_effect=["1", "Guada", "Lupita"]) 
    def test_iniciar_partida(self, mock_input):
       cli = CLI()
       cli.start()  #la partida se inicializa
       self.assertIsNotNone(cli._CLI__juego)
       self.assertIsInstance(cli._CLI__juego, BackgammonGame)
       self.assertEqual(len(cli._CLI__juego.get_jugadores()), 2)  

if __name__ == "__main__":
    unittest.main()
               