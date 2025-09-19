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

    def test_no_mas_de_15_fichas_en_un_punto(self):
        tablero = Tablero()
        for _ in range(15):
            tablero.colocar_ficha(0, Ficha("blanco"))

        with self.assertRaises(ValueError):
            tablero.colocar_ficha(0, Ficha("blanco"))

    def test_set_points_valido(self):
        tablero = Tablero()
        nuevo_estado = [[] for _ in range(24)]
        tablero.set_points(nuevo_estado)
        self.assertEqual(tablero.get_points(), nuevo_estado)

    def test_set_points_invalido(self):
        tablero = Tablero()
        with self.assertRaises(ValueError):
            tablero.set_points([[] for _ in range(10)])  # menos de 24

    def test_mover_ficha_valida(self):
        tablero = Tablero()
        ficha = Ficha("blanco")
        tablero.colocar_ficha(0, ficha)
        tablero.mover_ficha(0, 1)
        self.assertEqual(len(tablero.get_points()[0]), 0)
        self.assertEqual(len(tablero.get_points()[1]), 1)

    def test_mover_ficha_origen_vacio(self):
        tablero = Tablero()
        with self.assertRaises(MovimientoInvalidoException):
            tablero.mover_ficha(0, 1)

    def test_mover_ficha_fuera_de_rango(self):
        tablero = Tablero()
        ficha = Ficha("negro")
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


if __name__ == "__main__":
    unittest.main()