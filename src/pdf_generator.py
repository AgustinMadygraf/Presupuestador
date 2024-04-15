#src/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os
import datetime

def set_pdf_title(c, filename):
    title = os.path.splitext(os.path.basename(filename))[0]
    c.setTitle(title)

def draw_banner(c, width, height, side_margin, top_margin, banner_height):
    banner_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'banner.jpg')
    c.drawImage(banner_path, side_margin, height - top_margin - banner_height, 
                width - 2 * side_margin, banner_height, 
                preserveAspectRatio=True, anchor='n')

from reportlab.lib.units import mm

def draw_header(c, width, height, top_margin, banner_height, side_margin, sub_banner_text_size, data):
    # Dibujar la información de la izquierda con control de estilo de fuente
    left_text_info = [
        (data['left_1'], 4, "Helvetica-Bold"), 
        (data['left_2'], 8, "Helvetica"),
        (data['left_3'], 12, "Helvetica"),
        (data['left_4'], 16, "Helvetica"),
        (data['left_5'], 24, "Helvetica-Bold"),
        (data['left_6'], 28, "Helvetica")
    ]

    # Dibujar la información de la derecha
    right_text_info = [
        (data['right_1_a'], data['right_1_b'], 4),  
        (data['right_2_a'], data['right_2_b'], 8),  
        (data['right_3_a'], data['right_3_b'], 24)
    ]

    # Iterar sobre la información de la izquierda y aplicar el estilo de fuente adecuado
    for text, offset, font_style in left_text_info:
        c.setFont(font_style, sub_banner_text_size)  # Aplica el estilo de fuente aquí
        c.drawString(side_margin, height - top_margin - banner_height - offset * mm, text)

    # Dibujar la información de la derecha con un estilo uniforme
    c.setFont("Helvetica-Bold", sub_banner_text_size)
    for label, value, offset in right_text_info:
        label_width = c.stringWidth(label, "Helvetica-Bold", sub_banner_text_size)
        c.drawString(width - side_margin - label_width - 15 * mm, height - top_margin - banner_height - offset * mm, label)
        c.drawRightString(width - side_margin, height - top_margin - banner_height - offset * mm, value)


def create_pdf(data, filename):
    # Definir valores predeterminados para el modo de prueba
    default_data = {
        'left_1': "Cooperativa de Trabajo MADYGRAF LTDA",
        'left_2': "Ruta panamericana 36.700 - Garin - 1618",
        'left_3': "C.U.I.T.: 33 71465177 9",
        'left_4': "Teléfono: 11 4035-5771",
        'left_5': "Presupuesto para:",
        'left_6': "Cliente Desconocido",
        'right_1_a': "Fecha",
        'right_1_b': datetime.datetime.now().strftime("%d/%m/%Y"),
        'right_2_a': "N° de presupuesto",
        'right_2_b': "Desconocido",
        'right_3_a': "Presupuesto válido hasta:",
        'right_3_b': (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%d/%m/%Y")
    }

    # Actualizar el diccionario data con los valores predeterminados si alguno falta
    if data is None:
        data = default_data
    else:
        for key in default_data:
            data.setdefault(key, default_data[key])

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    set_pdf_title(c, filename)
    top_margin = 22 * mm
    side_margin = 21 * mm
    banner_height = 30 * mm
    sub_banner_text_size = 8

    draw_banner(c, width, height, side_margin, top_margin, banner_height)
    draw_header(c, width, height, top_margin, banner_height, side_margin, sub_banner_text_size, data)

    c.save()

