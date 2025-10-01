import unittest
from codigo.backgammon import BackgammonGame
from codigo.jugadores import Jugador
from codigo.excepciones import MovimientoInvalidoException, FichaInvalidaException
from codigo.fichas import Ficha

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

    def test_mover_ficha_destino_fuera_de_rango(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        #pruebo destino invalido (-1 y 24)
        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 0, -1)

        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 0, 24)

    def test_historial_registra_movimientos(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        juego.mover_ficha(jugador1, 0, 5)
        historial = juego.get_historial()

        self.assertEqual(len(historial), 1)
        self.assertIn("Guada movió una ficha de 0 a 5", historial[0])

    def test_chequear_victoria_sin_ganador(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        #aca ningun jugador deberia haber ganado aun
        self.assertIsNone(juego.chequear_victoria())

    def test_chequear_victoria_jugador1_gana(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        #fichas vacias del jugador1 para hacer como una victoria
        jugador1.set_fichas([])

        self.assertEqual(juego.chequear_victoria(), jugador1)

    def test_chequear_victoria_jugador2_gana(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        #fichas vacias del jugador2 para hacer como una victoria
        jugador2.set_fichas([])
        self.assertEqual(juego.chequear_victoria(), jugador2)

    def test_mover_ficha_con_dado_valido(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # pongo los dados a [5, 3]
        juego._BackgammonGame__ultima_tirada = (5, 3)
        juego._BackgammonGame__dados_disponibles = [5, 3]

        tablero = juego.get_tablero().get_points()
        self.assertEqual(len(tablero[0]), 15)

        # movimiento valido de 0 a 5 (uso el dado 5)
        juego.mover_ficha(jugador1, 0, 5)

        self.assertEqual(len(tablero[0]), 14)
        self.assertEqual(len(tablero[5]), 1)
        self.assertEqual(juego._BackgammonGame__dados_disponibles, [3])

    def test_mover_ficha_con_dado_invalido_lanza_excepcion(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        #pongo los dados a [2, 4]
        juego._BackgammonGame__ultima_tirada = (2, 4)
        juego._BackgammonGame__dados_disponibles = [2, 4]

        # entonces intento mover por ej 5 posiciones (no es valido)
        with self.assertRaises(MovimientoInvalidoException):
            juego.mover_ficha(jugador1, 0, 5)

    def test_captura_ficha_envia_al_bar(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # forzamos dados y disponibles
        juego._BackgammonGame__dados_disponibles = [1]

        # colocamos una ficha negra sola en el punto 1
        ficha_negra = Ficha("negro")
        juego.get_tablero().get_points()[1] = [ficha_negra]

        # jugador blanco mueve de 0 a 1 (distancia = 1)
        juego.mover_ficha(jugador1, 0, 1)

        # la ficha negra debe estar en el bar
        bar = juego.get_bar()
        self.assertIn(ficha_negra, bar["negro"])
        # en el punto 1 ahora debe estar la ficha blanca
        self.assertEqual(juego.get_tablero().get_points()[1][-1].get_color(), "blanco")

    def test_no_captura_si_mas_de_una_ficha_en_destino(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # forzamos dados y disponibles
        juego._BackgammonGame__dados_disponibles = [1]

        # colocamos dos fichas negras en el punto 1
        ficha_negra1 = Ficha("negro")
        ficha_negra2 = Ficha("negro")
        juego.get_tablero().get_points()[1] = [ficha_negra1, ficha_negra2]

        # jugador blanco mueve de 0 a 1 (distancia=1)
        juego.mover_ficha(jugador1, 0, 1)

        # las fichas negras siguen en el tablero (no se capturan)
        self.assertIn(ficha_negra1, juego.get_tablero().get_points()[1])
        self.assertIn(ficha_negra2, juego.get_tablero().get_points()[1])
        
       # bar negro debe estar vacío
        self.assertEqual(len(juego.get_bar()["negro"]), 0)

    def test_reingresar_ficha_valido(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        #forzamos una ficha capturada al bar blanco
        ficha_blanca = juego.get_tablero().get_points()[0].pop()
        juego.get_bar()["blanco"].append(ficha_blanca)

        #seteamos dados disponibles
        juego._BackgammonGame__dados_disponibles = [1]

        # reingreso en punto 0
        juego.reingresar_ficha(jugador1, 0)

        self.assertEqual(len(juego.get_bar()["blanco"]), 0)  # ya no esta en el bar
        self.assertIn(ficha_blanca, juego.get_tablero().get_points()[0])

    def test_reingreso_en_punto_ocupado_por_mas_de_una_ficha_rival(self):
        juego = BackgammonGame()
        jugador1 = Jugador("Guada", "blanco")
        jugador2 = Jugador("Lupita", "negro")
        juego.agregar_jugador(jugador1)
        juego.agregar_jugador(jugador2)
        juego.setup_inicial()

        # agregamos ficha blanca al bar
        ficha_blanca = juego.get_tablero().get_points()[0].pop()
        juego.get_bar()["blanco"].append(ficha_blanca)

        # en punto 0 ponemos dos fichas negras
        juego.get_tablero().get_points()[0] = [Ficha("negro"), Ficha("negro")]

        juego._BackgammonGame__dados_disponibles = [1]

        with self.assertRaises(MovimientoInvalidoException):
            juego.reingresar_ficha(jugador1, 0)

def test_mostrar_estado_inicial(self):
    juego = BackgammonGame()
    jugador1 = Jugador("Zoe", "blanco")
    jugador2 = Jugador("Pili", "negro")
    juego.agregar_jugador(jugador1)
    juego.agregar_jugador(jugador2)
    juego.iniciar_juego()

    estado = juego.mostrar_estado()
    self.assertIn("Turno actual: Zoe", estado)  # arranca jugador1
    self.assertIn("Dados disponibles: []", estado)
    self.assertIn("Bar: {blanco: 0, negro: 0}", estado)
    self.assertIn("Historial (ultimos 5): []", estado)

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

    # captura
    ficha = Ficha("blanco")
    juego.get_bar()["blanco"].append(ficha)
    juego.get_historial().append("Zoe movio una ficha")

    estado = juego.mostrar_estado()
    self.assertIn("Bar: {blanco: 1, negro: 0}", estado)
    self.assertIn("Historial (ultimos 5):", estado)
    self.assertIn("Zoe movio una ficha", estado)

if __name__ == "__main__":
    unittest.main()

