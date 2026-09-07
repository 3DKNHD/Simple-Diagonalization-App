import unittest

import numpy as np

from matrix_diagonalization.calculator import MatrixCalculator
from matrix_diagonalization.exceptions import InvalidMatrixError, NotDiagonalizableError


class CalculatorTests(unittest.TestCase):
    def setUp(self):
        self.calc = MatrixCalculator()

    def test_complete_graph_k3_power(self):
        C = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        result = self.calc.calculate_power(C, 3, adjacency_only=True)
        expected = np.array([[2, 3, 3], [3, 2, 3], [3, 3, 2]])
        np.testing.assert_array_equal(result["result"], expected)
        self.assertTrue(result["is_adjacency"])
        self.assertLess(result["residual"], 1e-8)

    def test_identity_power(self):
        result = self.calc.calculate_power(np.eye(4), 7)
        np.testing.assert_array_almost_equal(result["result"], np.eye(4))

    def test_power_zero_is_identity(self):
        result = self.calc.calculate_power([[2, 1], [1, 2]], 0)
        np.testing.assert_array_almost_equal(result["result"], np.eye(2), decimal=8)

    def test_weighted_symmetric_matches_direct(self):
        C = [[2.0, 1.0], [1.0, 2.0]]
        result = self.calc.calculate_power(C, 4, adjacency_only=False)
        np.testing.assert_allclose(result["result"], np.linalg.matrix_power(C, 4), atol=1e-8)
        self.assertTrue(result["is_symmetric"])

    def test_adjacency_mode_rejects_weights(self):
        with self.assertRaises(InvalidMatrixError):
            self.calc.calculate_power([[0, 2], [2, 0]], 2, adjacency_only=True)

    def test_jordan_block_not_diagonalizable(self):
        with self.assertRaises(NotDiagonalizableError):
            self.calc.calculate_power([[1, 1], [0, 1]], 3)

    def test_rotation_complex_eigenvalues(self):
        with self.assertRaises(NotDiagonalizableError):
            self.calc.calculate_power([[0, -1], [1, 0]], 2)

    def test_negative_power_rejected(self):
        with self.assertRaises(InvalidMatrixError):
            self.calc.calculate_power(np.eye(2), -1)

    def test_non_square_rejected(self):
        with self.assertRaises(InvalidMatrixError):
            self.calc.calculate_power([[1, 2, 3], [4, 5, 6]], 2)


if __name__ == "__main__":
    unittest.main()
