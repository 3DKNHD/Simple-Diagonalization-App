from enum import nonmember

import numpy as np
from fractions import Fraction
import math


class MatrixCalculator:


    @staticmethod
    def find_simple_eigenvectors(eigenvectors, eigenvalues):
        size = eigenvectors.shape[0]
        simple_eigenvectors = eigenvectors.copy()

        for i in range(size):
            v = eigenvectors[:, i]
            max_idx = np.argmax(np.abs(v))
            if np.abs(v[max_idx]) > 1e-10:
                scale_factor = 1.0 / v[max_idx]
                scaled_v = v * scale_factor

                is_simple = True
                for j in range(size):
                    value = scaled_v[j]
                    found = False
                    for denom in range(1, 21):
                        num = round(value * denom)
                        if np.abs(value - num / denom) < 1e-8:
                            scaled_v[j] = num / denom
                            found = True
                            break
                    if not found and np.abs(value - round(value)) < 1e-8:
                        scaled_v[j] = round(value)
                    elif not found:
                        is_simple = False
                        break

                if is_simple:
                    simple_eigenvectors[:, i] = scaled_v

        return simple_eigenvectors

    @staticmethod
    def group_eigenvalues_eigenvectors(eigenvalues, eigenvectors):
        tolerance = 1e-10
        eigenvalues = np.array(eigenvalues)
        eigenvectors = np.array(eigenvectors)

        if np.all(np.abs(eigenvalues.imag) < tolerance):
            eigenvalues = eigenvalues.real
            eigenvectors = eigenvectors.real

        eigenvectors = MatrixCalculator.find_simple_eigenvectors(eigenvectors, eigenvalues)

        pairs = []
        for i in range(len(eigenvalues)):
            pairs.append((eigenvalues[i], eigenvectors[:, i]))

        pairs.sort(key=lambda x: (x[0].real, x[0].imag))

        groups = []
        current_group = []
        current_eigenvalue = None

        for eigenvalue, eigenvector in pairs:
            if current_eigenvalue is None:
                current_group = [(eigenvalue, eigenvector)]
                current_eigenvalue = eigenvalue
            else:
                if abs(eigenvalue - current_eigenvalue) < tolerance:
                    current_group.append((eigenvalue, eigenvector))
                else:
                    groups.append(current_group)
                    current_group = [(eigenvalue, eigenvector)]
                    current_eigenvalue = eigenvalue

        if current_group:
            groups.append(current_group)

        return groups

    @staticmethod
    def format_eigenvalue(eigenvalue):
        if np.abs(eigenvalue.imag) < 1e-10:
            if np.abs(eigenvalue.real - round(eigenvalue.real)) < 1e-10:
                return f"{int(round(eigenvalue.real))}"
            else:
                try:
                    frac = Fraction(eigenvalue.real).limit_denominator(20)
                    if frac.denominator == 1:
                        return f"{frac.numerator}"
                    else:
                        return f"{frac.numerator}/{frac.denominator}"
                except:
                    return f"{eigenvalue.real:.4f}"
        else:
            return f"{eigenvalue:.4f}"

    @staticmethod
    def format_eigenvector(eigenvector):
        size = len(eigenvector)
        formatted = "["

        for j in range(size):
            if j > 0:
                formatted += ", "

            value = eigenvector[j]

            if np.abs(value.imag) > 1e-10:
                formatted += f"{value:.4f}"
            else:
                value_real = value.real

                if np.abs(value_real - round(value_real)) < 1e-8:
                    formatted += f"{int(round(value_real))}"
                else:
                    try:
                        frac = Fraction(value_real).limit_denominator(20)
                        if frac.denominator == 1:
                            formatted += f"{frac.numerator}"
                        else:
                            gcd_val = math.gcd(abs(frac.numerator), frac.denominator)
                            num_simple = frac.numerator // gcd_val
                            denom_simple = frac.denominator // gcd_val
                            if denom_simple == 1:
                                formatted += f"{num_simple}"
                            else:
                                formatted += f"{num_simple}/{denom_simple}"
                    except:
                        formatted += f"{value_real:.4f}"

        formatted += "]"
        return formatted

    @staticmethod
    def matrix_to_str_fractions(matrix):
        if matrix is None:
            return "None"

        matrix = np.array(matrix, dtype=float)
        rows = []
        matrix[np.abs(matrix) < 1e-10] = 0.0

        text_matrix = []
        for row in matrix:
            text_row = []
            for elem in row:
                if abs(elem) < 1e-10:
                    text = "0"
                elif abs(elem - round(elem)) < 1e-8:
                    text = str(int(round(elem)))
                else:
                    try:
                        frac = Fraction(elem).limit_denominator(100)
                        gcd_val = math.gcd(abs(frac.numerator), frac.denominator)
                        num_simple = frac.numerator // gcd_val
                        denom_simple = frac.denominator // gcd_val
                        if denom_simple == 1:
                            text = str(num_simple)
                        else:
                            text = f"{num_simple}/{denom_simple}"
                    except:
                        text = f"{elem:.4f}".rstrip("0").rstrip(".")
                text_row.append(text)
            text_matrix.append(text_row)

        if len(text_matrix) == 0:
            return ""

        col_widths = [
            max(len(text_matrix[i][j]) for i in range(len(text_matrix)))
            for j in range(len(text_matrix[0]))
        ]

        top = "┌ " + "   ".join("─" * w for w in col_widths) + " ┐"
        bottom = "└ " + "   ".join("─" * w for w in col_widths) + " ┘"

        rows.append(top)
        for row in text_matrix:
            formatted = "│ " + "   ".join(
                text.rjust(col_widths[i]) for i, text in enumerate(row)
            ) + " │"
            rows.append(formatted)
        rows.append(bottom)

        return "\n".join(rows)

    @staticmethod
    def matrix_to_str(matrix, precision=4):
        if matrix is None:
            return "None"

        matrix = np.array(matrix, dtype=float)
        rows = []
        matrix[np.abs(matrix) < 1e-10] = 0.0

        text_matrix = []
        for row in matrix:
            text_row = []
            for elem in row:
                if abs(elem - round(elem)) < 1e-10:
                    text = str(int(round(elem)))
                else:
                    text = f"{elem:.{precision}f}".rstrip("0").rstrip(".")
                text_row.append(text)
            text_matrix.append(text_row)

        col_widths = [
            max(len(text_matrix[i][j]) for i in range(len(text_matrix)))
            for j in range(len(text_matrix[0]))
        ]

        top = "┌ " + "   ".join("─" * w for w in col_widths) + " ┐"
        bottom = "└ " + "   ".join("─" * w for w in col_widths) + " ┘"

        rows.append(top)
        for row in text_matrix:
            formatted = "│ " + "   ".join(
                text.rjust(col_widths[i]) for i, text in enumerate(row)
            ) + " │"
            rows.append(formatted)
        rows.append(bottom)

        return "\n".join(rows)

    @staticmethod
    def calculate_power(matrix, power):

        #For This Case I`ll use integers
        #If you want it more general just use float
        C = np.array(matrix, dtype=int)

        C_unique_values = np.unique(C)

        if not set(C_unique_values).issubset({0,1}) or not len(C_unique_values) > 0:
            raise ValueError("Ponderada!")

        size = len(C)
        eigenvalues, eigenvectors = np.linalg.eig(C)

        if not np.all(np.isreal(eigenvalues)):
            raise ValueError("No reales")

        C_power_direct = np.linalg.matrix_power(C, power) if hasattr(np.linalg, 'matrix_power') else None


        groups = MatrixCalculator.group_eigenvalues_eigenvectors(eigenvalues, eigenvectors)

        all_eigenvalues = []
        all_eigenvectors = []

        for group in groups:
            for eigenvalue, eigenvector in group:
                all_eigenvalues.append(eigenvalue)
                all_eigenvectors.append(eigenvector)

        P = np.column_stack(all_eigenvectors)
        eigenvalues_array = np.array(all_eigenvalues)
        D = np.diag(eigenvalues_array)
        P_inv = np.linalg.inv(P)
        D_power = np.diag(eigenvalues_array ** power)
        C_power = P @ D_power @ P_inv

        C_power_rounded = np.round(C_power, 10)
        if np.all(np.abs(C_power_rounded - np.round(C_power_rounded)) < 1e-8):
            C_power_result = np.round(C_power_rounded).astype(int)
        else:
            C_power_result = C_power_rounded

        warning = False
        if C_power_direct is not None:
            C_power_normalized = C_power_result.astype(float)
            C_power_direct_normalized = C_power_direct.astype(float)
            max_abs_direct = np.max(np.abs(C_power_direct_normalized))
            if max_abs_direct > 1e-10:
                rel_error = np.max(np.abs(C_power_normalized - C_power_direct_normalized) / max_abs_direct)
                if rel_error > 1e-5:
                    warning = True

        interpretation = MatrixCalculator.get_interpretation(C_power_result, power)

        return {
            'matrix': C,
            'power': power,
            'eigenvalues_groups': groups,
            'P': P,
            'D': D,
            'P_inv': P_inv,
            'D_power': D_power,
            'result': C_power_result,
            'direct_power': C_power_direct,
            'size': size,
            'warning': warning,
            'interpretation': interpretation
        }

    @staticmethod
    def get_interpretation(result_matrix, power):
        size = len(result_matrix)
        interpretation_lines = []

        if size > 0:
            diag_idx = 0
            diag_value = result_matrix[diag_idx, diag_idx]

            if np.abs(diag_value - round(diag_value)) < 1e-8:
                diag_str = str(int(round(diag_value)))
            else:
                try:
                    frac = Fraction(diag_value).limit_denominator(20)
                    gcd_val = math.gcd(abs(frac.numerator), frac.denominator)
                    num_simple = frac.numerator // gcd_val
                    denom_simple = frac.denominator // gcd_val
                    if denom_simple == 1:
                        diag_str = f"{num_simple}"
                    else:
                        diag_str = f"{num_simple}/{denom_simple}"
                except:
                    diag_str = f"{diag_value:.2f}"

            interpretation_lines.append(
                f"• Elemento en la diagonal Cⁿ[{diag_idx + 1},{diag_idx + 1}] = {diag_str}\n"
                f"  Representa el número de caminos de longitud {power} desde el dispositivo {diag_idx + 1} "
                f"hasta sí mismo (ciclos de longitud {power}).\n\n"
            )

        if size > 1:
            off_diag_row, off_diag_col = 0, 1
            off_diag_value = result_matrix[off_diag_row, off_diag_col]


            if np.abs(off_diag_value - round(off_diag_value)) < 1e-8:
                off_diag_str = str(int(round(off_diag_value)))
            else:
                try:
                    frac = Fraction(off_diag_value).limit_denominator(20)
                    gcd_val = math.gcd(abs(frac.numerator), frac.denominator)
                    num_simple = frac.numerator // gcd_val
                    denom_simple = frac.denominator // gcd_val
                    if denom_simple == 1:
                        off_diag_str = f"{num_simple}"
                    else:
                        off_diag_str = f"{num_simple}/{denom_simple}"
                except:
                    off_diag_str = f"{off_diag_value:.2f}"

            interpretation_lines.append(
                f"• Elemento fuera de la diagonal Cⁿ[{off_diag_row + 1},{off_diag_col + 1}] = {off_diag_str}\n"
                f"  Representa el número de caminos de longitud {power} desde el dispositivo {off_diag_row + 1} "
                f"hasta el dispositivo {off_diag_col + 1}.\n\n"
            )

        interpretation_lines.append("INFORMACIÓN ADICIONAL PARA ANÁLISIS DE REDES:\n")
        interpretation_lines.append(
            f"• La matriz Cⁿ muestra todos los caminos de longitud {power} entre dispositivos.\n")
        interpretation_lines.append("• Valores altos indican muchas conexiones indirectas entre nodos.\n")
        interpretation_lines.append("• Una red está mejor conectada si hay múltiples caminos entre nodos.\n")
        interpretation_lines.append("• Los elementos diagonales representan ciclos (caminos que regresan al origen).\n")

        return "".join(interpretation_lines)