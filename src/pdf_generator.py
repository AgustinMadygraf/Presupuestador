from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Asume tamaño de carta

    # Aquí añadirías la lógica para añadir texto e imágenes al PDF
    c.drawString(100, 750, "Reporte de Presupuesto")
    c.drawString(100, 735, f"Proyecto: {data['nombre_proyecto']}")
    c.drawString(100, 720, f"Presupuesto Total: ${data['presupuesto_total']}")
    c.drawString(100, 705, f"Presupuesto Gastado: ${data['presupuesto_gastado']}")

    # Finaliza el PDF
    c.save()

# Ejemplo de uso:
# create_pdf({'nombre_proyecto': 'Construcción', 'presupuesto_total': 10000, 'presupuesto_gastado': 3000}, 'reporte.pdf')
