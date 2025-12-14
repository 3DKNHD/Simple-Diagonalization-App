from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from tkinter import filedialog, messagebox
import os


class PDFExporter:
    @staticmethod
    def export_to_pdf(results_text):
        try:
            pdfmetrics.registerFont(TTFont('DejaVuSansMono', 'DejaVuSansMono.ttf'))
            font_name = 'DejaVuSansMono'
        except:
            try:
                pdfmetrics.registerFont(TTFont('CourierNew', 'cour.ttf'))
                font_name = 'CourierNew'
            except:
                try:
                    pdfmetrics.registerFont(TTFont('Consolas', 'consola.ttf'))
                    font_name = 'Consolas'
                except:
                    font_name = 'Courier'

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar PDF como"
        )

        if not filepath:
            return False

        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        x_start = 40
        y_start = height - 50
        line_height = 12
        bottom_margin = 40

        text = c.beginText(x_start, y_start)
        text.setFont(font_name, 9)
        text.setTextOrigin(x_start, y_start)
        text.setLeading(line_height)

        contenido = results_text.split("\n")

        for i, line in enumerate(contenido):
            text.textLine(line)

            if text.getY() < bottom_margin:
                c.drawText(text)
                c.showPage()
                text = c.beginText(x_start, y_start)
                text.setFont(font_name, 9)
                text.setTextOrigin(x_start, y_start)
                text.setLeading(line_height)

        c.drawText(text)
        c.save()

        messagebox.showinfo("PDF generado", f"Archivo guardado en:\n{filepath}")
        return True