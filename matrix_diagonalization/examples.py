"""Matrices de ejemplo para la interfaz."""

EXAMPLES = {
    "K3 (completo 3×3)": {
        "size": 3,
        "power": 3,
        "mode": "graph",
        "field": "R",
        "matrix": [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
        ],
        "note": "Grafo completo: (Aⁿ)ᵢⱼ cuenta recorridos de longitud n.",
    },
    "Camino P3": {
        "size": 3,
        "power": 2,
        "mode": "graph",
        "field": "R",
        "matrix": [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ],
        "note": "Camino de 3 vértices (no dirigido).",
    },
    "Grafo dirigido": {
        "size": 3,
        "power": 2,
        "mode": "graph",
        "field": "R",
        "matrix": [
            [0, 1, 0],
            [0, 0, 1],
            [1, 0, 0],
        ],
        "note": "Ciclo dirigido: A ≠ Aᵀ.",
    },
    "Simétrica ponderada": {
        "size": 2,
        "power": 4,
        "mode": "algebra",
        "field": "R",
        "matrix": [
            [2, 1],
            [1, 2],
        ],
        "note": "Simétrica: diagonalizable con P ortogonal, P⁻¹ = Pᵀ.",
    },
    "No diagonalizable": {
        "size": 2,
        "power": 3,
        "mode": "algebra",
        "field": "R",
        "matrix": [
            [1, 1],
            [0, 1],
        ],
        "note": "Bloque de Jordan: alg > geo. Se usa J para Aⁿ.",
    },
    "Autovalores complejos": {
        "size": 2,
        "power": 2,
        "mode": "algebra",
        "field": "R",
        "matrix": [
            [0, -1],
            [1, 0],
        ],
        "note": "Rotación 90°. No diagonaliza sobre ℝ; sí sobre ℂ.",
    },
    "Racional 1/2": {
        "size": 2,
        "power": 2,
        "mode": "algebra",
        "field": "R",
        "matrix": [
            ["1/2", 0],
            [0, "3/2"],
        ],
        "note": "Entradas racionales exactas.",
    },
}


def default_grid(size: int, mode: str) -> list:
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            if mode == "graph":
                row.append("0" if i == j else "1")
            else:
                row.append("0")
        grid.append(row)
    return grid
