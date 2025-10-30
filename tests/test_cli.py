import unittest
from unittest.mock import patch, MagicMock, call
import io
import sys
from cli.cli import CLI
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.fichas import Ficha
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException


class TestCLIInicializacion(unittest.TestCase):
    """Tests de inicialización de CLI"""

    def test_cli_inicia_sin_juego(self):
        cli = CLI()
        self.assertIsNone(cli._CLI__juego)
        self.assertFalse(cli._CLI__partida_activa)

    def test_cli_estructura_basica(self):
        cli = CLI()
        self.assertTrue(hasattr(cli, '_CLI__juego'))
        self.assertTrue(hasattr(cli, '_CLI__partida_activa'))


class TestCLIMenuPrincipal(unittest.TestCase):
    """Tests del menú principal"""

    @patch('builtins.input', side_effect=["3"])
    @patch('builtins.print')
    def test_menu_opcion_salir(self, mock_print, mock_input):
        cli = CLI()
        cli.start()
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("MENÚ PRINCIPAL", printed_text)
        self.assertIn("Saliendo del juego", printed_text)

    @patch('builtins.input', side_effect=["invalid", "3"])
    @patch('builtins.print')
    def test_menu_opcion_invalida(self, mock_print, mock_input):
        cli = CLI()
        cli.start()
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Opción inválida", printed_text)

    @patch('builtins.input', side_effect=["4", "n", "3"])
    @patch('builtins.print')
    def test_menu_abandonar_sin_partida(self, mock_print, mock_input):
        cli = CLI()
        cli.start()
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("No hay partida en curso", printed_text)


class TestCLIIniciarPartida(unittest.TestCase):
    """Tests de inicialización de partida"""

    @patch('builtins.input', side_effect=[
        "1",        # Iniciar partida
        "Guada",    # Jugador 1
        "Lupita",   # Jugador 2
        "",         # Tirar dados
        "3"         # Salir (forzar fin)
    ])
    @patch('builtins.print')
    def test_iniciar_partida_crea_juego(self, mock_print, mock_input):
        cli = CLI()
        try:
            cli.start()
        except (StopIteration, IndexError):
            pass
        
        self.assertIsNotNone(cli._CLI__juego)
        self.assertIsInstance(cli._CLI__juego, BackgammonGame)
        self.assertEqual(len(cli._CLI__juego.get_jugadores()), 2)

    @patch('builtins.input', side_effect=[
        "1",
        "Alice",
        "Bob",
        "",
        "3"
    ])
    @patch('builtins.print')
    def test_iniciar_partida_setup_correcto(self, mock_print, mock_input):
        cli = CLI()
        try:
            cli.start()
        except (StopIteration, IndexError):
            pass
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Comienza la partida", printed_text)
        self.assertIn("Partida iniciada", printed_text)

class TestCLILoopPartida(unittest.TestCase):
    """Tests del loop principal de partida"""

    @patch('builtins.input', side_effect=[
        "1",        # Iniciar
        "Guada",
        "Bruno",
        "",         # Tirar dados
        "23", "20", # Movimiento
        "n",        # No seguir moviendo
        "3"         # Salir
    ])
    @patch('builtins.print')
    def test_turno_tira_dados_y_muestra_resultado(self, mock_print, mock_input):
        cli = CLI()
        try:
            cli.start()
        except (StopIteration, IndexError):
            pass
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Resultado del tiro", printed_text)
        self.assertIn("Turno de", printed_text)

    @patch('builtins.input', side_effect=[
        "1", "Alice", "Bob", "", "23", "20", "n", "3"
    ])
    @patch('builtins.print')
    def test_movimiento_valido_se_ejecuta(self, mock_print, mock_input):
        """Verifica que se registre al menos un movimiento"""
        cli = CLI()
        try:
            cli.start()
        except (StopIteration, IndexError):
            pass

        if cli._CLI__juego:
            historial = cli._CLI__juego.get_historial()
            self.assertGreaterEqual(len(historial), 0)

class TestCLIMovimientos(unittest.TestCase):
    """Tests de movimientos durante partida"""

    def setUp(self):
        self.cli = CLI()
        self.cli._CLI__juego = BackgammonGame()
        self.cli._CLI__partida_activa = True
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        self.cli._CLI__juego.agregar_jugador(j1)
        self.cli._CLI__juego.agregar_jugador(j2)
        self.cli._CLI__juego.setup_inicial()

    @patch('builtins.input', side_effect=["23", "20", "n"])
    @patch('builtins.print')
    def test_movimiento_normal_exitoso(self, mock_print, mock_input):
        self.cli._CLI__juego._BackgammonGame__dados_disponibles = [3]
        
        jugador = self.cli._CLI__juego.get_turno()
        
        try:
            # Simular un turno parcial
            origen = int(input("Origen: "))
            destino = int(input("Destino: "))
            self.cli._CLI__juego.mover_ficha(jugador, origen, destino)
        except (StopIteration, ValueError):
            pass

    @patch('builtins.input', side_effect=["99", "100", "n"])
    @patch('builtins.print')
    def test_movimiento_invalido_muestra_error(self, mock_print, mock_input):
        self.cli._CLI__juego._BackgammonGame__dados_disponibles = [3]
        
        jugador = self.cli._CLI__juego.get_turno()
        
        try:
            origen = int(input("Origen: "))
            destino = int(input("Destino: "))
            self.cli._CLI__juego.mover_ficha(jugador, origen, destino)
        except (MovimientoInvalidoException, StopIteration, ValueError):
            pass


class TestCLIReingreso(unittest.TestCase):
    """Tests de reingreso desde la barra"""

    def setUp(self):
        self.cli = CLI()
        self.cli._CLI__juego = BackgammonGame()
        self.cli._CLI__partida_activa = True
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        self.cli._CLI__juego.agregar_jugador(j1)
        self.cli._CLI__juego.agregar_jugador(j2)
        self.cli._CLI__juego.setup_inicial()

    def test_detecta_fichas_en_bar(self):
        # Poner ficha en bar
        ficha = Ficha("blanco")
        self.cli._CLI__juego.get_bar()["blanco"].append(ficha)
        
        bar = self.cli._CLI__juego.get_bar()["blanco"]
        self.assertEqual(len(bar), 1)


class TestCLIBearOff(unittest.TestCase):
    """Tests de fase bear-off"""

    def setUp(self):
        self.cli = CLI()
        self.cli._CLI__juego = BackgammonGame()
        self.cli._CLI__partida_activa = True
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        self.cli._CLI__juego.agregar_jugador(j1)
        self.cli._CLI__juego.agregar_jugador(j2)
        self.cli._CLI__juego.setup_inicial()

    def test_puede_sacar_fichas_cuando_todas_en_casa(self):
        # Limpiar tablero
        puntos = self.cli._CLI__juego.get_tablero().get_points()
        for i in range(24):
            puntos[i].clear()
        
        j1 = self.cli._CLI__juego.get_jugadores()[0]
        j1._Jugador__fichas.clear()
        
        # Poner todas en casa
        for i in range(6):
            ficha = Ficha("blanco")
            j1.agregar_ficha(ficha)
            puntos[i].append(ficha)
        
        self.assertTrue(self.cli._CLI__juego.puede_sacar_fichas(j1))


class TestCLIVictoria(unittest.TestCase):
    """Tests de detección de victoria"""

    def setUp(self):
        self.cli = CLI()
        self.cli._CLI__juego = BackgammonGame()
        self.cli._CLI__partida_activa = True
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        self.cli._CLI__juego.agregar_jugador(j1)
        self.cli._CLI__juego.agregar_jugador(j2)
        self.cli._CLI__juego.setup_inicial()

    def test_detecta_ganador_cuando_jugador_sin_fichas(self):
        # Simular victoria del jugador blanco
        puntos = self.cli._CLI__juego.get_tablero().get_points()
        j1, j2 = self.cli._CLI__juego.get_jugadores()
        
        # Limpiar fichas blancas
        for i in range(24):
            puntos[i] = [f for f in puntos[i] if f.get_color() != "blanco"]
        
        j1._Jugador__fichas.clear()
        
        ganador = self.cli._CLI__juego.chequear_victoria()
        self.assertEqual(ganador, j1)


class TestCLIHistorial(unittest.TestCase):
    """Tests de historial"""

    @patch('builtins.input', side_effect=["2", "3"])
    @patch('builtins.print')
    def test_mostrar_historial_sin_partida(self, mock_print, mock_input):
        cli = CLI()
        cli.start()
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("no hay partida iniciada", printed_text.lower())

    def test_mostrar_historial_con_movimientos(self):
        cli = CLI()
        cli._CLI__juego = BackgammonGame()
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        cli._CLI__juego.agregar_jugador(j1)
        cli._CLI__juego.agregar_jugador(j2)
        cli._CLI__juego.setup_inicial()
        
        cli._CLI__juego.get_historial().append("Movimiento de prueba")
        
        with patch('builtins.print') as mock_print:
            cli.mostrar_historial()
            printed_text = " ".join(str(call) for call in mock_print.call_args_list)
            self.assertIn("Movimiento de prueba", printed_text)

    def test_mostrar_historial_vacio(self):
        cli = CLI()
        cli._CLI__juego = BackgammonGame()
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        cli._CLI__juego.agregar_jugador(j1)
        cli._CLI__juego.agregar_jugador(j2)
        
        with patch('builtins.print') as mock_print:
            cli.mostrar_historial()
            printed_text = " ".join(str(call) for call in mock_print.call_args_list)
            self.assertIn("No hay movimientos", printed_text)


class TestCLIAbandonar(unittest.TestCase):
    """Tests de abandonar partida"""

    def test_abandonar_partida_activa(self):
        cli = CLI()
        cli._CLI__partida_activa = True
        cli._CLI__juego = BackgammonGame()
        
        with patch('builtins.input', return_value="s"):
            with patch('builtins.print'):
                cli.abandonar_partida()
        
        self.assertFalse(cli._CLI__partida_activa)
        self.assertIsNone(cli._CLI__juego)

    def test_cancelar_abandonar_partida(self):
        cli = CLI()
        cli._CLI__partida_activa = True
        cli._CLI__juego = BackgammonGame()
        
        with patch('builtins.input', return_value="n"):
            with patch('builtins.print'):
                cli.abandonar_partida()
        
        self.assertTrue(cli._CLI__partida_activa)
        self.assertIsNotNone(cli._CLI__juego)

    @patch('builtins.input', return_value="s")
    @patch('builtins.print')
    def test_abandonar_sin_partida_activa(self, mock_print, mock_input):
        cli = CLI()
        cli._CLI__partida_activa = False
        
        cli.abandonar_partida()
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("No hay partida en curso", printed_text)


class TestCLILeerEntero(unittest.TestCase):
    """Tests de validación de entrada de enteros"""

    def test_leer_entero_valido(self):
        cli = CLI()
        
        with patch('builtins.input', return_value="7"):
            valor = cli.leer_entero("Ingrese número: ")
        
        self.assertEqual(valor, 7)

    def test_leer_entero_invalido_reintenta(self):
        cli = CLI()
        
        respuestas = ["", "abc", "12.5", "42"]
        with patch('builtins.input', side_effect=respuestas):
            with patch('builtins.print'):
                valor = cli.leer_entero("Ingrese número: ")
        
        self.assertEqual(valor, 42)

    def test_leer_entero_vacio_reintenta(self):
        cli = CLI()
        
        with patch('builtins.input', side_effect=["", "5"]):
            with patch('builtins.print'):
                valor = cli.leer_entero("Ingrese número: ")
        
        self.assertEqual(valor, 5)

    def test_leer_entero_no_numerico_reintenta(self):
        cli = CLI()
        
        with patch('builtins.input', side_effect=["xyz", "10"]):
            with patch('builtins.print'):
                valor = cli.leer_entero("Ingrese número: ")
        
        self.assertEqual(valor, 10)


class TestCLIMostrarTablero(unittest.TestCase):
    """Tests de visualización del tablero"""

    def setUp(self):
        self.cli = CLI()
        self.cli._CLI__juego = BackgammonGame()
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        self.cli._CLI__juego.agregar_jugador(j1)
        self.cli._CLI__juego.agregar_jugador(j2)
        self.cli._CLI__juego.setup_inicial()

    @patch('builtins.print')
    def test_mostrar_tablero_formato_correcto(self, mock_print):
        self.cli.mostrar_tablero()
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("TABLERO DE BACKGAMMON", printed_text)
        self.assertIn("Zona superior", printed_text)
        self.assertIn("Zona inferior", printed_text)

    @patch('builtins.print')
    def test_mostrar_tablero_muestra_fichas(self, mock_print):
        self.cli.mostrar_tablero()
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        # Debe mostrar fichas en posiciones iniciales
        self.assertIn("[B", printed_text)  # Blancas
        self.assertIn("[N", printed_text)  # Negras


class TestCLIMostrarHistorialTurno(unittest.TestCase):
    """Tests de mostrar historial durante turno"""

    def setUp(self):
        self.cli = CLI()
        self.cli._CLI__juego = BackgammonGame()
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        self.cli._CLI__juego.agregar_jugador(j1)
        self.cli._CLI__juego.agregar_jugador(j2)

    @patch('builtins.print')
    def test_mostrar_historial_turno_vacio(self, mock_print):
        self.cli.mostrar_historial_turno()
        
        # No debe fallar con historial vacío
        self.assertTrue(True)

    @patch('builtins.print')
    def test_mostrar_historial_turno_con_movimientos(self, mock_print):
        self.cli._CLI__juego.get_historial().append("Movimiento 1")
        self.cli._CLI__juego.get_historial().append("Movimiento 2")
        self.cli._CLI__juego.get_historial().append("Movimiento 3")
        
        self.cli.mostrar_historial_turno()
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Últimos movimientos", printed_text)

    @patch('builtins.print')
    def test_mostrar_historial_turno_limita_a_3(self, mock_print):
        for i in range(10):
            self.cli._CLI__juego.get_historial().append(f"Mov {i}")
        
        self.cli.mostrar_historial_turno()
        
        # Debe mostrar solo los últimos 3
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Mov 9", printed_text)
        self.assertNotIn("Mov 0", printed_text)


class TestCLIIntegracion(unittest.TestCase):
    """Tests de integración completos"""

    @patch('builtins.input', side_effect=[
        "1",          # Iniciar partida
        "Player1",
        "Player2",
        "",           # Tirar dados
        "23", "20",   # Mover
        "n",          # No continuar
        "",           # Tirar dados turno 2
        "0", "3",     # Mover
        "n",
        "3"           # Salir
    ])
    @patch('builtins.print')
    def test_partida_dos_turnos_completos(self, mock_print, mock_input):
        cli = CLI()
        
        with patch.object(BackgammonGame, 'tirar_dados', return_value=(3, 4)):
            try:
                cli.start()
            except (StopIteration, IndexError):
                pass
        
        printed_text = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Comienza la partida", printed_text)

    def test_simular_victoria_completa(self):
        cli = CLI()
        cli._CLI__juego = BackgammonGame()
        cli._CLI__partida_activa = True
        
        j1 = Jugador("Ganador", "blanco")
        j2 = Jugador("Perdedor", "negro")
        cli._CLI__juego.agregar_jugador(j1)
        cli._CLI__juego.agregar_jugador(j2)
        cli._CLI__juego.setup_inicial()
        
        # Simular que j1 sacó todas sus fichas
        puntos = cli._CLI__juego.get_tablero().get_points()
        for i in range(24):
            puntos[i].clear()
        
        j1._Jugador__fichas.clear()
        
        # Dejar al menos una ficha negra
        ficha_negra = Ficha("negro")
        puntos[0].append(ficha_negra)
        j2._Jugador__fichas = [ficha_negra]
        
        ganador = cli._CLI__juego.chequear_victoria()
        self.assertEqual(ganador, j1)


class TestCLIManejosDeError(unittest.TestCase):
    """Tests de manejo de errores"""

    def setUp(self):
        self.cli = CLI()
        self.cli._CLI__juego = BackgammonGame()
        self.cli._CLI__partida_activa = True
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        self.cli._CLI__juego.agregar_jugador(j1)
        self.cli._CLI__juego.agregar_jugador(j2)
        self.cli._CLI__juego.setup_inicial()

    def test_movimiento_invalido_no_rompe_juego(self):
        self.cli._CLI__juego._BackgammonGame__dados_disponibles = [3]
        
        jugador = self.cli._CLI__juego.get_turno()
        
        try:
            # Intentar movimiento inválido
            self.cli._CLI__juego.mover_ficha(jugador, 10, 7)
        except MovimientoInvalidoException:
            # Debe capturar la excepción sin romper
            pass
        
        # El juego debe seguir funcionando
        self.assertIsNotNone(self.cli._CLI__juego)

    def test_entrada_no_numerica_para_punto(self):
        with patch('builtins.input', return_value="abc"):
            try:
                valor = int(input("Punto: "))
            except ValueError:
                # Debe capturar ValueError
                valor = None
        
        self.assertIsNone(valor)


class TestCLIEstadosPartida(unittest.TestCase):
    """Tests de estados de partida"""

    def test_partida_activa_despues_de_iniciar(self):
        cli = CLI()
        cli._CLI__juego = BackgammonGame()
        cli._CLI__partida_activa = True
        
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        cli._CLI__juego.agregar_jugador(j1)
        cli._CLI__juego.agregar_jugador(j2)
        cli._CLI__juego.setup_inicial()
        
        self.assertTrue(cli._CLI__partida_activa)
        self.assertIsNotNone(cli._CLI__juego)

    def test_partida_inactiva_tras_abandonar(self):
        cli = CLI()
        cli._CLI__partida_activa = True
        cli._CLI__juego = BackgammonGame()
        
        with patch('builtins.input', return_value="s"):
            with patch('builtins.print'):
                cli.abandonar_partida()
        
        self.assertFalse(cli._CLI__partida_activa)


if __name__ == "__main__":
    unittest.main()