import unittest
from codigo.excepciones import BackgammonException, MovimientoInvalidoException, FichaInvalidaException

class TestExcepciones(unittest.TestCase):

    def test_backgammon_exception_es_subclase_de_exception(self):
        self.assertTrue(issubclass(BackgammonException, Exception))

    def test_movimiento_invalido_es_subclase_de_backgammon_exception(self):
        self.assertTrue(issubclass(MovimientoInvalidoException, BackgammonException))

    def test_ficha_invalida_es_subclase_de_backgammon_exception(self):
        self.assertTrue(issubclass(FichaInvalidaException, BackgammonException))

    def test_lanzar_movimiento_invalido_exception(self):
        with self.assertRaises(MovimientoInvalidoException):
            raise MovimientoInvalidoException("Movimiento no permitido")

    def test_lanzar_ficha_invalida_exception(self):
        with self.assertRaises(FichaInvalidaException):
            raise FichaInvalidaException("Ficha no valida")


if __name__ == "__main__":
    unittest.main()
