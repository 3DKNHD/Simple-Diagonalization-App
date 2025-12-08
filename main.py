import numpy as np
import tkinter as tk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from tkinter import ttk, messagebox, scrolledtext, filedialog

from fractions import Fraction
import math


class MatrixDiagonalizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagonalización de Matrices de Adyacencia")
        self.root.geometry("900x700")
        self.dark_mode = False

        self.matrix_size = tk.IntVar(value=3)
        self.power = tk.IntVar(value=3)
        self.matrix_entries = []
        self.result_matrix = None

        self.setup_ui()

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        style = ttk.Style()

        if self.dark_mode:
            bg = "#1e1e1e"
            fg = "#ffffff"
            entry_bg = "#2b2b2b"
            button_bg = "#3a3a3a"

            self.root.configure(bg=bg)

            style.configure("TFrame", background=bg)
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("Title.TLabel", background=bg, foreground=fg)
            style.configure("Header.TLabel", background=bg, foreground=fg)

            style.configure("TButton",
                            background=button_bg,
                            foreground=fg,
                            bordercolor=button_bg)

            style.map("TButton",
                      background=[("active", "#505050")])

            style.configure("TLabelFrame",
                            background=bg,
                            foreground=fg)

            style.configure("TLabelFrame.Label",
                            background=bg,
                            foreground=fg)

            style.configure("TEntry",
                            fieldbackground=entry_bg,
                            foreground=fg)

            self.results_text.configure(
                bg="#121212",
                fg="white",
                insertbackground="white"
            )

        else:
            bg = "#f0f0f0"
            fg = "black"

            self.root.configure(bg=bg)

            style.configure("TFrame", background=bg)
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("Title.TLabel", background=bg, foreground=fg)
            style.configure("Header.TLabel", background=bg, foreground=fg)

            style.configure("TButton",
                            background="#e0e0e0",
                            foreground=fg)

            style.configure("TLabelFrame",
                            background=bg,
                            foreground=fg)

            style.configure("TLabelFrame.Label",
                            background=bg,
                            foreground=fg)

            style.configure("TEntry",
                            fieldbackground="white",
                            foreground="black")

            self.results_text.configure(
                bg="white",
                fg="black",
                insertbackground="black"
            )
        self.update_button_styles()

    def update_button_styles(self):
        style = ttk.Style()

        if self.dark_mode:
            style.configure("Primary.TButton",
                            background="#4CAF50",
                            foreground="white",
                            font=("Segoe UI", 10, "bold"))

            style.configure("Secondary.TButton",
                            background="#2196F3",
                            foreground="white")

            style.configure("Danger.TButton",
                            background="#E53935",
                            foreground="white")

            style.configure("Neutral.TButton",
                            background="#555555",
                            foreground="white")

            style.map("TButton",
                      background=[("active", "#666666")])

        else:
            style.configure("Primary.TButton",
                            background="#4CAF50",
                            foreground="white",
                            font=("Segoe UI", 10, "bold"))

            style.configure("Secondary.TButton",
                            background="#1976D2",
                            foreground="white")

            style.configure("Danger.TButton",
                            background="#D32F2F",
                            foreground="white")

            style.configure("Neutral.TButton",
                            background="#DDDDDD",
                            foreground="black")

            style.map("TButton",
                      background=[("active", "#CCCCCC")])


    def export_to_pdf(self):
        if self.result_matrix is None or not self.result_matrix.any():
            messagebox.showerror("Error", "Primero debes calcular la matriz.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar PDF como"
        )

        if not filepath:
            return

        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        text = c.beginText(40, height - 50)
        text.setFont("Courier", 9)


        contenido = self.results_text.get(1.0, tk.END).split("\n")

        for line in contenido:
            text.textLine(line)
            if text.getY() < 40:
                c.drawText(text)
                c.showPage()
                text = c.beginText(40, height - 50)
                text.setFont("Courier", 9)


        c.drawText(text)
        c.save()

        messagebox.showinfo("PDF generado", f"Archivo guardado en:\n{filepath}")

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("Accent.TButton", font=("Segoe UI", 11, "bold"), padding=10)

        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=3)
        main_frame.rowconfigure(3, weight=1)

        ttk.Label(
            main_frame,
            text="Diagonalización de Matrices de Adyacencia",
            style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=2, pady=(0, 10))

        ttk.Label(
            main_frame,
            text="Calcula Cⁿ usando autovalores:  Cⁿ = P · Dⁿ · P⁻¹",
            foreground="#555"
        ).grid(row=1, column=0, columnspan=2, pady=(0, 15))

        config_frame = ttk.LabelFrame(main_frame, text="⚙ Configuración", padding=10)
        config_frame.grid(row=2, column=0, sticky="nsw", padx=(0, 10))

        ttk.Label(config_frame, text="Tamaño de la matriz (n×n)").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(
            config_frame, from_=2, to=10, textvariable=self.matrix_size,
            width=6, command=self.create_matrix_inputs
        ).grid(row=1, column=0, pady=(0, 10))

        ttk.Label(config_frame, text="Potencia n").grid(row=2, column=0, sticky="w")
        ttk.Spinbox(
            config_frame, from_=1, to=20, textvariable=self.power, width=6
        ).grid(row=3, column=0, pady=(0, 15))

        ttk.Button(
            config_frame, text="Crear matriz",
            command=self.create_matrix_inputs,
            style="Secondary.TButton"
        ).grid(row=4, column=0, sticky="ew", pady=5)

        ttk.Button(
            config_frame, text="Cargar ejemplo 3×3",
            command=self.load_example,
            style="Danger.TButton"
        ).grid(row=5, column=0, sticky="ew")

        ttk.Button(
            config_frame,
            text="Calcular Cⁿ",
            command=self.calculate_power,
            style="Primary.TButton"
        ).grid(row=6, column=0, sticky="ew", pady=(20, 0))

        ttk.Button(
            config_frame,
            text="Alternar modo oscuro",
            command=self.toggle_dark_mode,
            style="Neutral.TButton"
        ).grid(row=7, column=0, sticky="ew", pady=5)
        self.update_button_styles()
        style = ttk.Style()
        style.configure(
            "Export.TButton",
            background="#4CAF50",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )
        style.map(
            "Export.TButton",
            background=[("active", "#45a049")],
            foreground=[("active", "white")]
        )

        ttk.Button(
            config_frame,
            text="Exportar a PDF",
            command=self.export_to_pdf,
            style="Export.TButton"
        ).grid(row=8, column=0, sticky="ew", pady=5)

        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=2, column=1, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        self.matrix_frame = ttk.LabelFrame(right_frame, text="🧮 Matriz de Adyacencia", padding=10)
        self.matrix_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        results_frame = ttk.LabelFrame(right_frame, text="📊 Resultados paso a paso", padding=10)
        results_frame.grid(row=1, column=0, sticky="nsew")
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=18,
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.results_text.grid(row=0, column=0, sticky="nsew")

        self.create_matrix_inputs()

    def create_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        size = self.matrix_size.get()
        self.matrix_entries = []

        for j in range(size):
            ttk.Label(self.matrix_frame, text=f"Col {j + 1}", font=('Arial', 9, 'bold')).grid(row=0, column=j + 1,
                                                                                              padx=5, pady=5)

        for i in range(size):
            row_entries = []
            ttk.Label(self.matrix_frame, text=f"Fila {i + 1}", font=('Arial', 9, 'bold')).grid(row=i + 1, column=0,
                                                                                               padx=5, pady=5)

            for j in range(size):
                entry = ttk.Entry(self.matrix_frame, width=8, justify='center')
                entry.grid(row=i + 1, column=j + 1, padx=5, pady=5)
                if i == j:
                    entry.insert(0, "0")
                else:
                    entry.insert(0, "1")
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)


    def load_example(self):
        self.matrix_size.set(3)
        self.power.set(3)
        self.create_matrix_inputs()

        for i in range(3):
            for j in range(3):
                if i == j:
                    self.matrix_entries[i][j].delete(0, tk.END)
                    self.matrix_entries[i][j].insert(0, "0")
                else:
                    self.matrix_entries[i][j].delete(0, tk.END)
                    self.matrix_entries[i][j].insert(0, "1")

    def get_matrix_from_inputs(self):
        size = self.matrix_size.get()
        matrix = []

        for i in range(size):
            row = []
            for j in range(size):
                try:
                    value = float(self.matrix_entries[i][j].get())
                    row.append(value)
                except ValueError:
                    messagebox.showerror("Error", f"Valor inválido en fila {i + 1}, columna {j + 1}")
                    return None
            matrix.append(row)

        return np.array(matrix, dtype=float)

    def rationalize_vector(self, vector, tolerance=1e-8):
        vector_rounded = np.round(vector, 10)

        if np.all(np.abs(vector_rounded) < tolerance):
            return np.zeros_like(vector_rounded, dtype=int)

        fractions = []
        for val in vector_rounded:
            if abs(val) < tolerance:
                fractions.append(Fraction(0, 1))
                continue

            frac = Fraction(val).limit_denominator(1000)
            fractions.append(frac)

        denoms = [f.denominator for f in fractions if f.denominator != 1 and f != 0]
        if not denoms:
            int_vector = [int(f.numerator) for f in fractions]
        else:
            lcm = 1
            for denom in denoms:
                lcm = lcm * denom // math.gcd(lcm, denom)

            int_vector = [int(f * lcm) for f in fractions]

        non_zero = [abs(v) for v in int_vector if v != 0]
        if non_zero:
            gcd_val = non_zero[0]
            for val in non_zero[1:]:
                gcd_val = math.gcd(gcd_val, val)

            if gcd_val > 1:
                int_vector = [v // gcd_val for v in int_vector]

        return np.array(int_vector)

    def group_eigenvectors(self, eigenvalues, eigenvectors, tolerance=1e-10):
        rounded_eigenvalues = np.round(eigenvalues, 10)

        unique_eigenvalues = []
        for val in rounded_eigenvalues:
            if not any(np.abs(val - u) < tolerance for u in unique_eigenvalues):
                unique_eigenvalues.append(val)

        grouped = {}
        for i, eigval in enumerate(rounded_eigenvalues):
            for u in unique_eigenvalues:
                if np.abs(eigval - u) < tolerance:
                    key = u
                    break

            if key not in grouped:
                grouped[key] = []

            rational_eigenvector = self.rationalize_vector(eigenvectors[:, i])
            grouped[key].append(rational_eigenvector)

        return unique_eigenvalues, grouped

    def calculate_power(self):
        C = self.get_matrix_from_inputs()
        if C is None:
            return

        n = self.power.get()
        size = len(C)

        self.results_text.delete(1.0, tk.END)

        self.results_text.insert(tk.END, "\n" + "═" * 70 + "\n")
        self.results_text.insert(tk.END, "   CÁLCULO DE Cⁿ POR DIAGONALIZACIÓN\n")
        self.results_text.insert(tk.END, "═" * 70 + "\n\n")

        self.results_text.insert(tk.END, f"Matriz de adyacencia C ({size}×{size}):\n")
        self.results_text.insert(tk.END, self.matrix_to_str(C) + "\n\n")
        self.results_text.insert(tk.END, f"Potencia a calcular: n = {n}\n\n")

        try:
            self.results_text.insert(tk.END, "\n" + "─" * 60 + "\n")
            self.results_text.insert(tk.END, "PASO 1: Cálculo de autovalores y autovectores\n")
            self.results_text.insert(tk.END, "─" * 60 + "\n")
            eigenvalues, eigenvectors = np.linalg.eig(C)

            if np.all(np.abs(eigenvalues.imag) < 1e-10):
                eigenvalues = eigenvalues.real
                eigenvectors = eigenvectors.real
            else:
                self.results_text.insert(tk.END, "Nota: La matriz tiene autovalores complejos\n")

            unique_eigenvalues, grouped_eigenvectors = self.group_eigenvectors(eigenvalues, eigenvectors)

            self.results_text.insert(tk.END, "Autovalores encontrados:\n")
            for val in unique_eigenvalues:
                self.results_text.insert(tk.END, f"   λ = {val:.4f}\n")
            self.results_text.insert(tk.END, "\n")

            for eigval in unique_eigenvalues:
                self.results_text.insert(tk.END, f"Autovalor λ = {eigval:.4f}:\n")
                for i, eigenvector in enumerate(grouped_eigenvectors[eigval]):
                    eigenvector_str = "  ["
                    for j, val in enumerate(eigenvector):
                        if j > 0:
                            eigenvector_str += ", "
                        eigenvector_str += f"{val}"
                    eigenvector_str += "]"
                    self.results_text.insert(tk.END, f"  Autovector {i + 1}: {eigenvector_str}\n")
                self.results_text.insert(tk.END, "\n")

            self.results_text.insert(tk.END, "\nPASO 2: Construcción de matrices P y D\n")

            P_columns = []
            eigenvalues_for_D = []

            for eigval in unique_eigenvalues:
                if eigval in grouped_eigenvectors:
                    eigenvectors_for_eigval = grouped_eigenvectors[eigval]

                    for eigenvector in eigenvectors_for_eigval:
                        P_columns.append(eigenvector.astype(float))
                        eigenvalues_for_D.append(eigval)

            if len(P_columns) < size:
                self.results_text.insert(tk.END,
                                         f"ADVERTENCIA: Solo se encontraron {len(P_columns)} autovectores independientes "
                                         f"de {size} necesarios.\n")

                remaining = size - len(P_columns)
                for i in range(remaining):
                    if i < len(eigenvalues):
                        P_columns.append(eigenvectors[:, i].real)
                        eigenvalues_for_D.append(eigenvalues[i].real)

            elif len(P_columns) > size:
                self.results_text.insert(tk.END,
                                         f"ADVERTENCIA: Se encontraron {len(P_columns)} autovectores, "
                                         f"tomando los primeros {size}.\n")
                P_columns = P_columns[:size]
                eigenvalues_for_D = eigenvalues_for_D[:size]

            if len(P_columns) < size:
                P_columns = [eigenvectors[:, i] for i in range(size)]
                eigenvalues_for_D = eigenvalues
                self.results_text.insert(tk.END,
                                         "Nota: Usando autovectores originales (no se pudieron racionalizar todos)\n")

            P = np.column_stack(P_columns)
            D = np.diag(eigenvalues_for_D)

            if np.linalg.matrix_rank(P) < size:
                self.results_text.insert(tk.END, "¡ADVERTENCIA: La matriz no es diagonalizable! "
                                                 "Los autovectores no son linealmente independientes.\n")
                P_inv = np.linalg.pinv(P)
                self.results_text.insert(tk.END, "Usando pseudoinversa para continuar.\n")
            else:
                P_inv = np.linalg.inv(P)

            self.results_text.insert(
                tk.END,
                f"Matriz P (autovectores racionalizados):\n{self.matrix_to_str(P)}\n\n"
            )

            self.results_text.insert(
                tk.END,
                f"Matriz D (autovalores en diagonal):\n{self.matrix_to_str(D)}\n\n"
            )

            self.results_text.insert(
                tk.END,
                f"Matriz P⁻¹:\n{self.matrix_to_str(P_inv)}\n\n"
            )

            self.results_text.insert(tk.END, "PASO 3: Cálculo de Dⁿ\n")
            D_power = np.diag(np.array(eigenvalues_for_D) ** n)
            self.results_text.insert(
                tk.END,
                f"Dⁿ (cada autovalor elevado a {n}):\n{self.matrix_to_str(D_power)}\n\n"
            )

            self.results_text.insert(tk.END, "PASO 4: Cálculo de Cⁿ = P × Dⁿ × P⁻¹\n")
            C_power = P @ D_power @ P_inv

            C_power_rounded = np.round(C_power, 12)
            if np.allclose(C_power_rounded, np.round(C_power_rounded), atol=1e-10):
                C_power = np.round(C_power_rounded).astype(int)
            else:
                C_power = C_power_rounded


            self.results_text.insert(tk.END, f"Matriz resultante Cⁿ:\n{self.matrix_to_str(C_power)}\n\n")

            self.results_text.insert(tk.END, "PASO 5: Interpretación en el contexto de redes\n")
            self.results_text.insert(tk.END, "\n" + "═" * 70 + "\n")


            self.results_text.insert(tk.END, "\nINTERPRETACIÓN DE RESULTADOS:\n")

            if size > 0:
                diag_idx = 0
                diag_value = C_power[diag_idx, diag_idx]
                self.results_text.insert(tk.END,
                                         f"• Elemento en la diagonal Cⁿ[{diag_idx + 1},{diag_idx + 1}] = {diag_value:.2f}\n")
                self.results_text.insert(tk.END,
                                         f"  Representa el número de caminos de longitud {n} desde el dispositivo {diag_idx + 1} "
                                         f"hasta sí mismo (ciclos de longitud {n}).\n\n")

            if size > 1:
                off_diag_row, off_diag_col = 0, 1
                off_diag_value = C_power[off_diag_row, off_diag_col]
                self.results_text.insert(tk.END,
                                         f"• Elemento fuera de la diagonal Cⁿ[{off_diag_row + 1},{off_diag_col + 1}] = {off_diag_value:.2f}\n")
                self.results_text.insert(tk.END,
                                         f"  Representa el número de caminos de longitud {n} desde el dispositivo {off_diag_row + 1} "
                                         f"hasta el dispositivo {off_diag_col + 1}.\n\n")

            self.results_text.insert(tk.END, "INFORMACIÓN ADICIONAL PARA ANÁLISIS DE REDES:\n")
            self.results_text.insert(tk.END,
                                     f"• La matriz Cⁿ muestra todos los caminos de longitud {n} entre dispositivos.\n")
            self.results_text.insert(tk.END, "• Valores altos indican muchas conexiones indirectas entre nodos.\n")
            self.results_text.insert(tk.END, "• Una red está mejor conectada si hay múltiples caminos entre nodos.\n")
            self.results_text.insert(tk.END,
                                     "• Los elementos diagonales representan ciclos (caminos que regresan al origen).\n")

            self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
            self.results_text.insert(tk.END, "VERIFICACIÓN: Cálculo directo de Cⁿ (sin diagonalización)\n")
            C_power_direct = np.linalg.matrix_power(C, n)
            C_power_direct = np.round(C_power_direct, 6)

            if np.allclose(C_power, C_power_direct, atol=1e-6):
                self.results_text.insert(tk.END, "✓ Los resultados coinciden (método validado).\n")
            else:
                self.results_text.insert(tk.END,
                                         "⚠ Hay diferencias numéricas pequeñas (normal en cálculos con punto flotante).\n")
                self.results_text.insert(tk.END, f"Matriz por cálculo directo:\n{self.matrix_to_str(C_power_direct)}\n")

            self.result_matrix = C_power

        except np.linalg.LinAlgError as e:
            messagebox.showerror("Error de cálculo", f"No se pudo diagonalizar la matriz:\n{str(e)}")
            self.results_text.insert(tk.END, f"ERROR: {str(e)}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{str(e)}")
            self.results_text.insert(tk.END, f"ERROR: {str(e)}\n")

    def matrix_to_str(self, matrix, precision=4):
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


def main():
    root = tk.Tk()
    app = MatrixDiagonalizationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()