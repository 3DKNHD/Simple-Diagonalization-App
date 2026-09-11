"""Informe PDF estructurado. Sin Tkinter: solo bytes."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .formatters import expr_str, format_eigenvalue_block, format_walks, matrix_ascii
from .models import CalculationResult

_FONT_CANDIDATES = [
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    Path("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
    Path("/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf"),
]


def _font_name() -> str:
    for path in _FONT_CANDIDATES:
        if path.is_file():
            try:
                pdfmetrics.registerFont(TTFont("AppSans", str(path)))
                return "AppSans"
            except Exception:
                continue
    return "Helvetica"


def _matrix_table(matrix, font_name: str) -> Table:
    data = [
        [expr_str(matrix[i, j]) for j in range(matrix.cols)]
        for i in range(matrix.rows)
    ]
    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (-1, -1), font_name),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("BACKGROUND", (0, 0), (-1, -1), colors.Color(0.95, 0.95, 0.97)),
            ]
        )
    )
    return table


def _p(text: str, style) -> Paragraph:
    safe = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
    return Paragraph(safe, style)


def build_pdf_bytes(result: CalculationResult) -> bytes:
    font_name = _font_name()
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "AppTitle",
        parent=styles["Title"],
        fontName=font_name,
        fontSize=16,
        spaceAfter=12,
    )
    heading = ParagraphStyle(
        "AppHeading",
        parent=styles["Heading2"],
        fontName=font_name,
        fontSize=12,
        spaceBefore=10,
        spaceAfter=6,
    )
    body = ParagraphStyle(
        "AppBody",
        parent=styles["Normal"],
        fontName=font_name,
        fontSize=9,
        leading=12,
    )

    story = []
    story.append(_p("Potencias por diagonalización", title))
    mode = "Grafo" if result.mode == "graph" else "Álgebra"
    field = "ℂ" if result.field == "C" else "ℝ"
    story.append(
        _p(
            f"Modo {mode} · cuerpo {field} · n = {result.power} · "
            f"estado: {result.status}",
            body,
        )
    )
    story.append(Spacer(1, 0.12 * inch))

    story.append(_p("Matriz A", heading))
    story.append(_matrix_table(result.matrix, font_name))
    story.append(_p(f"det(A) = {expr_str(result.det)}", body))

    story.append(_p("Polinomio característico", heading))
    story.append(_p(f"p(λ) = det(λI − A) = {expr_str(result.charpoly)}", body))

    story.append(_p("Autovalores y multiplicidades", heading))
    for info in result.eigenvalues:
        story.append(_p(format_eigenvalue_block(info), body))
        story.append(Spacer(1, 0.06 * inch))

    for msg in result.messages:
        story.append(_p(msg, body))

    if result.status == "diagonalizable" and result.P is not None:
        story.append(_p("Matrices P, D y P⁻¹", heading))
        if result.uses_p_transpose:
            story.append(_p("P es ortogonal: P⁻¹ = Pᵀ.", body))
        story.append(_p("P", body))
        story.append(_matrix_table(result.P, font_name))
        story.append(_p("D", body))
        story.append(_matrix_table(result.D, font_name))
        story.append(_p("P⁻¹", body))
        story.append(_matrix_table(result.P_inv, font_name))
        if result.D_power is not None:
            story.append(_p(f"D^{result.power}", heading))
            story.append(_matrix_table(result.D_power, font_name))

    if result.jordan_J is not None:
        story.append(_p("Forma de Jordan A = P J P⁻¹", heading))
        story.append(_p("P", body))
        story.append(_matrix_table(result.jordan_P, font_name))
        story.append(_p("J", body))
        story.append(_matrix_table(result.jordan_J, font_name))
        if result.jordan_J_power is not None:
            story.append(_p(f"J^{result.power}", body))
            story.append(_matrix_table(result.jordan_J_power, font_name))

    if result.result_power is not None:
        story.append(_p(f"A^{result.power}", heading))
        story.append(_matrix_table(result.result_power, font_name))
        story.append(_p(matrix_ascii(result.result_power), body))

    if result.mode == "graph":
        kind = "dirigido" if result.is_directed else "no dirigido"
        story.append(_p(f"Interpretación en grafos ({kind})", heading))
        story.append(_p(format_walks(result), body))

    if result.exp_tA is not None:
        story.append(_p("exponencial e^{tA}", heading))
        story.append(_matrix_table(result.exp_tA, font_name))

    buffer = BytesIO()
    SimpleDocTemplate(
        buffer,
        pagesize=letter,
        title="Diagonalización",
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.6 * inch,
        bottomMargin=0.6 * inch,
    ).build(story)
    return buffer.getvalue()
