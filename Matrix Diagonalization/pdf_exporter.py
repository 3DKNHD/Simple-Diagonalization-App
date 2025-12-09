from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import filedialog, messagebox


class PDFExporter:
    @staticmethod
    def export_to_pdf(results_text):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar PDF como"
        )

        if not filepath:
            return False

        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        text = c.beginText(40, height - 50)
        text.setFont("Courier", 9)

        contenido = results_text.split("\n")

        for line in contenido:
            text.textLine(line)
            if text.getY() < 40:
                c.drawText(text)
                c.showPage()
                text = c.beginText(40, height - 50)
                text.setFont("Courier", 9)

        c.drawText(text)
        c.save()

        messagebox.showinfo("PDF generado", f"Archivo guardado en:\n{filepath}")
        return True