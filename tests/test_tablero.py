 
import unittest
from codigo.tablero import Tablero

class TestTablero(unittest.TestCase):

    def test_tablero_tiene_24_puntos(self):
        tablero = Tablero()
        self.assertEqual(len(tablero._Tablero__points__), 24)

    def test_puntos_inician_vacios(self):
        tablero = Tablero()
        for punto in tablero._Tablero__points__:
            self.assertEqual(punto, [])

if __name__ == "__main__":
    unittest.main()
