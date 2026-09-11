"""Errores de validación y diagonalización."""


class MatrixError(Exception):
    """Error genérico de cálculo matricial."""


class InvalidMatrixError(MatrixError):
    """La matriz de entrada no cumple las hipótesis pedidas."""


class NotDiagonalizableError(MatrixError):
    """La matriz no es diagonalizable sobre los reales."""

    def __init__(self, message, details=None):
        super().__init__(message)
        self.details = details or {}
