import unittest
from codigo.fichas import Ficha

class TestFicha(unittest.TestCase):

    def test_crear_ficha(self):
        ficha = Ficha("blanco")
        self.assertEqual(ficha.obtener_color(), "blanco")

    def test_ficha_color_diferente(self):
        ficha = Ficha("negro")
        self.assertEqual(ficha.obtener_color(), "negro")

if __name__ == "__main__":
    unittest.main()
