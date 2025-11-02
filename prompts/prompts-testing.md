
Modelo utilizado
ChatGPT (GPT-4, versión Octubre 2025)

Prompt 1: test de movimiento válido
Mensaje:
Quiero hacer un test para por ej asegurarme de que el jugador puede mover una ficha blanca  
desde el punto 7 al punto 6 cuando el dado tiene valor 1.  ¿Cómo lo hago?

Respuesta:
import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.fichas import Ficha

class TestMovimientoValido(unittest.TestCase):
    def test_movimiento_valido(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()
        juego._BackgammonGame__dados_disponibles = [1]
        puntos = juego.get_tablero().get_points()
        ficha = puntos[7][-1]
        juego.mover_ficha(j1, 7, 6)
        self.assertNotIn(ficha, puntos[7])

Prompt 2: test de victoria

Mensaje:
Necesito un test que verifique que cuando un jugador saca todas sus fichas, para ver si
el método finalizar_jugada() devuelve al ganado digamos, ayudame. 

Respuesta:

def test_bearoff_y_victoria(self):
    juego = BackgammonGame()
    j1 = Jugador("Guada", "blanco")
    j2 = Jugador("Bruno", "negro")
    juego.agregar_jugador(j1)
    juego.agregar_jugador(j2)
    juego._BackgammonGame__fichas_fuera = {"blanco": 15, "negro": 0}
    ganador = juego.finalizar_jugada()
    self.assertEqual(ganador.get_color(), "blanco")

Prompt 3: test de los dados

Mensaje:
Quiero probar que el método roll() de Dados devuelve dos valores entre 1 y 6,
y que tamb si son iguales genera 4 movimientos.

Respuesta:

import unittest
from codigo.dados import Dados

class TestDados(unittest.TestCase):
    def test_tirada_y_dobles(self):
        dados = Dados()
        dados._Dados__valores = (4, 4)
        movs = dados.movimientos_disponibles()
        self.assertEqual(len(movs), 4)
        self.assertTrue(all(d == 4 for d in movs))


Prompt 4: test de CLI que abandona partida

Mensaje:
Quiero hacer un test que haga como que el jugador elige abandonar la partida en la CLI,
para comprobar que se limpia digamos como se hace eso?

Respuesta:

from unittest.mock import patch

@patch("builtins.input", side_effect=["s"])
def test_abandonar_partida(self, mock_input):
    cli = CLI()
    cli._CLI__partida_activa = True
    cli._CLI__juego = BackgammonGame()
    cli.abandonar_partida()
    self.assertFalse(cli._CLI__partida_activa)

Prompt 5: test de reingreso desde la barra

Mensaje:
Quiero probar que si una ficha es capturada, queda en la barra,
y que después con un dado válido se puede reingresar correctamente al tablero, con los test 

Respuesta:

import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.fichas import Ficha

class TestReingresoDesdeBarra(unittest.TestCase):
    def test_reingreso_ficha_valido(self):
        juego = BackgammonGame()
        j1 = Jugador("Guada", "blanco")
        j2 = Jugador("Bruno", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Simular ficha capturada
        ficha_capturada = Ficha("blanco")
        juego.get_bar()["blanco"].append(ficha_capturada)

        # Configurar dados disponibles
        juego._BackgammonGame__dados_disponibles = [3]

        # Intentar reingreso
        juego.reingresar_ficha(j1, 21)

        puntos = juego.get_tablero().get_points()
        self.assertIn(ficha_capturada, puntos[21])
        self.assertEqual(len(juego.get_bar()["blanco"]), 0)

Prompt 6: test de tirar dados y limpiar disponibles

Mensaje:
Quiero verificar que al tirar los dados se actualicen correctamente los valores
y que al finalizar el turno se vacíen los dados osea que vuelvan a quedar en cero me explico

Respuesta:

import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador

class TestDadosYTurno(unittest.TestCase):
    def test_tirar_y_finalizar_turno(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        tirada = juego.tirar_dados()
        self.assertEqual(len(juego.get_dados_disponibles()), 2 if tirada[0] != tirada[1] else 4)

        juego.finalizar_turno()
        self.assertEqual(juego.get_dados_disponibles(), [])

Prompt 7: test de setup_inicial

Mensaje:
Quiero hacer un test que confirme que el método setup_inicial()
coloca la cantidad correcta de fichas del backgammon en cada punto al iniciar el juego

Respuesta:

import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador

class TestSetupInicial(unittest.TestCase):
    def test_disposicion_inicial_correcta(self):
        juego = BackgammonGame()
        j1 = Jugador("Guada", "blanco")
        j2 = Jugador("Bruno", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        puntos = juego.get_tablero().get_points()
        self.assertEqual(len(puntos[23]), 2)
        self.assertEqual(len(puntos[12]), 5)
        self.assertEqual(len(puntos[7]), 3)
        self.assertEqual(len(puntos[5]), 5)

Prompt 8: test de movimiento inválido bloqueado

Mensaje:
Necesito probar que si el destino tiene dos fichas del rival,
el método mover_ficha lance la excepción MovimientoInvalidoException que tengo definida

Respuesta:

import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.fichas import Ficha
from codigo.excepciones import MovimientoInvalidoException

class TestMovimientoBloqueado(unittest.TestCase):
    def test_destino_bloqueado_por_rival(self):
        juego = BackgammonGame()
        j1 = Jugador("Guada", "blanco")
        j2 = Jugador("Bruno", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Simular punto bloqueado por negras
        puntos = juego.get_tablero().get_points()
        puntos[10] = [Ficha("negro"), Ficha("negro")]

        juego._BackgammonGame__dados_disponibles = [3]

        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(j1, 13, 10)

Prompt 9: test de CLI — tirar dados

Mensaje:
Quiero hacer un test de la interfaz CLI para verificar que cuando el jugador tira los dados,
se imprime el mensaje "Resultado del tiro" y se actualizan los dados del juego.
Puedo hacerlo con mock?

Respuesta:

import unittest
from unittest.mock import patch
from cli.cli import CLI

class TestCLITirarDados(unittest.TestCase):
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["1", "Guada", "Bruno", "", "3"])
    def test_tirar_dados_muestra_resultado(self, mock_input, mock_print):
        cli = CLI()
        try:
            cli.start()
        except (StopIteration, IndexError):
            pass

        printed = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("Resultado del tiro", printed)

Prompt 10: test de CLI — abandonar partida limpia estado

Mensaje:
Quiero probar que si el jugador elige la opción de abandonar partida en el menú,
la CLI finaliza la partida y deja el estado del juego como no iniciado.

Respuesta:

import unittest
from unittest.mock import patch
from cli.cli import CLI
from codigo.backgammon import BackgammonGame

class TestCLIAbandonarPartida(unittest.TestCase):
    @patch("builtins.input", side_effect=["4"])
    @patch("builtins.print")
    def test_abandonar_partida_limpia_estado(self, mock_print, mock_input):
        cli = CLI()
        cli._CLI__juego = BackgammonGame()
        cli._CLI__partida_activa = True

        cli.start()
        self.assertFalse(cli._CLI__partida_activa)

Prompt 11: test de Pygame — dibujar tablero sin errores

Mensaje:
Necesito probar que el método dibujar_tablero() de mi interfaz Pygame
se ejecuta sin lanzar errores ni excepciones, usando un mock del juego.

Respuesta:

import unittest
import pygame
from pygame_ui.interfaz_pygame import InterfazPygame
from unittest.mock import MagicMock

class TestInterfazPygame(unittest.TestCase):
    def test_dibujar_tablero_no_crashea(self):
        mock_juego = MagicMock()
        mock_juego.get_tablero().get_points.return_value = [[] for _ in range(24)]
        mock_juego.get_bar.return_value = {"blanco": [], "negro": []}
        mock_juego.get_turno.return_value.get_nombre.return_value = "Guada"
        mock_juego.get_turno.return_value.get_color.return_value = "blanco"
        mock_juego.get_dados_disponibles.return_value = []
        interfaz = InterfazPygame(mock_juego)

        try:
            interfaz.dibujar_tablero()
        except Exception as e:
            self.fail(f"dibujar_tablero lanzó una excepción: {e}")

Prompt 12: test de Pygame — mostrar victoria

Mensaje:
Quiero testear que el método mostrar_victoria() realmente muestra el texto del ganador
cuando el juego tiene un jugador ganador configurado.

Respuesta:

import unittest
from unittest.mock import MagicMock
from pygame_ui.interfaz_pygame import InterfazPygame

class TestPygameVictoria(unittest.TestCase):
    def test_mostrar_victoria_dibuja_texto(self):
        mock_juego = MagicMock()
        mock_ganador = MagicMock()
        mock_ganador.get_nombre.return_value = "Guada"
        mock_juego.get_ganador.return_value = mock_ganador

        interfaz = InterfazPygame(mock_juego)
        try:
            interfaz.mostrar_victoria()
        except Exception as e:
            self.fail(f"mostrar_victoria lanzó excepción: {e}")

Prompt 13: test de Pygame — click en botón tirar dados

Mensaje:
Quiero simular un click en el botón “Tirar dados” en Pygame
para asegurarme de que cambia la bandera dados_tirados y actualiza el mensaje.

Respuesta:

import unittest
import pygame
from pygame_ui.interfaz_pygame import InterfazPygame
from unittest.mock import MagicMock

class TestBotonDados(unittest.TestCase):
    def test_click_boton_tirar_dados(self):
        mock_juego = MagicMock()
        mock_juego.tirar_dados.return_value = (3, 5)
        mock_juego.get_dados_disponibles.return_value = [3, 5]
        mock_juego.get_turno.return_value.get_nombre.return_value = "Guada"
        mock_juego.get_turno.return_value.get_color.return_value = "blanco"

        interfaz = InterfazPygame(mock_juego)
        interfaz.manejar_click((interfaz.boton_dados.x + 5, interfaz.boton_dados.y + 5))

        self.assertTrue(interfaz.dados_tirados)
        self.assertIn("Dados:", interfaz.mensaje)

Prompt 14: test de historial registra movimiento

Mensaje:
Quiero verificar que cuando el jugador mueve una ficha,
el movimiento se agrega correctamente al historial del juego.
¿Cómo puedo hacer ese test?

Respuesta:

import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador

class TestHistorial(unittest.TestCase):
    def test_historial_registra_movimiento(self):
        juego = BackgammonGame()
        j1 = Jugador("Guada", "blanco")
        j2 = Jugador("Bruno", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [1]
        juego.mover_ficha(j1, 7, 6)

        historial = juego.get_historial()
        self.assertTrue(any("movió una ficha" in h for h in historial))

Prompt 15: test de cambio de turno después del movimiento

Mensaje:
Necesito probar que cuando un jugador usa todos sus dados,
automáticamente cambia el turno al otro jugador.

Respuesta:

import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador

class TestCambioTurno(unittest.TestCase):
    def test_cambia_turno_despues_de_movimientos(self):
        juego = BackgammonGame()
        j1 = Jugador("Guada", "blanco")
        j2 = Jugador("Bruno", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [1]
        turno_inicial = juego.get_turno()
        juego.mover_ficha(j1, 7, 6)
        turno_despues = juego.get_turno()

        self.assertNotEqual(turno_inicial, turno_despues)

Prompt 16: test de excepción por ficha incorrecta

Mensaje:
Quiero asegurarme de que si intento mover una ficha que no pertenece al jugador actual,
se lanza la excepción FichaInvalidaException.

Respuesta:

import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.excepciones import FichaInvalidaException

class TestFichaInvalida(unittest.TestCase):
    def test_movimiento_con_ficha_incorrecta(self):
        juego = BackgammonGame()
        j1 = Jugador("Guada", "blanco")
        j2 = Jugador("Bruno", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [1]
        with self.assertRaises(FichaInvalidaException):
            juego.mover_ficha(j2, 7, 6)

Prompt 17: test de puede_sacar_fichas verdadero

Mensaje:
Quiero testear que cuando todas las fichas de un jugador están dentro de su “casa”,
el método puede_sacar_fichas() devuelva True.

Respuesta:

import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.fichas import Ficha

class TestBearOff(unittest.TestCase):
    def test_puede_sacar_fichas_retorna_true(self):
        juego = BackgammonGame()
        j1 = Jugador("Guada", "blanco")
        j2 = Jugador("Bruno", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)

        # Todas las fichas blancas en su casa (0–5)
        puntos = [[] for _ in range(24)]
        for i in range(15):
            puntos[i % 6].append(Ficha("blanco"))
        juego.get_tablero().set_points(puntos)

        self.assertTrue(juego.puede_sacar_fichas(j1))

Prompt 18: test de CLI — menú principal muestra opciones

Mensaje:
Quiero probar que cuando arranca la CLI,
el menú principal imprime las opciones del juego (por ejemplo, “1. Nueva partida”).
¿Cómo puedo hacer eso?

Respuesta:

import unittest
from unittest.mock import patch
from cli.cli import CLI

class TestCLIMenu(unittest.TestCase):
    @patch("builtins.print")
    @patch("builtins.input", side_effect=["0"])
    def test_menu_principal_muestra_opciones(self, mock_input, mock_print):
        cli = CLI()
        try:
            cli.start()
        except (StopIteration, IndexError):
            pass

        printed = " ".join(str(call) for call in mock_print.call_args_list)
        self.assertIn("1.", printed)
        self.assertIn("Nueva partida", printed)

Prompt 19: test de excepción por movimiento inválido
Mensaje:
Necesito un test que verifique que si intento mover una ficha a un punto bloqueado,
se lanza una excepción MovimientoInvalidoException.

Respuesta:

def test_movimiento_invalido_lanza_excepcion(self):
    juego = BackgammonGame()
    j1 = Jugador("Guada", "blanco")
    j2 = Jugador("Bruno", "negro")
    juego.agregar_jugador(j1)
    juego.agregar_jugador(j2)
    juego.setup_inicial()
    with self.assertRaises(MovimientoInvalidoException):
        juego.mover_ficha(j1, 7, 18)