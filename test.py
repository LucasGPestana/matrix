import unittest
from matrix import Matrix

class TestMatrix(unittest.TestCase):

    def setUp(self):

        self.matrix = Matrix([[8/10, -1/10], [-1/10, 4/10]])

    def test_inverse(self):

        self.assertTrue([[round(elem, 2) for elem in line]
                         for line in self.matrix.inverse],
                        [[1.29, 0.32],
                         [0.32, 2.58]])

    def test_product(self):

        self.assertTrue([[round(elem, 2) for elem in line]
                         for line in Matrix(self.matrix.inverse).product([[5], [1]])],
                        [[6.77],
                         [4.19]])

if __name__ == "__main__":

    unittest.main()
