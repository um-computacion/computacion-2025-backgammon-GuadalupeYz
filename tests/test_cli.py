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

class TestCLI(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "Guada", "Lupita", ""])
    @patch("builtins.print")
    def test_jugar_turno_tira_dados(self, mock_print, mock_input):
        cli = CLI()
        cli.start()          
        # Verifica que se imprimio el resultado de los dados
        printed_texts = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Resultado del tiro", printed_texts)
        self.assertIn("Turno de", printed_texts)

class TestCLI(unittest.TestCase):

    def test_set_get_opcion(self):
        cli = CLI()
        cli.set_opcion("1")
        self.assertEqual(cli.get_opcion(), "1")

    #simula las entradas
    @patch("builtins.input", side_effect=["1", "Guada", "Lupita", "s"])
    def test_iniciar_partida_y_salir(self, mock_input):
        cli = CLI()
        try:
            cli.start()
        except Exception:
            self.fail("Error inesperado durante la partida")

    @patch("builtins.input", side_effect=["1", "Guada", "Lupita", "t", "0", "5", "s"])
    def test_movimiento_en_partida(self, mock_input):
        cli = CLI()
        try:
            cli.start()
        except Exception:
            self.fail("Error inesperado al mover ficha")

if __name__ == "__main__":
    unittest.main()

