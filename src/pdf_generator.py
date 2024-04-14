#src/pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Asume tamaño de carta

    # Valores por defecto para cuando los datos no están completos
    nombre_proyecto = data.get('nombre_proyecto', 'N/A') if data else 'N/A'
    presupuesto_total = data.get('presupuesto_total', 'N/A') if data else 'N/A'
    presupuesto_gastado = data.get('presupuesto_gastado', 'N/A') if data else 'N/A'

    c.drawString(100, 750, "Reporte de Presupuesto")
    c.drawString(100, 735, f"Proyecto: {nombre_proyecto}")
    c.drawString(100, 720, f"Presupuesto Total: ${presupuesto_total}")
    c.drawString(100, 705, f"Presupuesto Gastado: ${presupuesto_gastado}")

    # Finaliza el PDF
    c.save()
