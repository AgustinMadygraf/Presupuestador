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

    # Dibujar la información de la derecha, especificando estilo de fuente separado para etiqueta y valor
    right_text_info = [
        (data['right_1_a'], "Helvetica-Bold",   data['right_1_b'], "Helvetica", 4),
        (data['right_2_a'], "Helvetica-Bold",   data['right_2_b'], "Helvetica", 8),
        (data['right_3_a'], "Helvetica-Bold",   data['right_3_b'], "Helvetica", 24)
    ]

    # Iterar sobre la información de la izquierda y aplicar el estilo de fuente adecuado
    for text, offset, font_style in left_text_info:
        c.setFont(font_style, sub_banner_text_size)
        c.drawString(side_margin, height - top_margin - banner_height - offset * mm, text)

    # Iterar sobre la información de la derecha y aplicar el estilo de fuente adecuado, separando estilos para etiqueta y valor
    for label, label_font, value, value_font, offset in right_text_info:
        c.setFont(label_font, sub_banner_text_size)
        label_width = c.stringWidth(label, label_font, sub_banner_text_size)
        c.drawString(width - side_margin - label_width - 15 * mm, height - top_margin - banner_height - offset * mm, label)
        c.setFont(value_font, sub_banner_text_size)  # Cambia la fuente para el valor
        c.drawRightString(width - side_margin, height - top_margin - banner_height - offset * mm, value)


def create_pdf(data, filename):
    # Definir valores predeterminados para el modo de prueba
    default_data = {
        'left_1': "Cooperativa de Trabajo MADYGRAF LTDA",
        'left_2': "Ruta panamericana 36.700 - Garin - 1618",
        'left_3': "C.U.I.T.: 33 71465177 9",
        'left_4': "Teléfono: 11 4035-5771",
        'left_5': "Presupuesto para:",
        'left_6': "Cliente", # Cambiar por el nombre del cliente
        'right_1_a': "Fecha",
        'right_1_b': datetime.datetime.now().strftime("%d/%m/%Y"),
        'right_2_a': "N° de presupuesto",
        'right_2_b': "123",
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

