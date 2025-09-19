import unittest
from cli.cli import CLI

class TestCLI(unittest.TestCase):
    def test_set_get_opcion(self):
        cli = CLI()
        cli.set_opcion("1")
        self.assertEqual(cli.get_opcion(), "1")

if __name__ == "__main__":
    unittest.main()
