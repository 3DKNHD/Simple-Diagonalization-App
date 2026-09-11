"""Diagonalización exacta de matrices (sympy) y potencia Aⁿ."""

from .engine import analyze, parse_matrix, parse_matrix_text
from .exceptions import InvalidMatrixError, MatrixError
from .models import CalculationResult

__all__ = [
    "analyze",
    "parse_matrix",
    "parse_matrix_text",
    "CalculationResult",
    "MatrixError",
    "InvalidMatrixError",
]
