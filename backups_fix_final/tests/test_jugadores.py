import unittest
from codigo.jugadores import Jugador
from codigo.fichas import Ficha
from codigo.excepciones import FichaInvalidaException


class TestJugador(unittest.TestCase):

    # ========== TESTS DE CREACIÓN ==========
    def test_crear_jugador(self):
        jugador = Jugador("Guada", "blanco")
        self.assertEqual(jugador.get_nombre(), "Guada")
        self.assertEqual(jugador.get_color(), "blanco")
        self.assertEqual(jugador.cantidad_fichas(), 0)

    def test_crear_jugador_negro(self):
        jugador = Jugador("Lupita", "negro")
        self.assertEqual(jugador.get_nombre(), "Lupita")
        self.assertEqual(jugador.get_color(), "negro")
        self.assertEqual(jugador.cantidad_fichas(), 0)

    def test_crear_jugador_fichas_vacias(self):
        jugador = Jugador("Test", "blanco")
        self.assertEqual(jugador.get_fichas(), [])

    # ========== TESTS DE GETTERS/SETTERS ==========
    def test_set_nombre(self):
        jugador = Jugador("Lupita", "negro")
        jugador.set_nombre("Ana")
        self.assertEqual(jugador.get_nombre(), "Ana")

    def test_set_color(self):
        jugador = Jugador("Lupita", "negro")
        jugador.set_color("blanco")
        self.assertEqual(jugador.get_color(), "blanco")

    def test_setters_multiples_cambios(self):
        jugador = Jugador("Original", "blanco")
        jugador.set_nombre("Cambio1")
        jugador.set_nombre("Cambio2")
        jugador.set_color("negro")
        self.assertEqual(jugador.get_nombre(), "Cambio2")
        self.assertEqual(jugador.get_color(), "negro")

    # ========== TESTS DE AGREGAR FICHAS ==========
    def test_agregar_ficha_valida(self):
        jugador = Jugador("Lupita", "negro")
        ficha = Ficha("negro")
        jugador.agregar_ficha(ficha)
        self.assertEqual(jugador.cantidad_fichas(), 1)
        self.assertEqual(jugador.get_fichas(), [ficha])

    def test_agregar_ficha_valida_blanco(self):
        jugador = Jugador("Guada", "blanco")
        ficha = Ficha("blanco")
        jugador.agregar_ficha(ficha)
        self.assertEqual(jugador.cantidad_fichas(), 1)
        self.assertIn(ficha, jugador.get_fichas())

    def test_agregar_multiples_fichas_validas(self):
        jugador = Jugador("Guada", "blanco")
        ficha1 = Ficha("blanco")
        ficha2 = Ficha("blanco")
        ficha3 = Ficha("blanco")
        jugador.agregar_ficha(ficha1)
        jugador.agregar_ficha(ficha2)
        jugador.agregar_ficha(ficha3)
        self.assertEqual(jugador.cantidad_fichas(), 3)

    def test_agregar_ficha_invalida(self):
        jugador = Jugador("Guada", "blanco")
        ficha = Ficha("negro")
        with self.assertRaises(FichaInvalidaException):
            jugador.agregar_ficha(ficha)

    def test_agregar_ficha_invalida_negro_a_blanco(self):
        jugador = Jugador("Lupita", "negro")
        ficha = Ficha("blanco")
        with self.assertRaises(FichaInvalidaException):
            jugador.agregar_ficha(ficha)

    def test_agregar_ficha_invalida_no_modifica_lista(self):
        jugador = Jugador("Test", "blanco")
        ficha_valida = Ficha("blanco")
        ficha_invalida = Ficha("negro")
        jugador.agregar_ficha(ficha_valida)
        try:
            jugador.agregar_ficha(ficha_invalida)
        except FichaInvalidaException:
            pass
        self.assertEqual(jugador.cantidad_fichas(), 1)

    # ========== TESTS DE SET_FICHAS ==========
    def test_set_fichas(self):
        jugador = Jugador("Guada", "blanco")
        ficha1 = Ficha("blanco")
        ficha2 = Ficha("blanco")
        jugador.set_fichas([ficha1, ficha2])
        self.assertEqual(jugador.get_fichas(), [ficha1, ficha2])
        self.assertEqual(jugador.cantidad_fichas(), 2)

    def test_set_fichas_lista_vacia(self):
        jugador = Jugador("Guada", "blanco")
        jugador.set_fichas([])
        self.assertEqual(jugador.get_fichas(), [])
        self.assertEqual(jugador.cantidad_fichas(), 0)

    def test_set_fichas_reemplaza_lista_anterior(self):
        jugador = Jugador("Test", "negro")
        ficha1 = Ficha("negro")
        jugador.agregar_ficha(ficha1)
        
        ficha2 = Ficha("negro")
        ficha3 = Ficha("negro")
        jugador.set_fichas([ficha2, ficha3])
        
        self.assertEqual(jugador.cantidad_fichas(), 2)
        self.assertNotIn(ficha1, jugador.get_fichas())

    # ========== TESTS DE ELIMINAR FICHAS ==========
    def test_eliminar_ficha(self):
        jugador = Jugador("Lupita", "negro")
        ficha1 = Ficha("negro")
        ficha2 = Ficha("negro")
        jugador.set_fichas([ficha1, ficha2])
        jugador.eliminar_ficha(ficha1)
        self.assertEqual(jugador.get_fichas(), [ficha2])
        self.assertEqual(jugador.cantidad_fichas(), 1)

    def test_eliminar_ultima_ficha(self):
        jugador = Jugador("Test", "blanco")
        ficha = Ficha("blanco")
        jugador.agregar_ficha(ficha)
        jugador.eliminar_ficha(ficha)
        self.assertEqual(jugador.cantidad_fichas(), 0)
        self.assertEqual(jugador.get_fichas(), [])

    def test_eliminar_ficha_por_identidad(self):
        jugador = Jugador("Guada", "blanco")
        ficha1 = Ficha("blanco")
        ficha2 = Ficha("blanco")
        ficha3 = Ficha("blanco")
        jugador.set_fichas([ficha1, ficha2, ficha3])
        
        jugador.eliminar_ficha(ficha2)
        self.assertEqual(jugador.cantidad_fichas(), 2)
        self.assertIn(ficha1, jugador.get_fichas())
        self.assertNotIn(ficha2, jugador.get_fichas())
        self.assertIn(ficha3, jugador.get_fichas())

    def test_eliminar_ficha_por_color_cuando_no_existe_identidad(self):
        """Prueba el caso especial donde se busca por color (branch alternativo)"""
        jugador = Jugador("Test", "negro")
        ficha1 = Ficha("negro")
        ficha2 = Ficha("negro")
        jugador.set_fichas([ficha1, ficha2])
        
        # Creamos una ficha nueva que NO está en la lista por identidad
        ficha_nueva = Ficha("negro")
        jugador.eliminar_ficha(ficha_nueva)
        
        # Debe eliminar la primera ficha del mismo color
        self.assertEqual(jugador.cantidad_fichas(), 1)

    def test_eliminar_ficha_por_color_elimina_primera_coincidencia(self):
        jugador = Jugador("Guada", "blanco")
        ficha1 = Ficha("blanco")
        ficha2 = Ficha("blanco")
        ficha3 = Ficha("blanco")
        jugador.set_fichas([ficha1, ficha2, ficha3])
        
        ficha_nueva = Ficha("blanco")
        jugador.eliminar_ficha(ficha_nueva)
        
        # Debe quedar con 2 fichas (eliminó la primera)
        self.assertEqual(jugador.cantidad_fichas(), 2)

    def test_eliminar_ficha_inexistente(self):
        jugador = Jugador("Guada", "blanco")
        ficha = Ficha("blanco")
        with self.assertRaises(ValueError):
            jugador.eliminar_ficha(ficha)

    def test_eliminar_ficha_color_diferente(self):
        """Test del else en el except ValueError - cuando no encuentra el color"""
        jugador = Jugador("Test", "blanco")
        ficha_blanca = Ficha("blanco")
        jugador.agregar_ficha(ficha_blanca)
        
        # Intentar eliminar ficha negra (color diferente)
        ficha_negra = Ficha("negro")
        with self.assertRaises(ValueError):
            jugador.eliminar_ficha(ficha_negra)

    def test_eliminar_ficha_inexistente_con_otras_fichas(self):
        jugador = Jugador("Lupita", "negro")
        ficha1 = Ficha("negro")
        jugador.agregar_ficha(ficha1)
        
        # Intentar eliminar ficha blanca cuando el jugador tiene solo negras
        ficha_blanca = Ficha("blanco")
        with self.assertRaises(ValueError):
            jugador.eliminar_ficha(ficha_blanca)

    # ========== TESTS DE CANTIDAD_FICHAS ==========
    def test_cantidad_fichas_inicial(self):
        jugador = Jugador("Test", "blanco")
        self.assertEqual(jugador.cantidad_fichas(), 0)

    def test_cantidad_fichas_actualiza_correctamente(self):
        jugador = Jugador("Test", "negro")
        self.assertEqual(jugador.cantidad_fichas(), 0)
        
        jugador.agregar_ficha(Ficha("negro"))
        self.assertEqual(jugador.cantidad_fichas(), 1)
        
        jugador.agregar_ficha(Ficha("negro"))
        self.assertEqual(jugador.cantidad_fichas(), 2)

    # ========== TESTS INTEGRADOS ==========
    def test_operaciones_mixtas(self):
        """Test que combina varias operaciones para mejor cobertura"""
        jugador = Jugador("Player1", "blanco")
        
        # Agregar fichas
        for _ in range(5):
            jugador.agregar_ficha(Ficha("blanco"))
        self.assertEqual(jugador.cantidad_fichas(), 5)
        
        # Cambiar nombre
        jugador.set_nombre("Player2")
        
        # Eliminar algunas fichas
        fichas = jugador.get_fichas()
        jugador.eliminar_ficha(fichas[0])
        jugador.eliminar_ficha(fichas[1])
        
        self.assertEqual(jugador.cantidad_fichas(), 3)
        self.assertEqual(jugador.get_nombre(), "Player2")

    def test_get_fichas_retorna_lista_modificable(self):
        """Verifica que get_fichas retorna la referencia real"""
        jugador = Jugador("Test", "negro")
        ficha = Ficha("negro")
        jugador.agregar_ficha(ficha)
        
        lista1 = jugador.get_fichas()
        lista2 = jugador.get_fichas()
        
        self.assertIs(lista1, lista2)


if __name__ == "__main__":
    unittest.main()
