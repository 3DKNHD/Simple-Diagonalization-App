# Matrix Diagonalization Power Calculator / Calculadora de Potencia Matricial por Diagonalización

## English

### Project Description
A Python desktop app that computes the n-th power of a square matrix by diagonalization (`Cⁿ = P Dⁿ P⁻¹`). It started as a Linear Algebra final project and now handles general real matrices, not only unweighted adjacency matrices.

### Features
- **Diagonalization method**: `Cⁿ = P Dⁿ P⁻¹` when `C` is diagonalizable over ℝ
- **General matrices**: integer or real entries, including weighted/symmetric cases
- **Optional adjacency mode**: restrict inputs to 0/1 and interpret `Cⁿ` as walks of length `n`
- **Diagonalizability checks**: real eigenvalues, algebraic vs geometric multiplicity, invertibility of `P`
- **Interactive GUI**: examples, dark mode, copy results, PDF export
- **Numerical verification**: residual `||C − P D P⁻¹||` compared with direct `matrix_power`

### Requirements
- Python 3.8+
- NumPy (>=1.21.0)
- ReportLab (>=3.6.0)
- Tkinter (on Ubuntu/Debian: `sudo apt install python3-tk`)

### Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage
```bash
python main.py
```
or:
```bash
python -m matrix_diagonalization
```

1. Set the matrix size (2×2 to 10×10) and the power `n` (0 to 50)
2. Enter the matrix, or load an example from the list
3. Optionally enable “Solo adyacencia (0 y 1)” for graph interpretation
4. Click **Calcular Cⁿ** (or `Ctrl+Enter`)
5. Export the step-by-step report to PDF if you want

### Tests
```bash
python -m unittest tests.test_calculator -v
```

### License
MIT License — academic and educational use welcome.

---

## Español

### Descripción
Aplicación de escritorio en Python que calcula la n-ésima potencia de una matriz cuadrada por diagonalización (`Cⁿ = P Dⁿ P⁻¹`). Nació como proyecto final de Álgebra Lineal y ahora admite matrices reales generales, no solo adyacencia 0-1.

### Características
- **Método de diagonalización**: `Cⁿ = P Dⁿ P⁻¹` si `C` es diagonalizable sobre ℝ
- **Matrices generales**: enteras o reales, incluidas las ponderadas y simétricas
- **Modo adyacencia opcional**: solo 0 y 1, e interpreta `Cⁿ` como caminos de longitud `n`
- **Comprobación de diagonalizabilidad**: autovalores reales, multiplicidad algebraica vs geométrica, invertibilidad de `P`
- **Interfaz**: ejemplos, modo oscuro, copiar resultados, exportar PDF
- **Verificación numérica**: residual `||C − P D P⁻¹||` frente al producto directo

### Requisitos
- Python 3.8+
- NumPy (>=1.21.0)
- ReportLab (>=3.6.0)
- Tkinter (en Ubuntu/Debian: `sudo apt install python3-tk`)

### Instalación
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Uso
```bash
python main.py
```
o:
```bash
python -m matrix_diagonalization
```

1. Elige el orden de la matriz (2×2 a 10×10) y la potencia `n` (0 a 50)
2. Introduce la matriz o carga un ejemplo
3. Marca “Solo adyacencia (0 y 1)” si quieres la lectura en teoría de grafos
4. Pulsa **Calcular Cⁿ** (o `Ctrl+Enter`)
5. Exporta el desarrollo a PDF si lo necesitas

### Pruebas
```bash
python -m unittest tests.test_calculator -v
```

### Licencia
Licencia MIT — uso académico y educativo.
