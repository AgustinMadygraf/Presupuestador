from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter  # Asume tamaño de carta

    # Asegurarse de que las claves existen en el diccionario
    if all(key in data for key in ['nombre_proyecto', 'presupuesto_total', 'presupuesto_gastado']):
        c.drawString(100, 750, "Reporte de Presupuesto")
        c.drawString(100, 735, f"Proyecto: {data['nombre_proyecto']}")
        c.drawString(100, 720, f"Presupuesto Total: ${data['presupuesto_total']}")
        c.drawString(100, 705, f"Presupuesto Gastado: ${data['presupuesto_gastado']}")

        # Finaliza el PDF
        c.save()
    else:
        print("Datos incompletos para generar el PDF.")
