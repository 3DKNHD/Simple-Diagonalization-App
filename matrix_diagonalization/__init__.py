"""Diagonalización de matrices y cálculo de potencias Cⁿ = P Dⁿ P⁻¹."""

from .calculator import MatrixCalculator
from .exceptions import InvalidMatrixError, MatrixError, NotDiagonalizableError

__all__ = [
    "MatrixCalculator",
    "MatrixError",
    "InvalidMatrixError",
    "NotDiagonalizableError",
]
