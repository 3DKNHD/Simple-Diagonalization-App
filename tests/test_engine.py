import unittest

from sympy import Matrix, Rational, eye, simplify, symbols

from matrix_diagonalization.engine import analyze, parse_matrix, parse_matrix_text
from matrix_diagonalization.exceptions import InvalidMatrixError
from matrix_diagonalization.graphs import to_dot, walk_entries
from matrix_diagonalization.pdf_report import build_pdf_bytes


class EngineTests(unittest.TestCase):
    def test_complete_graph_k3_power(self):
        C = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        result = analyze(C, 3, field="R", mode="graph", compute_exp=False)
        expected = Matrix([[2, 3, 3], [3, 2, 3], [3, 3, 2]])
        self.assertEqual(simplify(result.result_power - expected), Matrix.zeros(3))
        self.assertTrue(result.is_adjacency)
        self.assertEqual(result.status, "diagonalizable")
        self.assertFalse(result.is_directed)

    def test_k3_charpoly(self):
        C = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        result = analyze(C, 1, compute_exp=False)
        lam = symbols("lambda")
        expected = (lam - 2) * (lam + 1) ** 2
        self.assertEqual(simplify(result.charpoly - expected.expand()), 0)

    def test_identity_power(self):
        result = analyze(eye(4), 7, compute_exp=False)
        self.assertEqual(result.result_power, eye(4))

    def test_power_zero_is_identity(self):
        result = analyze([[2, 1], [1, 2]], 0, compute_exp=False)
        self.assertEqual(result.result_power, eye(2))

    def test_weighted_symmetric_matches_direct(self):
        C = Matrix([[2, 1], [1, 2]])
        result = analyze(C, 4, field="R", mode="algebra", compute_exp=False)
        self.assertEqual(simplify(result.result_power - C**4), Matrix.zeros(2))
        self.assertTrue(result.is_symmetric)
        self.assertEqual(result.status, "diagonalizable")
        self.assertTrue(result.uses_p_transpose)
        self.assertEqual(simplify(result.P_inv - result.P.T), Matrix.zeros(2))

    def test_graph_mode_rejects_weights(self):
        with self.assertRaises(InvalidMatrixError):
            analyze([[0, 2], [2, 0]], 2, mode="graph")

    def test_jordan_block_uses_jordan(self):
        result = analyze([[1, 1], [0, 1]], 3, compute_exp=False)
        self.assertEqual(result.status, "jordan")
        self.assertEqual(result.result_power, Matrix([[1, 3], [0, 1]]))
        self.assertIsNotNone(result.jordan_J)
        geo = result.eigenvalues[0].geometric
        alg = result.eigenvalues[0].algebraic
        self.assertLess(geo, alg)

    def test_rotation_complex_over_reals(self):
        result = analyze([[0, -1], [1, 0]], 2, field="R", compute_exp=False)
        self.assertEqual(result.status, "complex_over_R")
        self.assertEqual(result.result_power, Matrix([[-1, 0], [0, -1]]))

    def test_rotation_diagonalizable_over_complex(self):
        result = analyze([[0, -1], [1, 0]], 2, field="C", compute_exp=False)
        self.assertEqual(result.status, "diagonalizable")
        self.assertIsNotNone(result.P)
        self.assertEqual(simplify(result.result_power - Matrix([[-1, 0], [0, -1]])), Matrix.zeros(2))

    def test_negative_power_identity(self):
        result = analyze(eye(2), -1, compute_exp=False)
        self.assertEqual(result.result_power, eye(2))

    def test_negative_power_invertible(self):
        A = Matrix([[2, 1], [1, 2]])
        result = analyze(A, -1, compute_exp=False)
        self.assertEqual(simplify(result.result_power - A.inv()), Matrix.zeros(2))

    def test_negative_power_singular_rejected(self):
        with self.assertRaises(InvalidMatrixError):
            analyze([[1, 0], [0, 0]], -1)

    def test_non_square_rejected(self):
        with self.assertRaises(InvalidMatrixError):
            analyze([[1, 2, 3], [4, 5, 6]], 2)

    def test_parse_rationals(self):
        A = parse_matrix([["1/2", "0"], ["0", "3/2"]])
        self.assertEqual(A[0, 0], Rational(1, 2))
        result = analyze(A, 2, compute_exp=False)
        self.assertEqual(result.result_power[0, 0], Rational(1, 4))

    def test_parse_matrix_text(self):
        A = parse_matrix_text("0 1\n1 0")
        self.assertEqual(A, Matrix([[0, 1], [1, 0]]))

    def test_parse_matrix_text_commas(self):
        A = parse_matrix_text("0, 1; 1, 0")
        self.assertEqual(A, Matrix([[0, 1], [1, 0]]))

    def test_path_p3_walks(self):
        P3 = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
        result = analyze(P3, 2, mode="graph", compute_exp=False)
        expected = Matrix([[1, 0, 1], [0, 2, 0], [1, 0, 1]])
        self.assertEqual(result.result_power, expected)
        walks = { (w.src, w.dst): w.count for w in result.walks }
        self.assertEqual(walks[(1, 1)], 1)
        self.assertEqual(walks[(1, 2)], 0)
        self.assertEqual(walks[(1, 3)], 1)
        self.assertEqual(walks[(2, 2)], 2)
        self.assertEqual(len(result.walks), 9)

    def test_directed_cycle(self):
        A = [[0, 1, 0], [0, 0, 1], [1, 0, 0]]
        result = analyze(A, 1, mode="graph", compute_exp=False)
        self.assertTrue(result.is_directed)
        dot = to_dot(result.matrix, directed=True)
        self.assertIn("digraph", dot)
        self.assertIn("->", dot)

    def test_walk_entries_helper(self):
        entries = walk_entries(Matrix([[2, 0], [0, 2]]))
        self.assertEqual(entries[0].src, 1)
        self.assertEqual(entries[0].count, 2)

    def test_exp_tA_diagonal(self):
        result = analyze([[1, 0], [0, 2]], 1, mode="algebra", compute_exp=True)
        self.assertIsNotNone(result.exp_tA)
        t = symbols("t", real=True)
        from sympy import exp
        self.assertEqual(simplify(result.exp_tA[0, 0] - exp(t)), 0)

    def test_pdf_bytes(self):
        result = analyze([[2, 1], [1, 2]], 2, compute_exp=False)
        data = build_pdf_bytes(result)
        self.assertTrue(data.startswith(b"%PDF"))
        self.assertGreater(len(data), 200)

    def test_systems_for_small_n(self):
        result = analyze([[2, 1], [1, 2]], 1, compute_exp=False)
        self.assertTrue(all(info.system_text for info in result.eigenvalues))


if __name__ == "__main__":
    unittest.main()
