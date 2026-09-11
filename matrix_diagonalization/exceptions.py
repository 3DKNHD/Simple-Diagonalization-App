"""Errores de validación."""


class MatrixError(Exception):
    """Error genérico de cálculo matricial."""


class InvalidMatrixError(MatrixError):
    """La matriz de entrada no cumple las hipótesis pedidas."""
