"""Grafo en DOT/SVG y tabla de recorridos."""

from __future__ import annotations

import math
from typing import Optional

from sympy import Matrix, simplify

from .models import WalkEntry


def is_directed(A: Matrix) -> bool:
    return A != A.T


def walk_entries(power_matrix: Matrix) -> list:
    n = power_matrix.rows
    rows = []
    for i in range(n):
        for j in range(n):
            rows.append(
                WalkEntry(src=i + 1, dst=j + 1, count=simplify(power_matrix[i, j]))
            )
    return rows


def to_dot(A: Matrix, directed: Optional[bool] = None) -> str:
    if directed is None:
        directed = is_directed(A)
    n = A.rows
    kind = "digraph" if directed else "graph"
    op = "->" if directed else "--"
    lines = [
        f"{kind} G {{",
        "  graph [rankdir=LR];",
        "  node [shape=circle, fontsize=12];",
    ]
    for i in range(n):
        lines.append(f"  {i + 1};")

    if directed:
        for i in range(n):
            for j in range(n):
                if A[i, j] == 0:
                    continue
                label = "" if A[i, j] == 1 else f' [label="{A[i, j]}"]'
                lines.append(f"  {i + 1} {op} {j + 1}{label};")
    else:
        seen = set()
        for i in range(n):
            for j in range(n):
                if A[i, j] == 0:
                    continue
                a, b = (i, j) if i <= j else (j, i)
                if (a, b) in seen:
                    continue
                seen.add((a, b))
                lines.append(f"  {i + 1} {op} {j + 1};")
    lines.append("}")
    return "\n".join(lines)


def to_svg(A: Matrix, directed: bool | None = None, size: int = 340) -> str:
    if directed is None:
        directed = is_directed(A)
    n = A.rows
    cx = cy = size / 2
    radius = size / 2 - 36
    positions = []
    for k in range(n):
        ang = -math.pi / 2 + (2 * math.pi * k / max(n, 1))
        positions.append((cx + radius * math.cos(ang), cy + radius * math.sin(ang)))

    marker = ""
    if directed:
        marker = (
            '<marker id="arrow" viewBox="0 0 10 10" refX="10" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="#333"/></marker>'
        )
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">',
        f"<defs>{marker}</defs>",
        f'<rect width="{size}" height="{size}" fill="white"/>',
    ]

    def edge(i, j):
        x1, y1 = positions[i]
        x2, y2 = positions[j]
        if i == j:
            mark = ' marker-end="url(#arrow)"' if directed else ""
            return (
                f'<path d="M {x1:.1f} {y1 - 16:.1f} '
                f'C {x1 + 28:.1f} {y1 - 48:.1f}, {x1 - 28:.1f} {y1 - 48:.1f}, '
                f'{x1:.1f} {y1 - 16:.1f}" fill="none" stroke="#333" '
                f'stroke-width="1.5"{mark}/>'
            )
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy) or 1
        shrink = 16
        sx, sy = x1 + dx / length * shrink, y1 + dy / length * shrink
        ex, ey = x2 - dx / length * shrink, y2 - dy / length * shrink
        mark = ' marker-end="url(#arrow)"' if directed else ""
        return (
            f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="#333" stroke-width="1.5"{mark}/>'
        )

    if directed:
        for i in range(n):
            for j in range(n):
                if A[i, j] != 0:
                    parts.append(edge(i, j))
    else:
        seen = set()
        for i in range(n):
            for j in range(n):
                if A[i, j] == 0:
                    continue
                a, b = (i, j) if i <= j else (j, i)
                if (a, b) in seen:
                    continue
                seen.add((a, b))
                parts.append(edge(i, j))

    for i, (x, y) in enumerate(positions, start=1):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="#1976D2" stroke="#0d47a1"/>')
        parts.append(
            f'<text x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" '
            f'fill="white" font-size="12" font-family="sans-serif">{i}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)
