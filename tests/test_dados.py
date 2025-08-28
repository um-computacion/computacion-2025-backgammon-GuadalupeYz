import unittest
from codigo.dados import Dados

class TestDados(unittest.TestCase):

    def test_roll_devuelve_tupla(self):
        dados = Dados()
        tirada = dados.roll()
        self.assertIsInstance(tirada, tuple)
        self.assertEqual(len(tirada), 2)

    def test_valores_dados_entre_1_y_6(self):
        dados = Dados()
        tirada = dados.roll()
        for valor in tirada:
            self.assertGreaterEqual(valor, 1)
            self.assertLessEqual(valor, 6)

if __name__ == "__main__":
    unittest.main()
