import unittest
from src.ordenacao import METODOS, ordenar, escolher

class TestOrdenacao(unittest.TestCase):
    def test_casos_basicos_em_todos_metodos(self):
        casos = [
            [], [7], [4, 4, 4], [1, 2, 3, 4],
            [4, 3, 2, 1], [-8, 3, -1, 0, -8],
            [5, -2, 100, 0, -100, 5]
        ]
        for nome, metodo in METODOS.items():
            for caso in casos:
                with self.subTest(metodo=nome, caso=caso):
                    self.assertEqual(metodo(caso), sorted(caso))

    def test_escolhedor_e_ordenar(self):
        casos = [[], [1], [3, 1, 2], [0] * 100,
                 list(range(100)), list(range(100, 0, -1)),
                 [-5, 2, -1, 0] * 20]
        for caso in casos:
            self.assertEqual(ordenar(caso), sorted(caso))

    def test_contagem_recusa_faixa_grande(self):
        with self.assertRaises(ValueError):
            METODOS["contagem"]([0, 10**8])

if __name__ == "__main__":
    unittest.main()
