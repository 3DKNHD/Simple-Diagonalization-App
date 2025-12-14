import tkinter as tk
from matrix_logic import MatrixCalculator
from pdf_exporter import PDFExporter
from gui import MatrixDiagonalizationApp


def main():

    calculator = MatrixCalculator()
    pdf_exporter = PDFExporter()

    root = tk.Tk()
    app = MatrixDiagonalizationApp(root)
    app.set_dependencies(calculator, pdf_exporter)

    root.mainloop()


if __name__ == "__main__":
    main()