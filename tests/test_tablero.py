import unittest
from codigo.tablero import Tablero
from codigo.fichas import Ficha
from codigo.excepciones import MovimientoInvalidoException


class TestTablero(unittest.TestCase):

    def test_tablero_tiene_24_puntos(self):
        tablero = Tablero()
        self.assertEqual(len(tablero.get_points()), 24)

    def test_puntos_inician_vacios(self):
        tablero = Tablero()
        for punto in tablero.get_points():
            self.assertEqual(punto, [])

    def test_colocar_ficha_valida(self):
        tablero = Tablero()
        ficha = Ficha("blanco")
        tablero.colocar_ficha(0, ficha)
        self.assertEqual(len(tablero.get_points()[0]), 1)

    def test_colocar_ficha_fuera_de_rango(self):
        tablero = Tablero()
        ficha = Ficha("negro")
        with self.assertRaises(ValueError):
            tablero.colocar_ficha(25, ficha)

    def test_colocar_ficha_negativa(self):
        tablero = Tablero()
        ficha = Ficha("blanco")
        with self.assertRaises(ValueError):
            tablero.colocar_ficha(-1, ficha)

    def test_colocar_ficha_en_punto_23(self):
        tablero = Tablero()
        ficha = Ficha("negro")
        tablero.colocar_ficha(23, ficha)
        self.assertEqual(len(tablero.get_points()[23]), 1)

    def test_no_mas_de_15_fichas_en_un_punto(self):
        tablero = Tablero()
        for _ in range(15):
            tablero.colocar_ficha(0, Ficha("blanco"))

        with self.assertRaises(ValueError):
            tablero.colocar_ficha(0, Ficha("blanco"))

    def test_colocar_exactamente_15_fichas(self):
        tablero = Tablero()
        for _ in range(15):
            tablero.colocar_ficha(0, Ficha("blanco"))
        self.assertEqual(len(tablero.get_points()[0]), 15)

    def test_set_points_valido(self):
        tablero = Tablero()
        nuevo_estado = [[] for _ in range(24)]
        tablero.set_points(nuevo_estado)
        self.assertEqual(tablero.get_points(), nuevo_estado)

    def test_set_points_con_fichas(self):
        tablero = Tablero()
        nuevo_estado = [[] for _ in range(24)]
        nuevo_estado[0] = [Ficha("blanco"), Ficha("blanco")]
        nuevo_estado[5] = [Ficha("negro")]
        tablero.set_points(nuevo_estado)
        self.assertEqual(len(tablero.get_points()[0]), 2)
        self.assertEqual(len(tablero.get_points()[5]), 1)

    def test_set_points_invalido(self):
        tablero = Tablero()
        with self.assertRaises(ValueError):
            tablero.set_points([[] for _ in range(10)])

    def test_set_points_mas_de_24(self):
        tablero = Tablero()
        with self.assertRaises(ValueError):
            tablero.set_points([[] for _ in range(30)])

    def test_mover_ficha_valida(self):
        tablero = Tablero()
        ficha = Ficha("blanco")
        tablero.colocar_ficha(0, ficha)
        tablero.mover_ficha(0, 1)
        self.assertEqual(len(tablero.get_points()[0]), 0)
        self.assertEqual(len(tablero.get_points()[1]), 1)

    def test_mover_ficha_mismo_punto(self):
        tablero = Tablero()
        ficha = Ficha("negro")
        tablero.colocar_ficha(5, ficha)
        tablero.mover_ficha(5, 5)
        self.assertEqual(len(tablero.get_points()[5]), 1)

    def test_mover_ficha_origen_vacio(self):
        tablero = Tablero()
        with self.assertRaises(MovimientoInvalidoException):
            tablero.mover_ficha(0, 1)

    def test_mover_ficha_origen_fuera_de_rango_negativo(self):
        tablero = Tablero()
        ficha = Ficha("negro")
        tablero.colocar_ficha(0, ficha)
        with self.assertRaises(MovimientoInvalidoException):
            tablero.mover_ficha(-1, 5)

    def test_mover_ficha_origen_fuera_de_rango_alto(self):
        tablero = Tablero()
        ficha = Ficha("negro")
        tablero.colocar_ficha(0, ficha)
        with self.assertRaises(MovimientoInvalidoException):
            tablero.mover_ficha(24, 5)

    def test_mover_ficha_destino_fuera_de_rango_negativo(self):
        tablero = Tablero()
        ficha = Ficha("blanco")
        tablero.colocar_ficha(0, ficha)
        with self.assertRaises(MovimientoInvalidoException):
            tablero.mover_ficha(0, -1)

    def test_mover_ficha_destino_fuera_de_rango_alto(self):
        tablero = Tablero()
        ficha = Ficha("blanco")
        tablero.colocar_ficha(0, ficha)
        with self.assertRaises(MovimientoInvalidoException):
            tablero.mover_ficha(0, 25)

    def test_mover_ficha_destino_lleno(self):
        tablero = Tablero()
        ficha = Ficha("blanco")
        tablero.colocar_ficha(0, ficha)
        for _ in range(15):
            tablero.colocar_ficha(1, Ficha("negro"))

        with self.assertRaises(MovimientoInvalidoException):
            tablero.mover_ficha(0, 1)

    def test_mover_multiple_fichas_del_mismo_punto(self):
        tablero = Tablero()
        tablero.colocar_ficha(0, Ficha("blanco"))
        tablero.colocar_ficha(0, Ficha("blanco"))
        tablero.colocar_ficha(0, Ficha("blanco"))
        
        tablero.mover_ficha(0, 5)
        self.assertEqual(len(tablero.get_points()[0]), 2)
        self.assertEqual(len(tablero.get_points()[5]), 1)

    def test_mover_ficha_a_punto_con_fichas(self):
        tablero = Tablero()
        tablero.colocar_ficha(0, Ficha("blanco"))
        tablero.colocar_ficha(1, Ficha("negro"))
        tablero.colocar_ficha(1, Ficha("negro"))
        
        tablero.mover_ficha(0, 1)
        self.assertEqual(len(tablero.get_points()[1]), 3)

    def test_obtener_tablero(self):
        tablero = Tablero()
        tablero.colocar_ficha(0, Ficha("blanco"))
        tablero.colocar_ficha(5, Ficha("negro"))
        
        estado = tablero.obtener_tablero()
        self.assertEqual(len(estado), 24)
        self.assertEqual(len(estado[0]), 1)
        self.assertEqual(len(estado[5]), 1)

    def test_obtener_tablero_vacio(self):
        tablero = Tablero()
        estado = tablero.obtener_tablero()
        self.assertEqual(len(estado), 24)
        for punto in estado:
            self.assertEqual(len(punto), 0)

    def test_obtener_tablero_retorna_referencia(self):
        tablero = Tablero()
        estado1 = tablero.obtener_tablero()
        estado2 = tablero.obtener_tablero()
        self.assertIs(estado1, estado2)

    def test_colocar_y_mover_fichas_diferentes_colores(self):
        tablero = Tablero()
        tablero.colocar_ficha(0, Ficha("blanco"))
        tablero.colocar_ficha(1, Ficha("negro"))
        
        tablero.mover_ficha(0, 2)
        tablero.mover_ficha(1, 3)
        
        self.assertEqual(len(tablero.get_points()[2]), 1)
        self.assertEqual(len(tablero.get_points()[3]), 1)
        self.assertEqual(tablero.get_points()[2][0].get_color(), "blanco")
        self.assertEqual(tablero.get_points()[3][0].get_color(), "negro")


if __name__ == "__main__":
    unittest.main()