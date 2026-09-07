"""Matrices de ejemplo para la interfaz."""

EXAMPLES = {
    "K3 (completo 3×3)": {
        "size": 3,
        "power": 3,
        "adjacency": True,
        "matrix": [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
        ],
        "note": "Grafo completo: (Cⁿ)ᵢⱼ cuenta caminos de longitud n.",
    },
    "Camino P3": {
        "size": 3,
        "power": 2,
        "adjacency": True,
        "matrix": [
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0],
        ],
        "note": "Camino de 3 vértices.",
    },
    "Simétrica ponderada": {
        "size": 2,
        "power": 4,
        "adjacency": False,
        "matrix": [
            [2, 1],
            [1, 2],
        ],
        "note": "Matriz simétrica (siempre diagonalizable sobre ℝ).",
    },
    "No diagonalizable": {
        "size": 2,
        "power": 3,
        "adjacency": False,
        "matrix": [
            [1, 1],
            [0, 1],
        ],
        "note": "Bloque de Jordan: un solo autovector independiente.",
    },
    "Autovalores complejos": {
        "size": 2,
        "power": 2,
        "adjacency": False,
        "matrix": [
            [0, -1],
            [1, 0],
        ],
        "note": "Rotación 90°: autovalores ±i, no diagonalizable sobre ℝ.",
    },
}
