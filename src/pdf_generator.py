#src/pdf_generator.py
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def create_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Asume tamaño de carta

    # Cargar y dibujar la imagen del banner
    banner_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'banner.jpg')
    c.drawImage(banner_path, 0, height - inch, width, inch)  # Asumiendo que el banner tiene 1 pulgada de altura

    # Asegurarse de que las claves existen en el diccionario
    nombre_proyecto = data.get('nombre_proyecto', 'N/A') if data else 'N/A'
    presupuesto_total = data.get('presupuesto_total', 'N/A') if data else 'N/A'
    presupuesto_gastado = data.get('presupuesto_gastado', 'N/A') if data else 'N/A'

    c.drawString(100, height - 1.5 * inch, f"Proyecto: {nombre_proyecto}")
    c.drawString(100, height - 1.75 * inch, f"Presupuesto Total: ${presupuesto_total}")
    c.drawString(100, height - 2 * inch, f"Presupuesto Gastado: ${presupuesto_gastado}")

    # Finaliza el PDF
    c.save()
