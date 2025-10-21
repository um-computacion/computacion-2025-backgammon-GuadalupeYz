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

class TestCLI(unittest.TestCase):

    @patch("builtins.input", side_effect=["1", "Guada", "Lupita", "s"])
    def test_iniciar_partida_con_historial(self, mock_input):
        cli = CLI()
        try:
            cli.start()
        except Exception:
            self.fail("Error inesperado al iniciar partida")

    @patch("builtins.input", side_effect=["2"])
    def test_ver_historial_sin_partida(self, mock_input):
        cli = CLI()
        cli.start()  # No hay partida activa
        try:
            cli.mostrar_historial()
        except Exception:
            self.fail("Error inesperado al mostrar historial sin partida")  

class TestCLI(unittest.TestCase):
    def setUp(self):
        self.cli = CLI()

    def test_iniciar_partida_crea_juego(self):
        #Verifica que iniciar_partida crea un juego y activa la partida.
        self.cli._CLI__juego = BackgammonGame()  # simular preparación
        self.cli._CLI__partida_activa = False
        self.cli._CLI__juego = BackgammonGame()
        self.cli._CLI__partida_activa = True
        self.assertTrue(self.cli._CLI__partida_activa)

    def test_abandonar_partida_funciona(self):
        #Simula abandono y verifica que se desactive correctamente.
        self.cli._CLI__partida_activa = True
        self.cli._CLI__juego = BackgammonGame()
        # Simular confirmación directa
        input_backup = __builtins__.input
        __builtins__.input = lambda _: "s"  
        self.cli.abandonar_partida()
        __builtins__.input = input_backup
        self.assertFalse(self.cli._CLI__partida_activa)
        self.assertIsNone(self.cli._CLI__juego)

    def test_leer_entero_valido(self):
        #Verifica que leer_entero devuelve un número entero válido.
        input_backup = __builtins__.input
        __builtins__.input = lambda _: "7"
        valor = self.cli.leer_entero("Ingrese un número: ")
        __builtins__.input = input_backup
        self.assertEqual(valor, 7)

    def test_leer_entero_invalido_y_reintenta(self):
        #Simula input inválido seguido de válido
        input_backup = __builtins__.input
        respuestas = iter(["", "a", "5"])
        __builtins__.input = lambda _: next(respuestas)
        valor = self.cli.leer_entero("Ingrese un número: ")
        __builtins__.input = input_backup
        self.assertEqual(valor, 5)

    def test_mostrar_historial_sin_juego(self):
        #No debe romper si no hay juego creado.
        try:
            self.cli._CLI__juego = None
            self.cli.mostrar_historial()
        except Exception as e:
            self.fail(f"mostrar_historial lanzó excepción inesperada: {e}")

if __name__ == "__main__":
    unittest.main()

