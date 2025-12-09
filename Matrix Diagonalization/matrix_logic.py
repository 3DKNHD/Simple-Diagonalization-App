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
        C = matrix
        size = len(C)
        C_power_direct = np.linalg.matrix_power(C, power) if np.linalg.matrix_power is not None else None

        eigenvalues, eigenvectors = np.linalg.eig(C)
        groups = MatrixCalculator.group_eigenvalues_eigenvectors(eigenvalues, eigenvectors)

        all_eigenvalues = []
        all_eigenvectors = []

        for group in groups:
            eigenvalue = group[0][0]
            for eigenvalue, eigenvector in group:
                all_eigenvalues.append(eigenvalue)
                all_eigenvectors.append(eigenvector)

        P = np.column_stack(all_eigenvectors)
        eigenvalues_array = np.array(all_eigenvalues)
        D = np.diag(eigenvalues_array)
        P_inv = np.linalg.inv(P)
        D_power = np.diag(eigenvalues_array ** power)
        temp = P @ D_power
        C_power = temp @ P_inv

        C_power_rounded = np.round(C_power, 10)
        if np.all(np.abs(C_power_rounded - np.round(C_power_rounded)) < 1e-8):
            C_power_result = np.round(C_power_rounded).astype(int)
        else:
            C_power_result = C_power_rounded

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
            'size': size
        }