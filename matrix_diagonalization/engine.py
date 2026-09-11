"""Motor exacto de diagonalización, Jordan, potencias y e^{tA} (sympy)."""

from __future__ import annotations

from typing import Iterable, Sequence, Union

from sympy import (
    Matrix,
    diag,
    eye,
    exp,
    factorial,
    im,
    nsimplify,
    simplify,
    symbols,
    sympify,
    zeros,
)
from sympy.core.sympify import SympifyError

from .exceptions import InvalidMatrixError
from .formatters import eigen_system
from .graphs import walk_entries
from .models import CalculationResult, EigenInfo

RawMatrix = Union[Matrix, Sequence[Sequence[Union[str, int, float]]]]


def parse_entry(raw) -> object:
    text = str(raw).strip()
    if text == "":
        raise InvalidMatrixError("Hay una entrada vacía en la matriz.")
    text = text.replace(" ", "").replace(",", ".")
    try:
        value = sympify(text, rational=True, evaluate=True)
    except (SympifyError, SyntaxError, TypeError, ValueError) as exc:
        raise InvalidMatrixError(f"No pude leer la entrada «{raw}».") from exc
    if getattr(value, "free_symbols", None):
        raise InvalidMatrixError(f"La entrada «{raw}» no es un número.")
    if getattr(value, "is_infinite", False):
        raise InvalidMatrixError("La matriz contiene valores no finitos.")
    return nsimplify(value, rational=True)


def parse_matrix(data: RawMatrix) -> Matrix:
    if isinstance(data, Matrix):
        A = data
    else:
        rows = [[parse_entry(value) for value in row] for row in data]
        if not rows:
            raise InvalidMatrixError("La matriz no puede estar vacía.")
        width = len(rows[0])
        if any(len(row) != width for row in rows):
            raise InvalidMatrixError("Todas las filas deben tener la misma longitud.")
        A = Matrix(rows)
    if A.rows != A.cols:
        raise InvalidMatrixError("La matriz debe ser cuadrada.")
    if A.rows < 1:
        raise InvalidMatrixError("La matriz no puede estar vacía.")
    return A


def parse_matrix_text(text: str) -> Matrix:
    raw = text.strip()
    if not raw:
        raise InvalidMatrixError("No hay ninguna fila que leer.")
    chunks = []
    for line in raw.replace(";", "\n").splitlines():
        line = line.strip()
        if line:
            chunks.append(line)
    if not chunks:
        raise InvalidMatrixError("No hay ninguna fila que leer.")
    rows = []
    for line in chunks:
        parts = [p for p in line.replace("|", " ").replace(",", " ").split() if p]
        if parts:
            rows.append(parts)
    if not rows:
        raise InvalidMatrixError("No hay ninguna fila que leer.")
    return parse_matrix(rows)


def is_adjacency_matrix(A: Matrix) -> bool:
    allowed = {0, 1}
    return all(A[i, j] in allowed for i in range(A.rows) for j in range(A.cols))


def is_real_number(value) -> bool:
    value = simplify(value)
    if value.is_real is True:
        return True
    if value.is_real is False:
        return False
    return simplify(im(value)) == 0


def _sort_eigenvals(pairs: Iterable[tuple]) -> list:
    def key(item):
        val = item[0]
        try:
            return (0, float(val.evalf().as_real_imag()[0]))
        except Exception:
            return (1, str(val))

    return sorted(pairs, key=key)


def _orthonormal_eigenbasis(A: Matrix) -> tuple[Matrix, Matrix]:
    cols = []
    vals = []
    for val, _alg, vects in A.eigenvects():
        try:
            orth = Matrix.orthogonalize(*vects, normalize=True)
        except Exception:
            orth = vects
        if not isinstance(orth, (list, tuple)):
            orth = [orth]
        for vec in orth:
            cols.append(Matrix(vec))
            vals.append(val)
    if not cols:
        raise InvalidMatrixError("No se encontraron autovectores.")
    P = Matrix.hstack(*cols)
    D = diag(*vals)
    return simplify(P), simplify(D)


def _matrices_equal(left: Matrix, right: Matrix) -> bool:
    return simplify(left - right) == zeros(*left.shape)


def _power_diagonal(D: Matrix, power: int) -> Matrix:
    n = D.rows
    if power == 0:
        return eye(n)
    entries = []
    for i in range(n):
        lam = D[i, i]
        if lam == 0 and power < 0:
            raise InvalidMatrixError(
                "No se puede calcular Dⁿ: hay un autovalor 0 y n es negativo."
            )
        entries.append(lam**power)
    return diag(*entries)


def _jordan_blocks(J: Matrix) -> list[tuple[object, int]]:
    blocks = []
    i = 0
    n = J.rows
    while i < n:
        lam = J[i, i]
        size = 1
        while (
            i + size < n
            and J[i + size, i + size] == lam
            and J[i + size - 1, i + size] == 1
        ):
            size += 1
        blocks.append((lam, size))
        i += size
    return blocks


def _exp_jordan_block(lam, size, t) -> Matrix:
    nil = zeros(size)
    for i in range(size - 1):
        nil[i, i + 1] = 1
    acc = zeros(size)
    nil_k = eye(size)
    for k in range(size):
        acc += (t**k / factorial(k)) * nil_k
        nil_k = nil_k * nil
    return exp(lam * t) * acc


def _exp_jordan_matrix(J: Matrix, t) -> Matrix:
    n = J.rows
    out = zeros(n)
    row = 0
    for lam, size in _jordan_blocks(J):
        block = _exp_jordan_block(lam, size, t)
        out[row : row + size, row : row + size] = block
        row += size
    return out


def _exp_tA(A: Matrix, P=None, D=None, P_inv=None, jordan_P=None, jordan_J=None):
    t = symbols("t", real=True)
    if P is not None and D is not None and P_inv is not None:
        exp_d = diag(*[exp(t * D[i, i]) for i in range(D.rows)])
        return simplify(P * exp_d * P_inv)
    if jordan_P is None or jordan_J is None:
        jordan_P, jordan_J = A.jordan_form()
    exp_j = _exp_jordan_matrix(jordan_J, t)
    return simplify(jordan_P * exp_j * jordan_P.inv())


def _eigen_infos(A: Matrix, write_systems: bool) -> list[EigenInfo]:
    infos = []
    for val, alg, vects in _sort_eigenvals(A.eigenvects()):
        basis = [Matrix(vec) for vec in vects]
        geo = len(basis)
        system_text = system_latex = None
        if write_systems:
            system_text, system_latex = eigen_system(A, val)
        infos.append(
            EigenInfo(
                value=simplify(val),
                algebraic=int(alg),
                geometric=geo,
                basis=basis,
                system_latex=system_latex,
                system_text=system_text,
            )
        )
    return infos


def analyze(
    matrix: RawMatrix,
    power: int = 1,
    field: str = "R",
    mode: str = "algebra",
    compute_exp: bool = True,
) -> CalculationResult:
    if field not in {"R", "C"}:
        raise InvalidMatrixError("El cuerpo debe ser ℝ o ℂ.")
    if mode not in {"algebra", "graph"}:
        raise InvalidMatrixError("El modo debe ser algebra o graph.")

    try:
        power = int(power)
    except (TypeError, ValueError) as exc:
        raise InvalidMatrixError("La potencia n debe ser un entero.") from exc

    A = parse_matrix(matrix)
    adjacency = is_adjacency_matrix(A)
    if mode == "graph" and not adjacency:
        raise InvalidMatrixError(
            "Modo grafo: solo se admiten entradas 0 y 1 (grafos no ponderados)."
        )

    det = simplify(A.det())
    if power < 0 and det == 0:
        raise InvalidMatrixError(
            "n es negativo y det(A) = 0: A no es invertible, Aⁿ no existe."
        )

    lam = symbols("lambda")
    charpoly = simplify(A.charpoly(lam).as_expr())
    symmetric = A == A.T
    directed = A != A.T
    infos = _eigen_infos(A, write_systems=A.rows <= 4)
    complex_eigs = [info for info in infos if not is_real_number(info.value)]
    defective = any(info.geometric < info.algebraic for info in infos)

    messages = []
    status = "diagonalizable"
    if field == "R" and complex_eigs:
        status = "complex_over_R"
        messages.append(
            "Hay autovalores complejos: A no es diagonalizable sobre ℝ. "
            "Cambia el cuerpo a ℂ para diagonalizarla (si es posible)."
        )
    elif defective:
        status = "jordan"
        messages.append(
            "No es diagonalizable: alguna multiplicidad geométrica es menor "
            "que la algebraica. Se usa la forma de Jordan para Aⁿ."
        )

    P = D = P_inv = D_power = None
    jordan_P = jordan_J = jordan_J_power = None
    uses_p_transpose = False
    is_orthogonal_diag = False
    result_power = simplify(A**power)

    if status == "diagonalizable":
        if symmetric and field == "R" and not complex_eigs:
            P, D = _orthonormal_eigenbasis(A)
            P_inv = simplify(P.T)
            if _matrices_equal(P.T * P, eye(A.rows)):
                uses_p_transpose = True
                is_orthogonal_diag = True
                messages.append(
                    "A es simétrica real: se diagonaliza con P ortogonal y P⁻¹ = Pᵀ."
                )
            else:
                P_inv = simplify(P.inv())
        else:
            P, D = A.diagonalize()
            P, D = simplify(P), simplify(D)
            P_inv = simplify(P.inv())
            if _matrices_equal(P_inv, P.T):
                uses_p_transpose = True
                is_orthogonal_diag = True

        D_power = _power_diagonal(D, power)
        result_power = simplify(P * D_power * P_inv)

    elif status == "jordan":
        jordan_P, jordan_J = A.jordan_form()
        jordan_P, jordan_J = simplify(jordan_P), simplify(jordan_J)
        jordan_J_power = simplify(jordan_J**power)
        result_power = simplify(jordan_P * jordan_J_power * jordan_P.inv())

    elif status == "complex_over_R":
        jordan_P, jordan_J = A.jordan_form()
        jordan_P, jordan_J = simplify(jordan_P), simplify(jordan_J)
        if A.is_diagonalizable():
            messages.append(
                "Sobre ℂ sí es diagonalizable. La forma de Jordan que se muestra "
                "es, en este caso, diagonal compleja."
            )

    exp_tA = None
    if compute_exp and mode == "algebra":
        try:
            exp_tA = _exp_tA(
                A,
                P=P,
                D=D,
                P_inv=P_inv,
                jordan_P=jordan_P,
                jordan_J=jordan_J,
            )
        except Exception:
            exp_tA = None
            messages.append("No se pudo construir e^{tA} de forma cerrada.")

    walks = walk_entries(result_power) if mode == "graph" else []

    return CalculationResult(
        matrix=A,
        power=power,
        field=field,
        mode=mode,
        status=status,
        charpoly=charpoly,
        eigenvalues=infos,
        is_symmetric=bool(symmetric),
        is_orthogonal_diag=is_orthogonal_diag,
        uses_p_transpose=uses_p_transpose,
        P=P,
        D=D,
        P_inv=P_inv,
        D_power=D_power,
        jordan_P=jordan_P,
        jordan_J=jordan_J,
        jordan_J_power=jordan_J_power,
        result_power=result_power,
        exp_tA=exp_tA,
        messages=messages,
        is_adjacency=adjacency,
        is_directed=bool(directed),
        walks=walks,
        det=det,
    )
