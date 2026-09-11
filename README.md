# Matrix Diagonalization Power Calculator / Calculadora de Potencia Matricial por Diagonalización

## English

### Project Description
A Streamlit web app that computes the n-th power of a square matrix with **exact arithmetic** (`sympy.Matrix`). When `A` is diagonalizable it uses `Aⁿ = P Dⁿ P⁻¹`; otherwise it falls back to the Jordan form. It started as a Linear Algebra final project for adjacency matrices and now covers general matrices over ℝ or ℂ.

### Features
- **Exact calculation**: integers, rationals (`1/2`) and decimals as `Rational` — no float-to-fraction guessing
- **Algebra / Graph modes**: in Graph mode, `(Aⁿ)ᵢⱼ` counts **walks** of length `n` (vertices may repeat)
- **Field ℝ or ℂ**: a 90° rotation is not diagonalizable over ℝ; it is over ℂ
- **Jordan form** when geometric multiplicity is smaller than algebraic (the flow does not stop)
- **Symmetric real matrices**: orthogonal `P` with **P⁻¹ = Pᵀ**
- **Characteristic polynomial**, eigen-systems for `n ≤ 4`, optional `e^{tA}`
- **Directed vs undirected graphs** (`A ≠ Aᵀ`) with Graphviz DOT
- **PDF download** (ReportLab, no file dialogs)

### Requirements
- Python 3.10+
- sympy, streamlit, reportlab (`pip install -r requirements.txt`)

### Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage
```bash
streamlit run app.py
```
or:
```bash
python main.py
```
or:
```bash
python -m matrix_diagonalization
```

1. Choose **Algebra** or **Graph**, and field **ℝ** or **ℂ**
2. Set the order (2×2 to 10×10) and the power `n` (negative if `A` is invertible)
3. Fill the grid, paste a matrix, or load an example (K3, P3, symmetric, Jordan, rotation)
4. Click **Calcular Aⁿ**
5. Download the PDF report if you want a numerical approximation, tick **evalf**

### Tests
```bash
python -m unittest tests.test_engine -v
```

### License
MIT License — academic and educational use welcome.

---

## Español

### Descripción
Aplicación web (Streamlit) que calcula la n-ésima potencia de una matriz cuadrada con **aritmética exacta** (`sympy.Matrix`). Si `A` es diagonalizable usa `Aⁿ = P Dⁿ P⁻¹`; si no, la forma de Jordan. Nació como proyecto final de Álgebra Lineal para matrices de adyacencia y ahora admite matrices generales sobre ℝ o ℂ.

### Características
- **Cálculo exacto**: enteros, racionales (`1/2`) y decimales como `Rational` — no inventa fracciones desde floats
- **Modos Álgebra / Grafo**: en Grafo, `(Aⁿ)ᵢⱼ` cuenta **recorridos** de longitud `n` (pueden repetir vértices)
- **Cuerpo ℝ o ℂ**: la rotación 90° no diagonaliza sobre ℝ; sí sobre ℂ
- **Forma de Jordan** cuando geo &lt; alg (el flujo no se corta)
- **Simétrica real**: `P` ortogonal y **P⁻¹ = Pᵀ**
- **Polinomio característico**, sistemas si `n ≤ 4`, `e^{tA}` opcional
- **Grafo dirigido vs no dirigido** (`A ≠ Aᵀ`) con DOT
- **Descarga PDF** (ReportLab, sin diálogos de archivo)

### Requisitos
- Python 3.10+
- sympy, streamlit, reportlab (`pip install -r requirements.txt`)

### Instalación
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Uso
```bash
streamlit run app.py
```
o:
```bash
python main.py
```
o:
```bash
python -m matrix_diagonalization
```

1. Elige **Álgebra** o **Grafo**, y el cuerpo **ℝ** o **ℂ**
2. Orden (2×2 a 10×10) y potencia `n` (negativa si `A` es invertible)
3. Rellena la grilla, pega texto o carga un ejemplo (K3, P3, simétrica, Jordan, rotación)
4. Pulsa **Calcular Aⁿ**
5. Descarga el PDF; marca **evalf** si quieres una aproximación numérica

### Pruebas
```bash
python -m unittest tests.test_engine -v
```

### Licencia
Licencia MIT — uso académico y educativo.
