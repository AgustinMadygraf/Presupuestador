#src/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
import os
from logs.config_logger import configurar_logging
from datetime import datetime
from data_definitions import custom_color1, custom_color2, data_test
from reportlab.lib import colors

logger = configurar_logging()


def create_pdf(data, filename):
    if data is None:
        data = data_test
    else:
        for key in data_test:
            data.setdefault(key, data_test[key])

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    set_pdf_title(c, filename)
    top_margin = 22 * mm
    side_margin = 21 * mm
    banner_height = 30 * mm
    sub_banner_text_size = 8

    draw_banner(c,  width,  height,     side_margin,                                     top_margin,     banner_height,  data)
    draw_header(c,  width,  height,     top_margin,                                      banner_height,  side_margin,    sub_banner_text_size, data)
    draw_table (c,  width,  height,     height - top_margin - banner_height - 53*mm,     side_margin,    data['table1_data'])
    draw_table (c,  width,  height,     height - top_margin - banner_height - 120*mm,    side_margin,    data['table2_data'])
    draw_footer(c,  width,  height,     top_margin,                                                      data['footer_text_info'])
    c.save()

def draw_footer(c, width, height, top_margin, footer_text_info):
    # Definición de la posición inicial del pie de página
    footer_start_y = height - top_margin - 155 * mm  # Ajusta según sea necesario
    left_margin = 21 * mm
    interlinea = 10 * mm

    # Iterar sobre cada fila de la información del pie de página
    for index, info in enumerate(footer_text_info):
        # Extraer los elementos de la fila
        line1_text  = info[0] if len(info) > 0 else ""
        line2_text  = info[1] if len(info) > 1 else ""
        right_label = info[2] if len(info) > 2 else ""
        right_value = info[3] if len(info) > 3 else ""

        # Configurar la fuente y dibujar los textos
        c.setFont("Helvetica", 8)
        c.drawString(left_margin, footer_start_y - index * interlinea, line1_text) 
        
        # Texto secundario (line2_text) opcional se dibuja un poco más a la derecha
        if line2_text:
            c.drawString(left_margin + 30 * mm, footer_start_y - index * interlinea, line2_text) 

        # Dibujar las etiquetas y valores en la parte derecha
        right_text_x = width - 80 * mm
        if right_label:
            c.setFont("Helvetica-Bold", 8)
            c.drawString(right_text_x, footer_start_y - index * interlinea, right_label)
        if right_value:
            c.setFont("Helvetica", 8)
            c.drawString(right_text_x + 30 * mm, footer_start_y - index * interlinea, right_value)

def set_pdf_title(c, filename):
    title = os.path.splitext(os.path.basename(filename))[0]
    c.setTitle(title)

def draw_banner(c, width, height, side_margin, top_margin, banner_height, data):
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

def draw_table(c, width, height, start_y, side_margin, table_data):
    # Ancho disponible para la tabla, ajustando los márgenes laterales
    table_width = width - 2 * side_margin

    # Estilo de la tabla
    table_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), custom_color1),  # Fondo del color definido para la cabecera
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),  # Fuente en negrita para la cabecera
        ('FONTNAME', (1,0), (-1,-1), 'Helvetica'),  # Fuente normal para los datos
        ('FONTSIZE', (0,0), (-1,-1), 8),  # Tamaño de letra para todas las celdas
        ('GRID', (0,0), (-1,-1), 1, custom_color1),  # Bordes de las celdas del mismo color que la cabecera
        ('BOX', (0,0), (-1,-1), 2, custom_color1),  # Bordes externos de la tabla
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, custom_color2])  # Alternar fondo de las filas
    ])

    # Ajustar los porcentajes de ancho de las columnas
    colWidths = [table_width * 0.16, table_width * 0.48, table_width * 0.18, table_width * 0.18]

    # Crear la tabla y configurar el estilo
    table = Table(table_data, colWidths=colWidths)
    table.setStyle(table_style)

    # Dibujar la tabla en el canvas, usando los mismos márgenes laterales que el banner
    table.wrapOn(c, table_width, height)  
    table.drawOn(c, side_margin, start_y) 

def handle_generate_pdf():
    try:
        presupuesto_id = get_presupuesto_id()
        file_path = prepare_output_directory()

        # Verificar si es el modo test y generar el nombre del archivo en consecuencia.´
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        if presupuesto_id is None:
            file_name = f"test_{current_time}.pdf"
            data = None
        else:
            file_name = (f"presupuesto_N{presupuesto_id}_{current_time}.pdf")
            data = None # Provisorio. Obtener los datos del presupuesto desde la base de datos
        full_file_path = os.path.join(file_path, file_name)
        logger.debug(f"Ruta del archivo configurada: {full_file_path}")
        print(f"Generando PDF en {full_file_path}")
        create_pdf(data, full_file_path)
        logger.info("PDF generado exitosamente.")
        
        # Abrir el PDF automáticamente después de crearlo
        os.startfile(full_file_path)
        print(f"Abriendo el archivo {full_file_path}")
        
    except Exception as e:
        logger.error(f"Error al generar el PDF: {e}", exc_info=True)
        print(f"Se produjo un error al generar el PDF: {e}")

def get_presupuesto_id():
    try:
        return int(input("ID del presupuesto para generar el PDF: "))
    except ValueError:
        logger.info("Modo TEST activado: Generando PDF vacío.")
        return None
    
def prepare_output_directory():
    # Detecta el directorio base del proyecto de manera dinámica
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    output_dir = os.path.join(base_dir, 'Presupuestador\generated_pdfs')
    # Crea el directorio si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir
