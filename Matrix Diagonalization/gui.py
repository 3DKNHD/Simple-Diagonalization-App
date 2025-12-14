import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext


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
        self.calculator = None
        self.pdf_exporter = None

        self.setup_ui()

    def set_dependencies(self, calculator, pdf_exporter):
        self.calculator = calculator
        self.pdf_exporter = pdf_exporter

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
            text="Calcula Cⁿ usando autovalores:  Cⁿ = P * Dⁿ * P⁻¹",
            foreground="#555",
            style = "Title.TLabel"
        ).grid(row=1, column=0, columnspan=2, pady=(0, 15))

        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding=10)
        config_frame.grid(row=2, column=0, sticky="nsw", padx=(0, 10))

        ttk.Label(config_frame, text="Orden de la matriz (n×n)").grid(row=0, column=0, sticky="w")
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

        self.matrix_frame = ttk.LabelFrame(right_frame, text="Matriz de Adyacencia", padding=10)
        self.matrix_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        results_frame = ttk.LabelFrame(right_frame, text="Resultados paso a paso", padding=10)
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
            ttk.Label(self.matrix_frame, text=f"Col {j + 1}", font=('Arial', 9, 'bold')).grid(
                row=0, column=j + 1, padx=5, pady=5
            )

        for i in range(size):
            row_entries = []
            ttk.Label(self.matrix_frame, text=f"Fila {i + 1}", font=('Arial', 9, 'bold')).grid(
                row=i + 1, column=0, padx=5, pady=5
            )

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
        return matrix

    def export_to_pdf(self):
        if self.result_matrix is None:
            messagebox.showerror("Error", "Primero debes calcular la matriz.")
            return

        content = self.results_text.get(1.0, tk.END)
        if self.pdf_exporter:
            self.pdf_exporter.export_to_pdf(content)

    def display_results(self, calculation_result):

        self.results_text.delete(1.0, tk.END)

        if not calculation_result:
            return

        self.results_text.insert(tk.END, "\n" + "═" * 70 + "\n")
        self.results_text.insert(tk.END, "   CÁLCULO DE Cⁿ POR DIAGONALIZACIÓN\n")
        self.results_text.insert(tk.END, "═" * 70 + "\n\n")

        self.results_text.insert(tk.END,
                                 f"Matriz de adyacencia C ({calculation_result['size']}×{calculation_result['size']}):\n")
        matrix_str = self.calculator.matrix_to_str(calculation_result['matrix'])
        self.results_text.insert(tk.END, matrix_str + "\n\n")
        self.results_text.insert(tk.END, f"Potencia a calcular: n = {calculation_result['power']}\n\n")

        self.results_text.insert(tk.END, "\n" + "─" * 60 + "\n")
        self.results_text.insert(tk.END, "PASO 1: Cálculo de autovalores y autovectores\n")
        self.results_text.insert(tk.END, "─" * 60 + "\n")
        self.results_text.insert(tk.END, "\nAutovalores y autovectores asociados:\n")
        self.results_text.insert(tk.END, "-" * 50 + "\n")

        for i, group in enumerate(calculation_result['eigenvalues_groups']):
            eigenvalue = group[0][0]
            self.results_text.insert(
                tk.END,
                f"\nAutovalor λ = {self.calculator.format_eigenvalue(eigenvalue)}\n"
            )

            for j, (_, eigenvector) in enumerate(group):
                self.results_text.insert(
                    tk.END,
                    f"   Autovector {j + 1}: {self.calculator.format_eigenvector(eigenvector)}\n"
                )

        self.results_text.insert(tk.END, "-" * 50 + "\n")

        self.results_text.insert(tk.END, "\nPASO 2: Construcción de matrices P, D y P⁻¹\n")
        self.results_text.insert(
            tk.END,
            f"\nMatriz P (autovectores como columnas):\n{self.calculator.matrix_to_str_fractions(calculation_result['P'])}\n"
        )
        self.results_text.insert(
            tk.END,
            f"\nMatriz D (autovalores en diagonal):\n{self.calculator.matrix_to_str_fractions(calculation_result['D'])}\n"
        )
        self.results_text.insert(
            tk.END,
            f"\nMatriz P⁻¹:\n{self.calculator.matrix_to_str_fractions(calculation_result['P_inv'])}\n"
        )

        self.results_text.insert(tk.END, "\nPASO 3: Cálculo de Dⁿ\n")
        self.results_text.insert(
            tk.END,
            f"\nDⁿ (cada autovalor elevado a {calculation_result['power']}):\n"
            f"{self.calculator.matrix_to_str_fractions(calculation_result['D_power'])}\n"
        )

        self.results_text.insert(tk.END, "\nPASO 4: Cálculo de Cⁿ = P * Dⁿ * P⁻¹\n")
        self.results_text.insert(
            tk.END,
            f"\nMatriz resultante Cⁿ:\n{self.calculator.matrix_to_str_fractions(calculation_result['result'])}\n"
        )

        if calculation_result.get('warning'):
            self.results_text.insert(1.0,
                                     "\nADVERTENCIA: Posible error numérico detectado\n"
                                     "   Los resultados pueden tener errores de precisión significativos.\n"
                                     "   Se recomienda verificar manualmente para cálculos críticos.\n\n"
                                     )

        self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.results_text.insert(tk.END, "PASO 5: Interpretación en el contexto de redes\n")
        self.results_text.insert(tk.END, f"\nINTERPRETACIÓN DE RESULTADOS (n = {calculation_result['power']}):\n\n")

        if 'interpretation' in calculation_result:
            self.results_text.insert(tk.END, calculation_result['interpretation'])
        else:
            self.results_text.insert(tk.END,
                                     "• La matriz Cⁿ muestra todos los caminos de longitud n entre dispositivos.\n"
                                     "• Valores altos indican muchas conexiones indirectas entre nodos.\n"
                                     "• Una red está mejor conectada si hay múltiples caminos entre nodos.\n"
                                     "• Los elementos diagonales representan ciclos (caminos que regresan al origen).\n"
                                     )

        self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.results_text.insert(tk.END, "Cálculo completado exitosamente\n")
        if calculation_result.get('warning'):
            self.results_text.insert(tk.END, "Nota: Ver advertencia al inicio de los resultados.\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n")

    def calculate_power(self):
        if not self.calculator:
            messagebox.showerror("Error", "Calculadora no disponible")
            return

        matrix_data = self.get_matrix_from_inputs()
        if matrix_data is None:
            return

        try:
            result = self.calculator.calculate_power(matrix_data, self.power.get())

            self.result_matrix = result['result']

            self.display_results(result)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error!")
            self.results_text.delete(1.0, tk.END)
            if str(e) == "Singular matrix":
                self.results_text.insert(tk.END, f"ERROR: No coincide la multiplicidad de los valores propios con la Dimensión de los subespacios propios asociados a estos\nNO DIAGONALIZABLE\n")
            elif str(e) == "No reales":
                self.results_text.insert(tk.END, f"ERROR: Algunos valores propios no son reales\nNO DIAGONALIZABLE\n")
            elif str(e) == "Ponderada!":
                self.results_text.insert(tk.END, f"ERROR: Como la matriz tiene pesos no se cumple la propiedad!\nNO CUMPLE LA PROPIEDAD\n")
            else:
                self.results_text.insert(tk.END, "Error", f"Ocurrió un error:\n{str(e)}")