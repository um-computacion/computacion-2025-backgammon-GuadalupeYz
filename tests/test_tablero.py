import unittest
from codigo.tablero import Tablero
from codigo.fichas import Ficha

class TestTablero(unittest.TestCase):

    def test_tablero_tiene_24_puntos(self):
        tablero = Tablero()
        self.assertEqual(len(tablero.get_points()), 24)

    def test_puntos_inician_vacios(self):
        tablero = Tablero()
        for punto in tablero.get_points():
            self.assertEqual(punto, [])

    def test_colocar_ficha(self):
        tablero = Tablero()
        ficha = Ficha("blanco")
        tablero.colocar_ficha(0, ficha)
        self.assertIn(ficha, tablero.get_points()[0])

    def test_colocar_ficha_fuera_de_rango(self):
        tablero = Tablero()
        ficha = Ficha("negro")
        with self.assertRaises(ValueError):
            tablero.colocar_ficha(25, ficha)

if __name__ == "__main__":
    unittest.main()
