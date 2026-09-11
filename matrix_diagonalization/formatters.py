"""Impresión exacta (LaTeX / texto). Nunca inventa fracciones desde floats."""

from __future__ import annotations

from sympy import Eq, Matrix, eye, latex, pretty, simplify, symbols

from .models import CalculationResult, EigenInfo


def expr_str(expr) -> str:
    return str(simplify(expr))


def expr_latex(expr) -> str:
    return latex(simplify(expr))


def matrix_ascii(matrix: Matrix) -> str:
    return pretty(simplify(matrix), use_unicode=True)


def matrix_latex(matrix: Matrix) -> str:
    return latex(simplify(matrix))


def eigen_system(A: Matrix, lam) -> tuple[str, str]:
    """Texto y LaTeX de (A − λI)x = 0."""
    n = A.rows
    xs = symbols(f"x1:{n + 1}")
    m = simplify(A - lam * eye(n))
    prod = m * Matrix(xs)
    eqs = [Eq(simplify(prod[i]), 0) for i in range(n)]
    text_lines = [str(eq) for eq in eqs]
    return "\n".join(text_lines), latex(eqs)


def charpoly_latex(result: CalculationResult) -> str:
    return rf"p(\lambda) = \det(\lambda I - A) = {expr_latex(result.charpoly)}"


def format_eigenvalue_block(info: EigenInfo) -> str:
    lines = [
        f"λ = {expr_str(info.value)}",
        f"  multiplicidad algebraica  alg = {info.algebraic}",
        f"  multiplicidad geométrica  geo = {info.geometric}",
    ]
    for i, vec in enumerate(info.basis, start=1):
        cols = [expr_str(vec[j]) for j in range(vec.rows)]
        lines.append(f"  autovector {i}: [{', '.join(cols)}]")
    if info.system_text:
        lines.append("  sistema (A − λI)x = 0:")
        for row in info.system_text.splitlines():
            lines.append(f"    {row}")
    return "\n".join(lines)


def format_walks(result: CalculationResult) -> str:
    if not result.walks:
        return ""
    n = result.power
    lines = [f"Recorridos de longitud {n} (no necesariamente caminos simples):"]
    for walk in result.walks:
        lines.append(
            f"  {walk.src} → {walk.dst}: {expr_str(walk.count)} recorrido(s)"
        )
    return "\n".join(lines)
