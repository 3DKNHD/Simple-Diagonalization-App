"""Interfaz gráfica para diagonalización y potencias de matrices."""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

from .calculator import MatrixCalculator
from .examples import EXAMPLES
from .exceptions import MatrixError
from .pdf_exporter import PDFExporter


class MatrixDiagonalizationApp:
    def __init__(self, root, calculator=None, pdf_exporter=None):
        self.root = root
        self.root.title("Diagonalización de Matrices")
        self.root.geometry("980x760")
        self.root.minsize(860, 640)
        self.dark_mode = False

        self.matrix_size = tk.IntVar(value=3)
        self.power = tk.IntVar(value=3)
        self.adjacency_only = tk.BooleanVar(value=False)
        self.example_name = tk.StringVar(value="K3 (completo 3×3)")
        self.matrix_entries = []
        self.result_matrix = None
        self.calculator = calculator or MatrixCalculator()
        self.pdf_exporter = pdf_exporter or PDFExporter()

        self.setup_ui()

    def set_dependencies(self, calculator, pdf_exporter):
        self.calculator = calculator
        self.pdf_exporter = pdf_exporter

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TCheckbutton", font=("Segoe UI", 10))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        ttk.Label(
            main_frame,
            text="Potencias por diagonalización",
            style="Title.TLabel",
        ).grid(row=0, column=0, columnspan=2, pady=(0, 4))

        ttk.Label(
            main_frame,
            text="Cⁿ = P  Dⁿ  P⁻¹   ·   válida cuando C es diagonalizable sobre ℝ",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, columnspan=2, pady=(0, 12))

        config_frame = ttk.LabelFrame(main_frame, text="Configuración", padding=10)
        config_frame.grid(row=2, column=0, sticky="nsw", padx=(0, 10))

        ttk.Label(config_frame, text="Orden de la matriz (n×n)").grid(row=0, column=0, sticky="w")
        ttk.Spinbox(
            config_frame,
            from_=2,
            to=10,
            textvariable=self.matrix_size,
            width=8,
            command=self.create_matrix_inputs,
        ).grid(row=1, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(config_frame, text="Potencia n").grid(row=2, column=0, sticky="w")
        ttk.Spinbox(
            config_frame,
            from_=0,
            to=50,
            textvariable=self.power,
            width=8,
        ).grid(row=3, column=0, sticky="ew", pady=(0, 8))

        ttk.Checkbutton(
            config_frame,
            text="Solo adyacencia (0 y 1)",
            variable=self.adjacency_only,
        ).grid(row=4, column=0, sticky="w", pady=(0, 10))

        ttk.Button(
            config_frame,
            text="Crear matriz",
            command=self.create_matrix_inputs,
            style="Secondary.TButton",
        ).grid(row=5, column=0, sticky="ew", pady=3)

        ttk.Label(config_frame, text="Ejemplos").grid(row=6, column=0, sticky="w", pady=(8, 0))
        example_box = ttk.Combobox(
            config_frame,
            textvariable=self.example_name,
            values=list(EXAMPLES.keys()),
            state="readonly",
            width=22,
        )
        example_box.grid(row=7, column=0, sticky="ew", pady=(0, 4))
        ttk.Button(
            config_frame,
            text="Cargar ejemplo",
            command=self.load_example,
            style="Secondary.TButton",
        ).grid(row=8, column=0, sticky="ew")

        ttk.Button(
            config_frame,
            text="Calcular Cⁿ",
            command=self.calculate_power,
            style="Primary.TButton",
        ).grid(row=9, column=0, sticky="ew", pady=(16, 0))

        ttk.Button(
            config_frame,
            text="Exportar a PDF",
            command=self.export_to_pdf,
            style="Danger.TButton",
        ).grid(row=10, column=0, sticky="ew", pady=4)

        ttk.Button(
            config_frame,
            text="Copiar resultados",
            command=self.copy_results,
            style="Neutral.TButton",
        ).grid(row=11, column=0, sticky="ew", pady=4)

        ttk.Button(
            config_frame,
            text="Alternar modo oscuro",
            command=self.toggle_dark_mode,
            style="Neutral.TButton",
        ).grid(row=12, column=0, sticky="ew", pady=4)

        self.update_button_styles()

        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=2, column=1, rowspan=2, sticky="nsew")
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)

        self.matrix_frame = ttk.LabelFrame(right_frame, text="Matriz C", padding=10)
        self.matrix_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        results_frame = ttk.LabelFrame(right_frame, text="Resultados paso a paso", padding=10)
        results_frame.grid(row=1, column=0, sticky="nsew")
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            height=22,
            wrap=tk.WORD,
            font=("Consolas", 10),
        )
        self.results_text.grid(row=0, column=0, sticky="nsew")

        self.status_var = tk.StringVar(value="Listo. Carga un ejemplo o introduce una matriz.")
        ttk.Label(main_frame, textvariable=self.status_var).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(8, 0)
        )

        self.create_matrix_inputs()
        self.root.bind("<Control-Return>", lambda _event: self.calculate_power())

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        style = ttk.Style()

        if self.dark_mode:
            bg, fg, entry_bg, button_bg = "#1e1e1e", "#ffffff", "#2b2b2b", "#3a3a3a"
            self.root.configure(bg=bg)
            style.configure("TFrame", background=bg)
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("Title.TLabel", background=bg, foreground=fg)
            style.configure("Subtitle.TLabel", background=bg, foreground="#dddddd")
            style.configure("TCheckbutton", background=bg, foreground=fg)
            style.configure("TButton", background=button_bg, foreground=fg, bordercolor=button_bg)
            style.map("TButton", background=[("active", "#505050")])
            style.configure("TLabelFrame", background=bg, foreground=fg)
            style.configure("TLabelFrame.Label", background=bg, foreground=fg)
            style.configure("TEntry", fieldbackground=entry_bg, foreground=fg)
            style.configure("TSpinbox", fieldbackground=entry_bg, foreground=fg, background=bg)
            style.configure("TCombobox", fieldbackground=entry_bg, foreground=fg, background=bg)
            self.results_text.configure(bg="#121212", fg="white", insertbackground="white")
        else:
            bg, fg = "#f0f0f0", "black"
            self.root.configure(bg=bg)
            style.configure("TFrame", background=bg)
            style.configure("TLabel", background=bg, foreground=fg)
            style.configure("Title.TLabel", background=bg, foreground=fg)
            style.configure("Subtitle.TLabel", background=bg, foreground="#444444")
            style.configure("TCheckbutton", background=bg, foreground=fg)
            style.configure("TButton", background="#e0e0e0", foreground=fg)
            style.configure("TLabelFrame", background=bg, foreground=fg)
            style.configure("TLabelFrame.Label", background=bg, foreground=fg)
            style.configure("TEntry", fieldbackground="white", foreground="black")
            style.configure("TSpinbox", fieldbackground="white", foreground="black", background=bg)
            style.configure("TCombobox", fieldbackground="white", foreground="black", background=bg)
            self.results_text.configure(bg="white", fg="black", insertbackground="black")

        self.update_button_styles()

    def update_button_styles(self):
        style = ttk.Style()
        style.configure("Primary.TButton", background="#4CAF50", foreground="white")
        style.configure("Secondary.TButton", background="#1976D2", foreground="white")
        style.configure("Danger.TButton", background="#D32F2F", foreground="white")
        if self.dark_mode:
            style.configure("Neutral.TButton", background="#555555", foreground="white")
            style.map("TButton", background=[("active", "#666666")])
        else:
            style.configure("Neutral.TButton", background="#DDDDDD", foreground="black")
            style.map("TButton", background=[("active", "#CCCCCC")])

    def create_matrix_inputs(self):
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        size = int(self.matrix_size.get())
        self.matrix_entries = []

        for j in range(size):
            ttk.Label(self.matrix_frame, text=f"Col {j + 1}", font=("Arial", 9, "bold")).grid(
                row=0, column=j + 1, padx=4, pady=4
            )

        for i in range(size):
            row_entries = []
            ttk.Label(self.matrix_frame, text=f"Fila {i + 1}", font=("Arial", 9, "bold")).grid(
                row=i + 1, column=0, padx=4, pady=4
            )
            for j in range(size):
                entry = ttk.Entry(self.matrix_frame, width=8, justify="center")
                entry.grid(row=i + 1, column=j + 1, padx=4, pady=4)
                entry.insert(0, "0" if i == j else "1")
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)

    def load_example(self):
        example = EXAMPLES.get(self.example_name.get())
        if example is None:
            messagebox.showerror("Error", "Selecciona un ejemplo válido.")
            return

        self.matrix_size.set(example["size"])
        self.power.set(example["power"])
        self.adjacency_only.set(example["adjacency"])
        self.create_matrix_inputs()

        for i, row in enumerate(example["matrix"]):
            for j, value in enumerate(row):
                self.matrix_entries[i][j].delete(0, tk.END)
                self.matrix_entries[i][j].insert(0, str(value))

        self.status_var.set(example.get("note", "Ejemplo cargado."))

    def get_matrix_from_inputs(self):
        size = int(self.matrix_size.get())
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                raw = self.matrix_entries[i][j].get().strip().replace(",", ".")
                try:
                    row.append(float(raw))
                except ValueError:
                    messagebox.showerror(
                        "Error",
                        f"Valor inválido en fila {i + 1}, columna {j + 1}: «{raw}»",
                    )
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

    def copy_results(self):
        content = self.results_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showinfo("Copiar", "No hay resultados para copiar.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(content)
        self.status_var.set("Resultados copiados al portapapeles.")

    def display_results(self, calculation_result):
        self.results_text.delete(1.0, tk.END)
        if not calculation_result:
            return

        calc = self.calculator
        size = calculation_result["size"]
        kind = "adyacencia" if calculation_result.get("is_adjacency") else "general"
        symmetry = "simétrica" if calculation_result.get("is_symmetric") else "no simétrica"

        self.results_text.insert(tk.END, "\n" + "═" * 70 + "\n")
        self.results_text.insert(tk.END, "   CÁLCULO DE Cⁿ POR DIAGONALIZACIÓN\n")
        self.results_text.insert(tk.END, "═" * 70 + "\n\n")
        self.results_text.insert(
            tk.END,
            f"Matriz C ({size}×{size}, {kind}, {symmetry}):\n",
        )
        self.results_text.insert(tk.END, calc.matrix_to_str(calculation_result["matrix"]) + "\n\n")
        self.results_text.insert(tk.END, f"Potencia a calcular: n = {calculation_result['power']}\n")

        self.results_text.insert(tk.END, "\n" + "─" * 60 + "\n")
        self.results_text.insert(tk.END, "PASO 1: Autovalores, autovectores y multiplicidades\n")
        self.results_text.insert(tk.END, "─" * 60 + "\n")

        for row in calculation_result.get("multiplicities", []):
            self.results_text.insert(
                tk.END,
                f"\nλ = {calc.format_eigenvalue(row['eigenvalue'])}   "
                f"alg = {row['algebraic']}   geo = {row['geometric']}\n",
            )

        for group in calculation_result["eigenvalues_groups"]:
            eigenvalue = group[0][0]
            self.results_text.insert(
                tk.END,
                f"\nAutovalor λ = {calc.format_eigenvalue(eigenvalue)}\n",
            )
            for j, (_, eigenvector) in enumerate(group):
                self.results_text.insert(
                    tk.END,
                    f"   Autovector {j + 1}: {calc.format_eigenvector(eigenvector)}\n",
                )

        self.results_text.insert(tk.END, "\nPASO 2: Construcción de P, D y P⁻¹\n")
        self.results_text.insert(
            tk.END,
            f"\nMatriz P (autovectores como columnas):\n{calc.matrix_to_str_fractions(calculation_result['P'])}\n",
        )
        self.results_text.insert(
            tk.END,
            f"\nMatriz D (autovalores en la diagonal):\n{calc.matrix_to_str_fractions(calculation_result['D'])}\n",
        )
        self.results_text.insert(
            tk.END,
            f"\nMatriz P⁻¹:\n{calc.matrix_to_str_fractions(calculation_result['P_inv'])}\n",
        )

        self.results_text.insert(tk.END, "\nPASO 3: Cálculo de Dⁿ\n")
        self.results_text.insert(
            tk.END,
            f"\nDⁿ (cada autovalor elevado a {calculation_result['power']}):\n"
            f"{calc.matrix_to_str_fractions(calculation_result['D_power'])}\n",
        )

        self.results_text.insert(tk.END, "\nPASO 4: Cⁿ = P Dⁿ P⁻¹\n")
        self.results_text.insert(
            tk.END,
            f"\nMatriz resultante Cⁿ:\n{calc.matrix_to_str_fractions(calculation_result['result'])}\n",
        )

        if calculation_result.get("direct_power") is not None:
            self.results_text.insert(
                tk.END,
                f"\nComprobación directa (Cⁿ por multiplicación):\n"
                f"{calc.matrix_to_str_fractions(calculation_result['direct_power'])}\n",
            )

        if calculation_result.get("warning"):
            self.results_text.insert(
                1.0,
                "\nADVERTENCIA: posible inestabilidad numérica "
                f"(||C−PDP⁻¹||∞ ≈ {calculation_result.get('residual', 0):.2e}, "
                f"cond(P) ≈ {calculation_result.get('cond_P', 0):.2e}).\n"
                "Verifica el resultado si lo vas a usar en un cálculo crítico.\n\n",
            )

        self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.results_text.insert(tk.END, "PASO 5: Interpretación\n")
        self.results_text.insert(tk.END, calculation_result.get("interpretation", ""))
        self.results_text.insert(tk.END, "\n" + "=" * 60 + "\n")
        self.results_text.insert(tk.END, "Cálculo completado.\n")
        self.results_text.insert(tk.END, "=" * 60 + "\n")

    def calculate_power(self):
        if not self.calculator:
            messagebox.showerror("Error", "Calculadora no disponible")
            return

        matrix_data = self.get_matrix_from_inputs()
        if matrix_data is None:
            return

        try:
            result = self.calculator.calculate_power(
                matrix_data,
                self.power.get(),
                adjacency_only=self.adjacency_only.get(),
            )
            self.result_matrix = result["result"]
            self.display_results(result)
            self.status_var.set(
                f"C^{result['power']} calculada. Residual ≈ {result['residual']:.2e}"
            )
        except MatrixError as exc:
            self.result_matrix = None
            messagebox.showerror("No se pudo calcular", str(exc))
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"ERROR\n{exc}\n")
            self.status_var.set(str(exc))
        except Exception as exc:
            self.result_matrix = None
            messagebox.showerror("Error", f"Ocurrió un error inesperado:\n{exc}")
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, f"Error inesperado:\n{exc}")
            self.status_var.set("Error inesperado.")


def run_app():
    root = tk.Tk()
    MatrixDiagonalizationApp(root)
    root.mainloop()
