import unittest
from codigo.fichas import Ficha

class TestFicha(unittest.TestCase):

    def test_crear_ficha(self):
        ficha = Ficha("blanco")
        self.assertEqual(ficha.get_color(), "blanco")

    def test_ficha_color_diferente(self):
        ficha = Ficha("negro")
        self.assertEqual(ficha.get_color(), "negro")

    def test_cambiar_color(self):
        ficha = Ficha("blanco")
        ficha.set_color("negro")
        self.assertEqual(ficha.get_color(), "negro")

if __name__ == "__main__":
    unittest.main()


