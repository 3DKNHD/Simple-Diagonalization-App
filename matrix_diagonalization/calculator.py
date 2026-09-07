"""Cálculo de Cⁿ por diagonalización: Cⁿ = P Dⁿ P⁻¹."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from .exceptions import InvalidMatrixError, NotDiagonalizableError

_REAL_TOL = 1e-8
_ZERO_TOL = 1e-10
_RANK_TOL = 1e-8


class MatrixCalculator:
    @staticmethod
    def format_number(value, denom_limit=100):
        if value is None or (isinstance(value, float) and not np.isfinite(value)):
            return str(value)

        imag = float(np.imag(value)) if np.iscomplexobj(value) else 0.0
        real = float(np.real(value))

        if abs(imag) > _REAL_TOL:
            return f"{real:.4f}{imag:+.4f}j"

        if abs(real) < _ZERO_TOL:
            return "0"
        if abs(real - round(real)) < 1e-8:
            return str(int(round(real)))

        frac = Fraction(real).limit_denominator(denom_limit)
        if frac.denominator == 1:
            return str(frac.numerator)
        return f"{frac.numerator}/{frac.denominator}"

    @classmethod
    def format_eigenvalue(cls, eigenvalue):
        return cls.format_number(eigenvalue, denom_limit=20)

    @classmethod
    def format_eigenvector(cls, eigenvector):
        parts = [cls.format_number(component, denom_limit=20) for component in eigenvector]
        return "[" + ", ".join(parts) + "]"

    @classmethod
    def matrix_to_str_fractions(cls, matrix):
        return cls._matrix_to_str(matrix, as_fractions=True)

    @classmethod
    def matrix_to_str(cls, matrix, precision=4):
        return cls._matrix_to_str(matrix, as_fractions=False, precision=precision)

    @classmethod
    def _matrix_to_str(cls, matrix, as_fractions=True, precision=4):
        if matrix is None:
            return "None"

        matrix = np.array(matrix, dtype=float)
        if matrix.size == 0:
            return ""

        matrix = matrix.copy()
        matrix[np.abs(matrix) < _ZERO_TOL] = 0.0

        text_matrix = []
        for row in matrix:
            text_row = []
            for elem in row:
                if as_fractions:
                    text_row.append(cls.format_number(elem, denom_limit=100))
                elif abs(elem - round(elem)) < 1e-10:
                    text_row.append(str(int(round(elem))))
                else:
                    text_row.append(f"{elem:.{precision}f}".rstrip("0").rstrip("."))
            text_matrix.append(text_row)

        col_widths = [
            max(len(text_matrix[i][j]) for i in range(len(text_matrix)))
            for j in range(len(text_matrix[0]))
        ]

        top = "┌ " + "   ".join("─" * w for w in col_widths) + " ┐"
        bottom = "└ " + "   ".join("─" * w for w in col_widths) + " ┘"
        lines = [top]
        for row in text_matrix:
            formatted = "│ " + "   ".join(
                text.rjust(col_widths[i]) for i, text in enumerate(row)
            ) + " │"
            lines.append(formatted)
        lines.append(bottom)
        return "\n".join(lines)

    @staticmethod
    def is_adjacency_matrix(matrix):
        values = np.unique(np.asarray(matrix, dtype=float))
        return np.all(np.isin(np.round(values, 10), [0.0, 1.0])) and np.allclose(
            values, np.round(values)
        )

    @staticmethod
    def is_symmetric(matrix, tol=_REAL_TOL):
        array = np.asarray(matrix, dtype=float)
        return array.ndim == 2 and array.shape[0] == array.shape[1] and np.allclose(
            array, array.T, atol=tol
        )

    @staticmethod
    def simplify_vector(vector):
        v = np.asarray(vector, dtype=float).copy()
        max_idx = int(np.argmax(np.abs(v)))
        if np.abs(v[max_idx]) <= _ZERO_TOL:
            return v

        scaled = v / v[max_idx]
        simplified = np.empty_like(scaled)
        for i, value in enumerate(scaled):
            found = False
            for denom in range(1, 21):
                num = round(value * denom)
                if abs(value - num / denom) < 1e-8:
                    simplified[i] = num / denom
                    found = True
                    break
            if not found:
                if abs(value - round(value)) < 1e-8:
                    simplified[i] = round(value)
                else:
                    return v
        return simplified

    @classmethod
    def simplify_basis(cls, basis):
        columns = [cls.simplify_vector(basis[:, i]) for i in range(basis.shape[1])]
        return np.column_stack(columns) if columns else basis

    @staticmethod
    def nullspace(matrix, tol=_RANK_TOL):
        array = np.asarray(matrix, dtype=float)
        n = array.shape[1]
        _, singular_values, vh = np.linalg.svd(array, full_matrices=True)
        if singular_values.size == 0:
            return n, np.eye(n)

        cutoff = max(tol, tol * float(np.max(singular_values)))
        rank = int(np.sum(singular_values > cutoff))
        dim = n - rank
        basis = vh[rank:, :].T
        return dim, basis

    @staticmethod
    def cluster_eigenvalues(eigenvalues, tol=_REAL_TOL):
        order = np.argsort(np.real(eigenvalues))
        groups = []
        current = None
        for index in order:
            value = eigenvalues[index]
            if current is None or abs(value - current) >= tol:
                groups.append([value])
                current = value
            else:
                groups[-1].append(value)
        return groups

    def calculate_power(self, matrix, power, adjacency_only=False):
        try:
            power = int(power)
        except (TypeError, ValueError) as exc:
            raise InvalidMatrixError("La potencia n debe ser un entero.") from exc

        if power < 0:
            raise InvalidMatrixError("La potencia n debe ser un entero no negativo.")

        C = np.array(matrix, dtype=float)
        if C.ndim != 2 or C.shape[0] != C.shape[1]:
            raise InvalidMatrixError("La matriz debe ser cuadrada.")
        if C.shape[0] < 1:
            raise InvalidMatrixError("La matriz no puede estar vacía.")
        if not np.all(np.isfinite(C)):
            raise InvalidMatrixError("La matriz contiene valores no numéricos.")

        if adjacency_only and not self.is_adjacency_matrix(C):
            raise InvalidMatrixError(
                "Modo adyacencia: solo se admiten entradas 0 y 1 "
                "(grafos no ponderados)."
            )

        size = C.shape[0]
        symmetric = self.is_symmetric(C)
        adjacency = self.is_adjacency_matrix(C)

        if symmetric:
            eigenvalues, _ = np.linalg.eigh(C)
        else:
            eigenvalues, _ = np.linalg.eig(C)

        if np.max(np.abs(np.imag(eigenvalues))) > _REAL_TOL:
            raise NotDiagonalizableError(
                "Algunos autovalores no son reales: la matriz no es diagonalizable sobre ℝ.",
                details={"eigenvalues": eigenvalues},
            )

        eigenvalues = np.real(eigenvalues)
        clusters = self.cluster_eigenvalues(eigenvalues)

        group_pairs = []
        multiplicity_rows = []
        basis_columns = []

        identity = np.eye(size)
        for cluster in clusters:
            lam = float(np.mean(cluster))
            if abs(lam - round(lam)) < 1e-8:
                lam = float(round(lam))
            algebraic = len(cluster)
            geometric, basis = self.nullspace(C - lam * identity)
            multiplicity_rows.append(
                {
                    "eigenvalue": lam,
                    "algebraic": algebraic,
                    "geometric": geometric,
                }
            )
            if geometric < algebraic:
                raise NotDiagonalizableError(
                    "No es diagonalizable: la multiplicidad geométrica es menor que la algebraica "
                    f"para λ = {self.format_eigenvalue(lam)} "
                    f"(alg = {algebraic}, geo = {geometric}).",
                    details={
                        "eigenvalue": lam,
                        "algebraic": algebraic,
                        "geometric": geometric,
                        "multiplicities": multiplicity_rows,
                    },
                )

            take = min(geometric, algebraic)
            chosen = self.simplify_basis(basis[:, :take])
            for col in range(chosen.shape[1]):
                vector = chosen[:, col]
                group_pairs.append((lam, vector))
                basis_columns.append(vector)

        groups = []
        current_lambda = None
        current_group = []
        for lam, vector in group_pairs:
            if current_lambda is None or abs(lam - current_lambda) >= _REAL_TOL:
                if current_group:
                    groups.append(current_group)
                current_group = [(lam, vector)]
                current_lambda = lam
            else:
                current_group.append((lam, vector))
        if current_group:
            groups.append(current_group)

        P = np.column_stack(basis_columns)
        rank_p = int(np.linalg.matrix_rank(P, tol=_RANK_TOL))
        if rank_p < size:
            raise NotDiagonalizableError(
                "No es diagonalizable: no hay una base de ℝⁿ formada por autovectores "
                f"(rango de P = {rank_p} < {size})."
            )

        try:
            P_inv = np.linalg.inv(P)
        except np.linalg.LinAlgError as exc:
            raise NotDiagonalizableError(
                "No es diagonalizable: la matriz de autovectores P no es invertible."
            ) from exc

        eigenvalues_array = np.array([pair[0] for pair in group_pairs], dtype=float)
        D = np.diag(eigenvalues_array)
        if power == 0:
            D_power = np.eye(size)
        else:
            D_power = np.diag(np.power(eigenvalues_array, power))

        C_power = P @ D_power @ P_inv
        reconstruction = P @ D @ P_inv
        residual = float(np.max(np.abs(C - reconstruction)))
        cond_p = float(np.linalg.cond(P))

        C_power_direct = np.linalg.matrix_power(C, power)
        C_power_rounded = np.round(C_power, 10)
        if np.all(np.abs(C_power_rounded - np.round(C_power_rounded)) < 1e-8):
            C_power_result = np.round(C_power_rounded).astype(int)
        else:
            C_power_result = C_power_rounded

        warning = residual > 1e-6 or cond_p > 1e8
        max_abs_direct = float(np.max(np.abs(C_power_direct)))
        if max_abs_direct > _ZERO_TOL:
            rel_error = float(
                np.max(np.abs(C_power.astype(float) - C_power_direct.astype(float)))
                / max_abs_direct
            )
            if rel_error > 1e-5:
                warning = True

        interpretation = self.get_interpretation(
            C_power_result,
            power,
            adjacency=adjacency,
            residual=residual,
            multiplicities=multiplicity_rows,
            symmetric=symmetric,
        )

        return {
            "matrix": C,
            "power": power,
            "eigenvalues_groups": groups,
            "P": P,
            "D": D,
            "P_inv": P_inv,
            "D_power": D_power,
            "result": C_power_result,
            "direct_power": C_power_direct,
            "size": size,
            "warning": warning,
            "interpretation": interpretation,
            "is_adjacency": adjacency,
            "is_symmetric": symmetric,
            "residual": residual,
            "cond_P": cond_p,
            "multiplicities": multiplicity_rows,
        }

    @classmethod
    def get_interpretation(
        cls,
        result_matrix,
        power,
        adjacency=True,
        residual=0.0,
        multiplicities=None,
        symmetric=False,
    ):
        size = len(result_matrix)
        lines = []

        lines.append("COMPROBACIONES NUMÉRICAS:\n")
        lines.append(
            f"• ||C − P D P⁻¹||∞ ≈ {residual:.2e}  "
            "(debe ser ~0 si la diagonalización es correcta).\n"
        )
        if symmetric:
            lines.append(
                "• La matriz es simétrica: es diagonalizable sobre ℝ y admite una base ortogonal.\n"
            )
        if multiplicities:
            lines.append("• Multiplicidades (algebraica vs geométrica):\n")
            for row in multiplicities:
                lines.append(
                    f"    λ = {cls.format_eigenvalue(row['eigenvalue'])}:  "
                    f"alg = {row['algebraic']}, geo = {row['geometric']}\n"
                )
        lines.append("\n")

        if not adjacency:
            lines.append("INTERPRETACIÓN ALGEBRAICA:\n")
            lines.append(
                f"• Cⁿ se obtuvo como P Dⁿ P⁻¹, elevando solo los autovalores a la potencia {power}.\n"
            )
            lines.append(
                "• Este atajo es válido precisamente porque C es diagonalizable.\n"
            )
            return "".join(lines)

        if size > 0:
            diag_value = result_matrix[0, 0]
            diag_str = cls.format_number(diag_value, denom_limit=20)
            lines.append(
                f"• Elemento en la diagonal Cⁿ[1,1] = {diag_str}\n"
                f"  Caminos de longitud {power} desde el vértice 1 hasta sí mismo "
                f"(ciclos de longitud {power}).\n\n"
            )

        if size > 1:
            off_diag_value = result_matrix[0, 1]
            off_diag_str = cls.format_number(off_diag_value, denom_limit=20)
            lines.append(
                f"• Elemento fuera de la diagonal Cⁿ[1,2] = {off_diag_str}\n"
                f"  Caminos de longitud {power} desde el vértice 1 hasta el vértice 2.\n\n"
            )

        lines.append("INFORMACIÓN ADICIONAL PARA GRAFOS:\n")
        lines.append(
            f"• (Cⁿ)ᵢⱼ cuenta los caminos de longitud {power} del vértice i al vértice j.\n"
        )
        lines.append("• Valores altos indican muchas conexiones indirectas entre nodos.\n")
        lines.append("• Los elementos diagonales representan ciclos que regresan al origen.\n")
        return "".join(lines)
