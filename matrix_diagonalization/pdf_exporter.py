"""Exportación del cálculo a PDF."""

from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from tkinter import filedialog, messagebox

_FONT_CANDIDATES = [
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"),
    Path("/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"),
    Path("/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf"),
    Path("/usr/share/fonts/truetype/freefont/FreeMono.ttf"),
    Path("DejaVuSansMono.ttf"),
]


class PDFExporter:
    @staticmethod
    def _resolve_font():
        for path in _FONT_CANDIDATES:
            if path.is_file():
                font_name = "AppMono"
                try:
                    pdfmetrics.registerFont(TTFont(font_name, str(path)))
                    return font_name
                except Exception:
                    continue
        return "Courier"

    @staticmethod
    def _wrap_line(line, max_chars=96):
        if len(line) <= max_chars:
            return [line]
        chunks = []
        remaining = line
        while remaining:
            chunks.append(remaining[:max_chars])
            remaining = remaining[max_chars:]
        return chunks

    def export_to_pdf(self, results_text):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar PDF como",
        )
        if not filepath:
            return False

        font_name = self._resolve_font()
        pdf = canvas.Canvas(filepath, pagesize=letter)
        _, height = letter

        x_start = 40
        y_start = height - 50
        line_height = 12
        bottom_margin = 40

        text = pdf.beginText(x_start, y_start)
        text.setFont(font_name, 9)
        text.setLeading(line_height)

        for raw_line in results_text.split("\n"):
            for line in self._wrap_line(raw_line):
                text.textLine(line)
                if text.getY() < bottom_margin:
                    pdf.drawText(text)
                    pdf.showPage()
                    text = pdf.beginText(x_start, y_start)
                    text.setFont(font_name, 9)
                    text.setLeading(line_height)

        pdf.drawText(text)
        pdf.save()
        messagebox.showinfo("PDF generado", f"Archivo guardado en:\n{filepath}")
        return True
