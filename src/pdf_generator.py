#src/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
import os

def create_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4  # Usar el tamaño de página A4

    # Definir los márgenes
    top_margin = 22 * mm  # Margen superior
    side_margin = 21 * mm  # Margen lateral   25 mucho   20 poco
    banner_height = 30 * mm  # Altura del banner

    # Cargar y dibujar la imagen del banner con márgenes
    banner_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'banner.jpg')
    c.drawImage(banner_path, side_margin, height - top_margin - banner_height, width - 2 * side_margin, banner_height, preserveAspectRatio=True, anchor='n')

    # Asegurarse de que las claves existen en el diccionario
    nombre_proyecto = data.get('nombre_proyecto', 'N/A') if data else 'N/A'
    presupuesto_total = data.get('presupuesto_total', 'N/A') if data else 'N/A'
    presupuesto_gastado = data.get('presupuesto_gastado', 'N/A') if data else 'N/A'

    text_start = height - top_margin - banner_height - 15 * mm  # Espacio debajo del banner

    c.drawString(side_margin, text_start, f"Proyecto: {nombre_proyecto}")
    c.drawString(side_margin, text_start - 15 * mm, f"Presupuesto Total: ${presupuesto_total}")
    c.drawString(side_margin, text_start - 30 * mm, f"Presupuesto Gastado: ${presupuesto_gastado}")

    # Finaliza el PDF
    c.save()
