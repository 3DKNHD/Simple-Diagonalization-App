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
            text="Calcula Cⁿ usando autovalores:  Cⁿ = P Dⁿ P⁻¹",
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
            style="Secondary.TButton"
        ).grid(row=5, column=0, sticky="ew")

        ttk.Button(
            config_frame,
            text="Calcular Cⁿ",
            command=self.calculate_power,
            style="Primary.TButton"
        ).grid(row=6, column=0, sticky="ew", pady=(20, 0))

        ttk.Button(
            config_frame,
            text="Exportar a PDF",
            command=self.export_to_pdf,
            style="Danger.TButton"
        ).grid(row=7, column=0, sticky="ew", pady=5)

        ttk.Button(
            config_frame,
            text="Alternar modo oscuro",
            command=self.toggle_dark_mode,
            style="Neutral.TButton"
        ).grid(row=8, column=0, sticky="ew", pady=5)
        self.update_button_styles()

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

    def find_simple_eigenvectors(self, eigenvectors, eigenvalues):
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

    def group_eigenvalues_eigenvectors(self, eigenvalues, eigenvectors):
        tolerance = 1e-10

        eigenvalues = np.array(eigenvalues)
        eigenvectors = np.array(eigenvectors)

        if np.all(np.abs(eigenvalues.imag) < tolerance):
            eigenvalues = eigenvalues.real
            eigenvectors = eigenvectors.real

        eigenvectors = self.find_simple_eigenvectors(eigenvectors, eigenvalues)

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

    def format_eigenvalue(self, eigenvalue):
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

    def format_eigenvector(self, eigenvector):
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

    def matrix_to_str_fractions(self, matrix, matrix_type="all"):
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

    def calculate_power(self):
        C = self.get_matrix_from_inputs()
        if C is None:
            return

        n = self.power.get()
        size = len(C)

        self.results_text.delete(1.0, tk.END)

        try:
            C_power_direct = np.linalg.matrix_power(C, n)
        except:
            C_power_direct = None

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

            groups = self.group_eigenvalues_eigenvectors(eigenvalues, eigenvectors)

            self.results_text.insert(tk.END, "\nAutovalores y autovectores agrupados:\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n")

            all_eigenvalues = []
            all_eigenvectors = []

            for i, group in enumerate(groups):
                eigenvalue = group[0][0]
                self.results_text.insert(tk.END,
                                         f"\nGrupo {i + 1}: Autovalor λ = {self.format_eigenvalue(eigenvalue)}\n")

                for eigenvalue, eigenvector in group:
                    all_eigenvalues.append(eigenvalue)
                    all_eigenvectors.append(eigenvector)

                for j, (_, eigenvector) in enumerate(group):
                    self.results_text.insert(tk.END, f"   Autovector {j + 1}: {self.format_eigenvector(eigenvector)}\n")

            self.results_text.insert(tk.END, "-" * 50 + "\n")

            P = np.column_stack(all_eigenvectors)
            eigenvalues_array = np.array(all_eigenvalues)

            D = np.diag(eigenvalues_array)

            try:
                P_inv = np.linalg.inv(P)
            except np.linalg.LinAlgError:
                self.results_text.insert(tk.END, "ERROR: La matriz P no es invertible.\n")
                return

            self.results_text.insert(tk.END, "\nPASO 2: Construcción de matrices P, D y P⁻¹\n")

            self.results_text.insert(
                tk.END,
                f"\nMatriz P (autovectores como columnas):\n{self.matrix_to_str_fractions(P)}\n"
            )

            self.results_text.insert(
                tk.END,
                f"\nMatriz D (autovalores en diagonal):\n{self.matrix_to_str_fractions(D)}\n"
            )

            self.results_text.insert(
                tk.END,
                f"\nMatriz P⁻¹:\n{self.matrix_to_str_fractions(P_inv)}\n"
            )

            self.results_text.insert(tk.END, "\nPASO 3: Cálculo de Dⁿ\n")
            D_power = np.diag(eigenvalues_array ** n)
            self.results_text.insert(
                tk.END,
                f"\nDⁿ (cada autovalor elevado a {n}):\n{self.matrix_to_str_fractions(D_power)}\n"
            )

            self.results_text.insert(tk.END, "\nPASO 4: Cálculo de Cⁿ = P × Dⁿ × P⁻¹\n")

            temp = P @ D_power
            C_power = temp @ P_inv

            C_power_rounded = np.round(C_power, 10)

            if np.all(np.abs(C_power_rounded - np.round(C_power_rounded)) < 1e-8):
                C_power = np.round(C_power_rounded).astype(int)
            else:
                C_power = C_power_rounded

            warning_shown = False
            if C_power_direct is not None:
                C_power_normalized = C_power.astype(float)
                C_power_direct_normalized = C_power_direct.astype(float)

                max_abs_direct = np.max(np.abs(C_power_direct_normalized))
                if max_abs_direct > 1e-10:  # Evitar división por cero
                    # Error relativo máximo
                    rel_error = np.max(np.abs(C_power_normalized - C_power_direct_normalized) / max_abs_direct)

                    # Solo mostrar advertencia si el error es significativo
                    if rel_error > 1e-5:  # Más del 0.001% de error relativo
                        warning_shown = True

            self.results_text.insert(tk.END, f"\nMatriz resultante Cⁿ:\n{self.matrix_to_str_fractions(C_power)}\n")

            # ========== MOSTRAR ADVERTENCIA SI ES NECESARIO ==========
            if warning_shown:
                # Solo mostrar una vez al inicio de los resultados
                self.results_text.insert(1.0,
                                         "\n⚠️ ADVERTENCIA: Posible error numérico detectado\n"
                                         "   Los resultados pueden tener errores de precisión significativos.\n"
                                         "   Se recomienda verificar manualmente para cálculos críticos.\n\n"
                                         )

            self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
            self.results_text.insert(tk.END, "PASO 5: Interpretación en el contexto de redes\n")

            self.results_text.insert(tk.END, f"\nINTERPRETACIÓN DE RESULTADOS(n = {n}):\n\n")

            if size > 0:
                diag_idx = 0
                diag_value = C_power[diag_idx, diag_idx]
                try:
                    if abs(diag_value - round(diag_value)) > 1e-8:
                        frac = Fraction(diag_value).limit_denominator(20)
                        gcd_val = math.gcd(abs(frac.numerator), frac.denominator)
                        num_simple = frac.numerator // gcd_val
                        denom_simple = frac.denominator // gcd_val
                        if denom_simple == 1:
                            diag_str = f"{num_simple}"
                        else:
                            diag_str = f"{num_simple}/{denom_simple}"
                    else:
                        diag_str = f"{int(round(diag_value))}"
                except:
                    diag_str = f"{diag_value:.2f}"

                self.results_text.insert(tk.END,
                                         f"• Elemento en la diagonal Cⁿ[{diag_idx + 1},{diag_idx + 1}] = {diag_str}\n")
                self.results_text.insert(tk.END,
                                         f"  Representa el número de caminos de longitud {n} desde el dispositivo {diag_idx + 1} "
                                         f"hasta sí mismo (ciclos de longitud {n}).\n\n")

            if size > 1:
                off_diag_row, off_diag_col = 0, 1
                off_diag_value = C_power[off_diag_row, off_diag_col]
                try:
                    if abs(off_diag_value - round(off_diag_value)) > 1e-8:
                        frac = Fraction(off_diag_value).limit_denominator(20)
                        gcd_val = math.gcd(abs(frac.numerator), frac.denominator)
                        num_simple = frac.numerator // gcd_val
                        denom_simple = frac.denominator // gcd_val
                        if denom_simple == 1:
                            off_diag_str = f"{num_simple}"
                        else:
                            off_diag_str = f"{num_simple}/{denom_simple}"
                    else:
                        off_diag_str = f"{int(round(off_diag_value))}"
                except:
                    off_diag_str = f"{off_diag_value:.2f}"

                self.results_text.insert(tk.END,
                                         f"• Elemento fuera de la diagonal Cⁿ[{off_diag_row + 1},{off_diag_col + 1}] = {off_diag_str}\n")
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

            self.results_text.insert(tk.END, "✓ Cálculo completado exitosamente\n")
            if warning_shown:
                self.results_text.insert(tk.END, "⚠ Nota: Ver advertencia al inicio de los resultados.\n")
            self.results_text.insert(tk.END, "=" * 60 + "\n")

            self.result_matrix = C_power

        except np.linalg.LinAlgError as e:
            messagebox.showerror("Error de cálculo", f"No se pudo diagonalizar la matriz:\n{str(e)}")
            self.results_text.insert(tk.END, f"ERROR: {str(e)}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{str(e)}")
            self.results_text.insert(tk.END, f"ERROR: {str(e)}\n")


def main():
    root = tk.Tk()
    app = MatrixDiagonalizationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()