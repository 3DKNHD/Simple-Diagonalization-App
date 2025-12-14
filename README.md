# Matrix Diagonalization Power Calculator / Calculadora de Potencia Matricial por Diagonalización

## English

### Project Description
A Python application that computes the n-th power of an adjacency matrix using diagonalization (Cⁿ = P Dⁿ P⁻¹). Developed as a final project for Linear Algebra, this tool visualizes the step-by-step diagonalization process and generates detailed PDF reports.

### Features
- **Diagonalization Method**: Computes matrix powers via C = PDP⁻¹ → Cⁿ = PDⁿP⁻¹
- **Adjacency Matrix Support**: Currently supports unweighted adjacency matrices (0s and 1s only)
- **Interactive GUI**: User-friendly interface with matrix input and real-time validation
- **PDF Export**: Generates professional reports with complete calculation steps
- **Error Handling**: Validates matrix properties and provides clear error messages
- **Dark/Light Mode**: Toggleable interface themes

### Requirements
- Python 3.8+
- NumPy (>=1.21.0) - for matrix operations and eigenvalue decomposition
- ReportLab (>=3.6.0) - for PDF report generation

### Installation
1. Clone or download the project
2. Install dependencies:
```bash
pip install numpy>=1.21.0 reportlab>=3.6.0
```

### Project Structure
```
matrix_diagonalization/
├── main.py                 # Main entry point - launches the application
├── matrix_logic.py         # Core matrix calculations and diagonalization logic
├── pdf_exporter.py         # PDF export functionality using ReportLab
├── gui.py                  # Graphical user interface (Tkinter)
└── requirements.txt        # Python dependencies
```

### Usage

#### Launch the Application
```bash
python main.py
```

#### Using the GUI
1. Set matrix size (2×2 to 10×10)
2. Enter matrix values (0s and 1s for adjacency matrices)
3. Specify the power (n)
4. Click "Calculate Cⁿ" to compute the result
5. Use "Export to PDF" to save the calculation steps

#### Example Matrix
For a 3×3 adjacency matrix of a simple path graph:
```
[0, 1, 1]
[1, 0, 1]
[1, 1, 0]
```
Calculating C³ shows the number of paths of length 3 between nodes.

### Calculation Process
1. **Eigenvalue/Vector Computation**: Finds eigenvalues and eigenvectors of the matrix
2. **Diagonalization**: Constructs P (eigenvectors), D (diagonal eigenvalues), and P⁻¹
3. **Power Calculation**: Computes Dⁿ (diagonal matrix with eigenvaluesⁿ)
4. **Reconstruction**: Calculates Cⁿ = P × Dⁿ × P⁻¹
5. **Verification**: Compares with direct computation (if available)

### PDF Report Contents
- Input matrix and parameters
- Eigenvalues and eigenvectors (grouped by eigenvalue)
- Matrices P, D, and P⁻¹
- Dⁿ calculation
- Final result Cⁿ
- Interpretation in graph theory context
- Timestamp and calculation details


### Academic Context
This project demonstrates:
- Matrix diagonalization theory
- Eigenvalue decomposition applications
- Graph theory connections (adjacency matrix powers)
- Numerical stability considerations
- Professional technical reporting

### License
MIT License - For academic and educational use

---

## Español

### Descripción del Proyecto
Una aplicación Python que calcula la n-ésima potencia de una matriz de adyacencia usando diagonalización (Cⁿ = P Dⁿ P⁻¹). Desarrollada como proyecto final de Álgebra Lineal, esta herramienta visualiza el proceso de diagonalización paso a paso y genera reportes PDF detallados.

### Características
- **Método de Diagonalización**: Calcula potencias matriciales mediante C = PDP⁻¹ → Cⁿ = PDⁿP⁻¹
- **Soporte para Matrices de Adyacencia**: Actualmente solo matrices no ponderadas (solo 0s y 1s)
- **Interfaz Gráfica Interactiva**: Interfaz amigable con entrada matricial y validación en tiempo real
- **Exportación PDF**: Genera reportes profesionales con pasos completos de cálculo
- **Manejo de Errores**: Valida propiedades matriciales y proporciona mensajes de error claros
- **Modo Oscuro/Claro**: Temas de interfaz intercambiables

### Requisitos
- Python 3.8+
- NumPy (>=1.21.0) - para operaciones matriciales y descomposición de valores propios
- ReportLab (>=3.6.0) - para generación de reportes PDF

### Instalación
1. Clona o descarga el proyecto
2. Instala las dependencias:
```bash
pip install numpy>=1.21.0 reportlab>=3.6.0
```

### Estructura del Proyecto
```
matrix_diagonalization/
├── main.py                 # Punto de entrada principal - lanza la aplicación
├── matrix_logic.py         # Cálculos matriciales principales y lógica de diagonalización
├── pdf_exporter.py         # Funcionalidad de exportación PDF usando ReportLab
├── gui.py                  # Interfaz gráfica de usuario (Tkinter)
└── requirements.txt        # Dependencias de Python
```

### Uso

#### Lanzar la Aplicación
```bash
python main.py
```

#### Usando la Interfaz Gráfica
1. Establece el tamaño de la matriz (2×2 a 10×10)
2. Ingresa los valores de la matriz (0s y 1s para matrices de adyacencia)
3. Especifica la potencia (n)
4. Haz clic en "Calcular Cⁿ" para computar el resultado
5. Usa "Exportar a PDF" para guardar los pasos del cálculo

#### Matriz de Ejemplo
Para una matriz de adyacencia 3×3 de un grafo camino simple:
```
[0, 1, 1]
[1, 0, 1]
[1, 1, 0]
```
Calcular C³ muestra el número de caminos de longitud 3 entre nodos.

### Proceso de Cálculo
1. **Cálculo de Valores/Vectores Propios**: Encuentra valores y vectores propios de la matriz
2. **Diagonalización**: Construye P (vectores propios), D (valores propios diagonales) y P⁻¹
3. **Cálculo de Potencia**: Computa Dⁿ (matriz diagonal con valores propiosⁿ)
4. **Reconstrucción**: Calcula Cⁿ = P × Dⁿ × P⁻¹
5. **Verificación**: Compara con cálculo directo (si está disponible)

### Contenido del Reporte PDF
- Matriz de entrada y parámetros
- Valores y vectores propios (agrupados por valor propio)
- Matrices P, D y P⁻¹
- Cálculo de Dⁿ
- Resultado final Cⁿ
- Interpretación en contexto de teoría de grafos
- Marca de tiempo y detalles del cálculo

### Contexto Académico
Este proyecto demuestra:
- Teoría de diagonalización de matrices
- Aplicaciones de descomposición en valores propios
- Conexiones con teoría de grafos (potencias de matrices de adyacencia)
- Consideraciones de estabilidad numérica
- Generación de reportes técnicos profesionales

### Licencia
Licencia MIT - Para uso académico y educativo

---

## Future Development / Desarrollo Futuro
**English**: The current version supports unweighted adjacency matrices. I'm working on a more general version that will handle weighted matrices.

**Español**: La versión actual soporta matrices de adyacencia no ponderadas. Estoy trabajando en una versión más general que manejará matrices ponderadas.