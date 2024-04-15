#src/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import os
import datetime

custom_color = colors.Color(31/255, 73/255, 125/255)

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
    draw_table(c, data, width, height, height - top_margin - banner_height - 53*mm, side_margin)
    c.save()

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

def draw_table(c, data, width, height, start_y, side_margin):
    # Datos de la tabla
    table_data = [
        ["Vendedor", "Nombre", "Fecha de envío", "Condiciones"],
        [1497, "Najarro Eymy", "a convenir", "50% anticipo"]
    ]

    # Ancho disponible para la tabla, ajustando los márgenes laterales
    table_width = width - 2 * side_margin

    # Estilo de la tabla
    table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), custom_color),  # Fondo del color definido para la cabecera
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),  # Fuente en negrita para la cabecera
        ('FONTNAME', (1,0), (-1,-1), 'Helvetica'),  # Fuente normal para los datos
        ('GRID', (0,0), (-1,-1), 1, custom_color),  # Bordes de las celdas del mismo color que la cabecera
        ('BOX', (0,0), (-1,-1), 2, custom_color)  # Bordes externos de la tabla
    ])

    # Crear la tabla y configurar el estilo
    table = Table(table_data, colWidths=[table_width*0.2, table_width*0.3, table_width*0.3, table_width*0.2])
    table.setStyle(table_style)

    # Dibujar la tabla en el canvas, usando los mismos márgenes laterales que el banner
    table.wrapOn(c, table_width, height)  # 'wrap' prepara la tabla para ser dibujada
    table.drawOn(c, side_margin, start_y)  # 'draw' coloca la tabla en el canvas


