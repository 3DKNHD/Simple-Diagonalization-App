import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from matrix_logic import MatrixCalculator
from pdf_exporter import PDFExporter


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

    def export_to_pdf(self):
        if self.result_matrix is None or not self.result_matrix.any():
            messagebox.showerror("Error", "Primero debes calcular la matriz.")
            return

        content = self.results_text.get(1.0, tk.END)
        PDFExporter.export_to_pdf(content)

    def calculate_power(self):
        import numpy as np
        C = self.get_matrix_from_inputs()
        if C is None:
            return

        n = self.power.get()

        self.results_text.delete(1.0, tk.END)

        try:
            results = MatrixCalculator.calculate_power(C, n)

            self.results_text.insert(tk.END, "\n" + "═" * 70 + "\n")
            self.results_text.insert(tk.END, "   CÁLCULO DE Cⁿ POR DIAGONALIZACIÓN\n")
            self.results_text.insert(tk.END, "═" * 70 + "\n\n")

            self.results_text.insert(tk.END, f"Matriz de adyacencia C ({results['size']}×{results['size']}):\n")
            self.results_text.insert(tk.END, MatrixCalculator.matrix_to_str(C) + "\n\n")
            self.results_text.insert(tk.END, f"Potencia a calcular: n = {n}\n\n")

            self.results_text.insert(tk.END, "\n" + "─" * 60 + "\n")
            self.results_text.insert(tk.END, "PASO 1: Cálculo de autovalores y autovectores\n")
            self.results_text.insert(tk.END, "─" * 60 + "\n")

            self.results_text.insert(tk.END, "\nAutovalores y autovectores agrupados:\n")
            self.results_text.insert(tk.END, "-" * 50 + "\n")

            for i, group in enumerate(results['eigenvalues_groups']):
                eigenvalue = group[0][0]
                self.results_text.insert(tk.END,
                                         f"\nGrupo {i + 1}: Autovalor λ = {MatrixCalculator.format_eigenvalue(eigenvalue)}\n")

                for j, (_, eigenvector) in enumerate(group):
                    self.results_text.insert(tk.END,
                                             f"   Autovector {j + 1}: {MatrixCalculator.format_eigenvector(eigenvector)}\n")

            self.results_text.insert(tk.END, "-" * 50 + "\n")

            self.results_text.insert(tk.END, "\nPASO 2: Construcción de matrices P, D y P⁻¹\n")
            self.results_text.insert(tk.END,
                                     f"\nMatriz P (autovectores como columnas):\n{MatrixCalculator.matrix_to_str_fractions(results['P'])}\n")
            self.results_text.insert(tk.END,
                                     f"\nMatriz D (autovalores en diagonal):\n{MatrixCalculator.matrix_to_str_fractions(results['D'])}\n")
            self.results_text.insert(tk.END,
                                     f"\nMatriz P⁻¹:\n{MatrixCalculator.matrix_to_str_fractions(results['P_inv'])}\n")

            self.results_text.insert(tk.END, "\nPASO 3: Cálculo de Dⁿ\n")
            self.results_text.insert(tk.END,
                                     f"\nDⁿ (cada autovalor elevado a {n}):\n{MatrixCalculator.matrix_to_str_fractions(results['D_power'])}\n")

            self.results_text.insert(tk.END, "\nPASO 4: Cálculo de Cⁿ = P × Dⁿ × P⁻¹\n")
            self.results_text.insert(tk.END,
                                     f"\nMatriz resultante Cⁿ:\n{MatrixCalculator.matrix_to_str_fractions(results['result'])}\n")

            warning_shown = False
            if results['direct_power'] is not None:
                C_power_normalized = results['result'].astype(float)
                C_power_direct_normalized = results['direct_power'].astype(float)
                max_abs_direct = np.max(np.abs(C_power_direct_normalized))
                if max_abs_direct > 1e-10:
                    rel_error = np.max(np.abs(C_power_normalized - C_power_direct_normalized) / max_abs_direct)
                    if rel_error > 1e-5:
                        warning_shown = True

            if warning_shown:
                self.results_text.insert(1.0,
                                         "\nADVERTENCIA: Posible error numérico detectado\n"
                                         "   Los resultados pueden tener errores de precisión significativos.\n"
                                         "   Se recomienda verificar manualmente para cálculos críticos.\n\n"
                                         )

            self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
            self.results_text.insert(tk.END, "PASO 5: Interpretación en el contexto de redes\n")
            self.results_text.insert(tk.END, f"\nINTERPRETACIÓN DE RESULTADOS(n = {n}):\n\n")

            size = results['size']
            C_power = results['result']

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