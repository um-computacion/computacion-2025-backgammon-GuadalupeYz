 
import unittest
from unittest.mock import patch
import io
from CLI import cli

class TestCLI(unittest.TestCase):

    @patch("sys.stdout", new_callable=io.StringIO)
    def test_start_muestra_menu(self, mock_stdout):
        cli.start()
        salida = mock_stdout.getvalue()
        self.assertIn("¡¡¡Bienvenido al juego Backgammon!!!", salida)
        self.assertIn("Menu principal:", salida)
        self.assertIn("1. Inicio partida", salida)
        self.assertIn("2. Salir", salida)

if __name__ == "__main__":
    unittest.main()

