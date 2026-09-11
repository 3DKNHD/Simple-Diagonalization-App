"""Resultados del análisis de diagonalización."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

from sympy import Expr, Matrix

Status = Literal["diagonalizable", "jordan", "complex_over_R"]
Field = Literal["R", "C"]
Mode = Literal["algebra", "graph"]


@dataclass
class EigenInfo:
    value: Expr
    algebraic: int
    geometric: int
    basis: list
    system_latex: Optional[str] = None
    system_text: Optional[str] = None


@dataclass
class WalkEntry:
    src: int
    dst: int
    count: Expr


@dataclass
class CalculationResult:
    matrix: Matrix
    power: int
    field: Field
    mode: Mode
    status: Status
    charpoly: Expr
    eigenvalues: list
    is_symmetric: bool
    is_orthogonal_diag: bool
    uses_p_transpose: bool
    P: Optional[Matrix] = None
    D: Optional[Matrix] = None
    P_inv: Optional[Matrix] = None
    D_power: Optional[Matrix] = None
    jordan_P: Optional[Matrix] = None
    jordan_J: Optional[Matrix] = None
    jordan_J_power: Optional[Matrix] = None
    result_power: Optional[Matrix] = None
    exp_tA: Optional[Matrix] = None
    messages: list = field(default_factory=list)
    is_adjacency: bool = False
    is_directed: bool = False
    walks: list = field(default_factory=list)
    det: Optional[Expr] = None
    charpoly_symbol: str = "lambda"
