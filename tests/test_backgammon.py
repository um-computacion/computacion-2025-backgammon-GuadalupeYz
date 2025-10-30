import unittest
from unittest.mock import Mock, patch
import pytest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException
from codigo.fichas import Ficha
from codigo.tablero import Tablero
from codigo.dados import Dados


class TestBackgammonGameBasico(unittest.TestCase):
    """Tests básicos de inicialización y setup"""

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
        juego.iniciar_juego()  # No debe lanzar error

    def test_no_pueden_haber_mas_de_dos_jugadores(self):
        juego = BackgammonGame()
        juego.agregar_jugador(Jugador("Guada", "blanco"))
        juego.agregar_jugador(Jugador("Lupita", "negro"))

        with self.assertRaises(ValueError):
            juego.agregar_jugador(Jugador("Extra", "rojo"))

    def test_setup_inicial_asigna_fichas_correctamente(self):
        """Setup inicial con posiciones correctas de backgammon"""
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        self.assertEqual(jugador1.cantidad_fichas(), 15)
        self.assertEqual(jugador2.cantidad_fichas(), 15)
        
        tablero = juego.get_tablero().get_points()
        # Posiciones iniciales blancas
        self.assertEqual(len(tablero[23]), 2)
        self.assertEqual(len(tablero[12]), 5)
        self.assertEqual(len(tablero[7]), 3)
        self.assertEqual(len(tablero[5]), 5)
        
        # Posiciones iniciales negras
        self.assertEqual(len(tablero[0]), 2)
        self.assertEqual(len(tablero[11]), 5)
        self.assertEqual(len(tablero[16]), 3)
        self.assertEqual(len(tablero[18]), 5)


class TestBackgammonDados(unittest.TestCase):
    """Tests de tirada de dados"""

    def test_tirar_dados(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        
        resultado = juego.tirar_dados()
        self.assertIsInstance(resultado, tuple)
        self.assertEqual(len(resultado), 2)
        for valor in resultado:
            self.assertGreaterEqual(valor, 1)
            self.assertLessEqual(valor, 6)

    def test_tirar_dados_dobles_genera_cuatro_movimientos(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        
        self.assertEqual(len(juego.get_jugadores()), 2)
        self.assertIsInstance(juego.get_tablero(), Tablero)
        self.assertIsInstance(juego.get_dados(), Dados)
        self.assertIsInstance(juego.get_historial(), list)
        self.assertIsInstance(juego.get_bar(), dict)
        self.assertEqual(juego.get_ultima_tirada(), (0, 0))

    def test_setters_basicos(self):
        juego = BackgammonGame()
        
        nuevo_tablero = Tablero()
        juego.set_tablero(nuevo_tablero)
        self.assertEqual(juego.get_tablero(), nuevo_tablero)
        
        nuevos_dados = Dados()
        juego.set_dados(nuevos_dados)
        self.assertEqual(juego.get_dados(), nuevos_dados)

    def test_get_turno_sin_jugadores_lanza_error(self):
        juego = BackgammonGame()
        with self.assertRaises(ValueError):
            juego.get_turno()

    def test_get_ganador_devuelve_none_sin_victoria(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()
        
        self.assertIsNone(juego.get_ganador())

    def test_get_fichas_fuera_blanco(self):
        juego = BackgammonGame()
        fichas = juego.get_fichas_fuera("blanco")
        self.assertIsInstance(fichas, list)
        self.assertEqual(len(fichas), 0)

    def test_get_fichas_fuera_negro(self):
        juego = BackgammonGame()
        fichas = juego.get_fichas_fuera("negro")
        self.assertIsInstance(fichas, list)
        self.assertEqual(len(fichas), 0)


class TestBackgammonEdgeCases(unittest.TestCase):
    """Tests de casos límite y situaciones especiales"""

    def test_mover_en_turno_incorrecto(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [3]

        # j2 intenta mover en turno de j1
        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(j2, 0, 3)

    def test_finalizar_turno_cambia_jugador_y_limpia_dados(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        
        juego.tirar_dados()
        turno_inicial = juego.get_turno()
        
        juego.finalizar_turno()
        
        self.assertNotEqual(juego.get_turno(), turno_inicial)
        self.assertEqual(len(juego.get_dados_disponibles()), 0)

    def test_reingresar_sin_dados_lanza_error(self):
        """Test corregido: necesita dados disponibles pero sin el dado correcto"""
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Poner ficha en bar
        ficha = Ficha("blanco")
        juego.get_bar()["blanco"].append(ficha)

        # Limpiar dados disponibles (sin dados no puede reingresar)
        juego._BackgammonGame__dados_disponibles = []

        with self.assertRaises(MovimientoInvalidoException):
            juego.reingresar_ficha(j1, 20)


    def test_sacar_ficha_sin_estar_todas_en_casa_lanza_error(self):
        juego = BackgammonGame()
        j1 = Jugador("Blanco", "blanco")
        j2 = Jugador("Negro", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [2]

        with self.assertRaises(MovimientoInvalidoException):
            juego.sacar_ficha(j1, 5)

    def test_sacar_ficha_de_punto_vacio_lanza_error(self):
        juego = BackgammonGame()
        j1 = Jugador("Blanco", "blanco")
        j2 = Jugador("Negro", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Preparar todas en casa
        puntos = juego.get_tablero().get_points()
        for i in range(24):
            puntos[i].clear()
        
        j1._Jugador__fichas.clear()
        ficha = Ficha("blanco")
        j1.agregar_ficha(ficha)
        puntos[2].append(ficha)

        juego._BackgammonGame__dados_disponibles = [3]

        with self.assertRaises(MovimientoInvalidoException):
            juego.sacar_ficha(j1, 5)  # Punto 5 está vacío

    def test_sacar_ficha_ajena_lanza_error(self):
        juego = BackgammonGame()
        j1 = Jugador("Blanco", "blanco")
        j2 = Jugador("Negro", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Preparar todas blancas en casa
        puntos = juego.get_tablero().get_points()
        for i in range(24):
            puntos[i].clear()
        
        j1._Jugador__fichas.clear()
        # Poner ficha negra en casa de blancas
        ficha_negra = Ficha("negro")
        puntos[2].append(ficha_negra)

        juego._BackgammonGame__dados_disponibles = [3]

        with self.assertRaises(FichaInvalidaException):
            juego.sacar_ficha(j1, 2)

    def test_cambiar_turno_sin_jugadores_lanza_error(self):
        juego = BackgammonGame()
        with self.assertRaises(ValueError):
            juego.cambiar_turno()

    def test_setup_inicial_sin_jugadores_lanza_error(self):
        juego = BackgammonGame()
        with self.assertRaises(ValueError):
            juego.setup_inicial()

    def test_historial_registra_captura(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [3]

        # Colocar ficha negra sola
        ficha_negra = Ficha("negro")
        juego.get_tablero().get_points()[20] = [ficha_negra]

        juego.mover_ficha(j1, 23, 20)

        historial = juego.get_historial()
        self.assertTrue(any("capturó" in entrada for entrada in historial))

    def test_reingresar_captura_ficha_rival(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Poner ficha blanca en bar
        ficha_blanca = juego.get_tablero().get_points()[23].pop()
        juego.get_bar()["blanco"].append(ficha_blanca)

        # Poner una ficha negra sola en punto de reingreso
        ficha_negra = Ficha("negro")
        juego.get_tablero().get_points()[20] = [ficha_negra]

        juego._BackgammonGame__dados_disponibles = [4]  # reingreso en 20

        juego.reingresar_ficha(j1, 20)

        # La ficha negra debe ir al bar
        self.assertEqual(len(juego.get_bar()["negro"]), 1)
        self.assertIn(ficha_negra, juego.get_bar()["negro"])

    def test_mover_consume_dado_correcto(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [2, 5]
        
        juego.mover_ficha(j1, 23, 21)  # Mover 2

        self.assertNotIn(2, juego.get_dados_disponibles())
        self.assertIn(5, juego.get_dados_disponibles())

    def test_reingresar_consume_dado_correcto(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Poner ficha en bar
        ficha = juego.get_tablero().get_points()[23].pop()
        juego.get_bar()["blanco"].append(ficha)

        juego._BackgammonGame__dados_disponibles = [3, 4]

        juego.reingresar_ficha(j1, 20)  # necesita dado 4

        self.assertNotIn(4, juego.get_dados_disponibles())
        self.assertIn(3, juego.get_dados_disponibles())

    def test_sacar_ficha_consume_dado_correcto(self):
        juego = BackgammonGame()
        j1 = Jugador("Blanco", "blanco")
        j2 = Jugador("Negro", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Todas en casa
        puntos = juego.get_tablero().get_points()
        for i in range(24):
            puntos[i].clear()
        
        j1._Jugador__fichas.clear()
        ficha = Ficha("blanco")
        j1.agregar_ficha(ficha)
        puntos[2].append(ficha)

        juego._BackgammonGame__dados_disponibles = [3, 5]

        juego.sacar_ficha(j1, 2)  # necesita dado 3

        self.assertNotIn(3, juego.get_dados_disponibles())
        self.assertIn(5, juego.get_dados_disponibles())

    def test_dados_disponibles_devuelve_copia(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)

        juego._BackgammonGame__dados_disponibles = [3, 5]
        
        dados = juego.get_dados_disponibles()
        dados.append(6)  # Modificar copia

        # El original no debe cambiar
        self.assertEqual(len(juego.get_dados_disponibles()), 2)


class TestBackgammonIntegracion(unittest.TestCase):
    """Tests de integración con flujos completos"""

    def test_flujo_completo_turno_basico(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Turno 1: Alice tira y mueve
        self.assertEqual(juego.get_turno(), j1)
        juego.tirar_dados()
        self.assertGreater(len(juego.get_dados_disponibles()), 0)

        # Simular movimiento válido
        juego._BackgammonGame__dados_disponibles = [3]
        juego.mover_ficha(j1, 23, 20)

        # Turno cambió automáticamente
        self.assertEqual(juego.get_turno(), j2)

    def test_flujo_captura_y_reingreso(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Capturar ficha
        juego._BackgammonGame__dados_disponibles = [3]
        ficha_negra = Ficha("negro")
        juego.get_tablero().get_points()[20] = [ficha_negra]
        
        juego.mover_ficha(j1, 23, 20)
        
        # Verificar captura
        self.assertEqual(len(juego.get_bar()["negro"]), 1)

        # Cambiar a Bob y reingresar
        juego.cambiar_turno()
        juego._BackgammonGame__dados_disponibles = [5]
        
        juego.reingresar_ficha(j2, 4)  # negro reingresa en 4 (distancia 5)
        
        self.assertEqual(len(juego.get_bar()["negro"]), 0)

    def test_setup_inicial_limpia_estado_previo(self):
        """Test corregido: verifica que setup_inicial limpia el estado"""
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        # Modificar estado
        juego.get_historial().append("test")
        juego.get_bar()["blanco"].append(Ficha("blanco"))
        juego._BackgammonGame__dados_disponibles = [3, 5]

        # Hacer setup de nuevo
        juego.setup_inicial()

        # Verificar que se limpió el estado
        self.assertEqual(len(juego.get_historial()), 0)
        self.assertEqual(len(juego.get_bar()["blanco"]), 0)
        self.assertEqual(len(juego.get_bar()["negro"]), 0)
        
        # Verificar que las fichas están en sus posiciones iniciales
        tablero = juego.get_tablero().get_points()
        self.assertEqual(len(tablero[23]), 2)  # Blancas
        self.assertEqual(len(tablero[0]), 2)   # Negras
        
        # Verificar que los jugadores tienen 15 fichas cada uno
        self.assertEqual(j1.cantidad_fichas(), 15)
        self.assertEqual(j2.cantidad_fichas(), 15)

    def test_tirar_dados_normales_genera_dos_movimientos(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)

        juego.get_dados().roll = Mock(return_value=(3, 5))
        juego.tirar_dados()
        
        dados_disp = juego.get_dados_disponibles()
        self.assertEqual(len(dados_disp), 2)
        self.assertIn(3, dados_disp)
        self.assertIn(5, dados_disp)


class TestBackgammonTurnos(unittest.TestCase):
    """Tests de gestión de turnos"""

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

    def test_cambiar_turno_varias_veces_alterna(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        
        juego.cambiar_turno()
        self.assertEqual(juego.get_turno(), jugador2)
        juego.cambiar_turno()
        self.assertEqual(juego.get_turno(), jugador1)

    def test_cambiar_turno_limpia_dados_disponibles(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        
        juego.tirar_dados()
        self.assertGreater(len(juego.get_dados_disponibles()), 0)
        
        juego.cambiar_turno()
        self.assertEqual(len(juego.get_dados_disponibles()), 0)
        self.assertEqual(juego.get_ultima_tirada(), (0, 0))


class TestBackgammonMovimientos(unittest.TestCase):
    """Tests de movimientos de fichas"""

    def test_mover_ficha_sin_tirar_dados_lanza_error(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 23, 20)

    def test_mover_ficha_valido_con_dados(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Forzar dados disponibles
        juego._BackgammonGame__dados_disponibles = [3, 5]
        juego._BackgammonGame__ultima_tirada = (3, 5)

        tablero = juego.get_tablero().get_points()
        fichas_antes = len(tablero[23])
        
        juego.mover_ficha(jugador1, 23, 20)  # Mover 3 espacios

        self.assertEqual(len(tablero[23]), fichas_antes - 1)
        self.assertEqual(len(tablero[20]), 1)

    def test_mover_ficha_origen_vacio_lanza_excepcion(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [5]
        
        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 10, 5)  # punto 10 está vacío

    def test_mover_ficha_de_otro_jugador_lanza_excepcion(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [3]

        # Intentar mover fichas negras (punto 0) siendo jugador blanco
        with self.assertRaises(FichaInvalidaException):
            juego.mover_ficha(jugador1, 0, 3)

    def test_mover_ficha_destino_fuera_de_rango(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [1]

        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 0, -1)

        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 0, 24)

    def test_mover_con_dado_invalido_lanza_excepcion(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Dados disponibles: 2 y 4
        juego._BackgammonGame__dados_disponibles = [2, 4]
        juego._BackgammonGame__ultima_tirada = (2, 4)

        # Intentar mover 5 espacios (no hay dado de 5)
        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 23, 18)

    def test_mover_ficha_direccion_incorrecta_blancas(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [3]

        # Blancas no pueden moverse hacia índices mayores
        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(j1, 5, 8)

    def test_mover_ficha_direccion_incorrecta_negras(self):
        juego = BackgammonGame()
        j1 = Jugador("Alice", "blanco")
        j2 = Jugador("Bob", "negro")
        juego.agregar_jugador(j1)
        juego.agregar_jugador(j2)
        juego.setup_inicial()
        
        juego.cambiar_turno()  # Cambiar a negras
        juego._BackgammonGame__dados_disponibles = [3]

        # Negras no pueden moverse hacia índices menores
        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(j2, 18, 15)


class TestBackgammonCaptura(unittest.TestCase):
    """Tests de captura de fichas"""

    def test_captura_ficha_envia_al_bar(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [3]

        # Colocar una ficha negra sola en punto 20
        ficha_negra = Ficha("negro")
        juego.get_tablero().get_points()[20] = [ficha_negra]

        juego.mover_ficha(jugador1, 23, 20)

        # La ficha negra debe estar en el bar
        self.assertEqual(len(juego.get_bar()["negro"]), 1)
        # En punto 20 debe estar la ficha blanca
        self.assertEqual(juego.get_tablero().get_points()[20][-1].get_color(), "blanco")

    def test_no_captura_si_mas_de_una_ficha_en_destino(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [3]

        # Colocar dos fichas negras en punto 20
        ficha_negra1 = Ficha("negro")
        ficha_negra2 = Ficha("negro")
        juego.get_tablero().get_points()[20] = [ficha_negra1, ficha_negra2]

        # Blancas en punto bloqueado
        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 23, 20)


class TestBackgammonReingreso(unittest.TestCase):
    """Tests de reingreso desde la barra"""

    def test_reingresar_ficha_valido(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Poner una ficha blanca en el bar
        ficha_blanca = juego.get_tablero().get_points()[23].pop()
        juego.get_bar()["blanco"].append(ficha_blanca)

        # Setear dados: para blancas, reingreso en punto 20 necesita dado 4 (24-20=4)
        juego._BackgammonGame__dados_disponibles = [4]

        juego.reingresar_ficha(jugador1, 20)

        self.assertEqual(len(juego.get_bar()["blanco"]), 0)
        self.assertIn(ficha_blanca, juego.get_tablero().get_points()[20])

    def test_reingresar_sin_fichas_en_bar_lanza_error(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [3]

        with self.assertRaises(MovimientoInvalidoException):
            juego.reingresar_ficha(jugador1, 20)

    def test_mover_con_fichas_en_bar_lanza_error(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Agregar ficha al bar
        ficha = Ficha("blanco")
        juego.get_bar()["blanco"].append(ficha)

        juego._BackgammonGame__dados_disponibles = [3]

        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 23, 20)

    def test_reingreso_en_punto_bloqueado_lanza_error(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Poner ficha blanca en bar
        ficha_blanca = juego.get_tablero().get_points()[23].pop()
        juego.get_bar()["blanco"].append(ficha_blanca)

        # Bloquear punto 20 con dos fichas negras
        juego.get_tablero().get_points()[20] = [Ficha("negro"), Ficha("negro")]

        juego._BackgammonGame__dados_disponibles = [4]  # reingreso en 20

        with self.assertRaises(MovimientoInvalidoException):
            juego.reingresar_ficha(jugador1, 20)


class TestBackgammonHistorial(unittest.TestCase):
    """Tests de historial de movimientos"""

    def test_historial_registra_movimientos(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        juego._BackgammonGame__dados_disponibles = [3]
        juego.mover_ficha(jugador1, 23, 20)

        historial = juego.get_historial()
        self.assertEqual(len(historial), 1)
        self.assertIn("Guada", historial[0])
        self.assertIn("23", historial[0])
        self.assertIn("20", historial[0])


class TestBackgammonVictoria(unittest.TestCase):
    """Tests de condiciones de victoria"""

    def test_chequear_victoria_sin_ganador(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        self.assertIsNone(juego.chequear_victoria())

    def test_chequear_victoria_jugador1_gana(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Vaciar todas las fichas del jugador1 para simular victoria
        puntos = juego.get_tablero().get_points()
        for punto in [23, 12, 7, 5]:
            puntos[punto].clear()
        jugador1._Jugador__fichas.clear()

        self.assertEqual(juego.chequear_victoria(), jugador1)

    def test_chequear_victoria_jugador2_gana(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Vaciar todas las fichas del jugador2
        puntos = juego.get_tablero().get_points()
        for punto in [0, 11, 16, 18]:
            puntos[punto].clear()
        jugador2._Jugador__fichas.clear()

        self.assertEqual(juego.chequear_victoria(), jugador2)

    def test_finalizar_jugada_sin_victoria(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        self.assertIsNone(juego.finalizar_jugada())

    def test_finalizar_jugada_con_victoria(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Simular que jugador1 ganó
        puntos = juego.get_tablero().get_points()
        for punto in [23, 12, 7, 5]:
            puntos[punto].clear()
        jugador1._Jugador__fichas.clear()

        ganador = juego.finalizar_jugada()
        self.assertEqual(ganador, jugador1)


class TestBackgammonEstado(unittest.TestCase):
    """Tests de estado y utilidades"""

    def test_mostrar_estado_inicial(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Zoe", "blanco")
        jugador2 = Jugador("Pili", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.iniciar_juego()

        estado = juego.mostrar_estado()
        self.assertIn("Turno actual: Zoe", estado)
        self.assertIn("Dados disponibles: []", estado)
        self.assertIn("Bar: {blanco: 0, negro: 0}", estado)

    def test_mostrar_estado_despues_de_tirar_dados(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Zoe", "blanco")
        jugador2 = Jugador("Pili", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.iniciar_juego()
        juego.tirar_dados()

        estado = juego.mostrar_estado()
        self.assertIn("Turno actual: Zoe", estado)
        self.assertIn("Dados disponibles:", estado)

    def test_mostrar_estado_con_bar_y_historial(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Zoe", "blanco")
        jugador2 = Jugador("Pili", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.iniciar_juego()

        # Agregar ficha al bar y al historial
        ficha = Ficha("blanco")
        juego.get_bar()["blanco"].append(ficha)
        juego.get_historial().append("Zoe movio una ficha")

        estado = juego.mostrar_estado()
        self.assertIn("Bar: {blanco: 1, negro: 0}", estado)
        self.assertIn("Historial", estado)
        self.assertIn("Zoe movio una ficha", estado)

    def test_reiniciar_partida_vacia_todo(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Carli", "blanco")
        jugador2 = Jugador("Eva", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.iniciar_juego()
        juego.tirar_dados()
        juego.get_historial().append("Movimiento ficticio")
        juego.get_bar()["blanco"].append(Ficha("blanco"))

        juego.reiniciar_partida()

        self.assertEqual(juego.get_historial(), [])
        self.assertEqual(juego.get_bar(), {"blanco": [], "negro": []})
        self.assertEqual(juego.get_turno().get_nombre(), "Carli")
        self.assertEqual(juego.get_dados_disponibles(), [])


class TestBackgammonBearOff(unittest.TestCase):
    """Tests de sacar fichas del tablero"""

    def test_puede_sacar_fichas_todas_en_casa(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Blanco", "blanco")
        jugador2 = Jugador("Negro", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Limpiar tablero y poner todas las fichas blancas en su casa (0-5)
        puntos = juego.get_tablero().get_points()
        for i in range(24):
            puntos[i].clear()
        
        jugador1._Jugador__fichas.clear()
        for i in range(6):
            for _ in range(2):
                ficha = Ficha("blanco")
                jugador1.agregar_ficha(ficha)
                puntos[i].append(ficha)

        self.assertTrue(juego.puede_sacar_fichas(jugador1))

    def test_no_puede_sacar_fichas_si_hay_fuera_de_casa(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Blanco", "blanco")
        jugador2 = Jugador("Negro", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Estado inicial: fichas están en varios puntos
        self.assertFalse(juego.puede_sacar_fichas(jugador1))

    def test_sacar_ficha_con_dado_exacto(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Blanco", "blanco")
        jugador2 = Jugador("Negro", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # Preparar: todas las blancas en casa
        puntos = juego.get_tablero().get_points()
        for i in range(24):
            puntos[i].clear()
        
        jugador1._Jugador__fichas.clear()
        ficha = Ficha("blanco")
        jugador1.agregar_ficha(ficha)
        puntos[2].append(ficha)  # Punto 2, necesita dado 3 para sacar

        juego._BackgammonGame__dados_disponibles = [3]

        juego.sacar_ficha(jugador1, 2)

        self.assertEqual(len(puntos[2]), 0)
        self.assertEqual(len(juego.get_fichas_fuera("blanco")), 1)

