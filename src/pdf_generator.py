#src/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

def set_pdf_title(c, filename):
    title = os.path.splitext(os.path.basename(filename))[0]
    c.setTitle(title)

def draw_banner(c, width, height, side_margin, top_margin, banner_height):
    banner_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'banner.jpg')
    c.drawImage(banner_path, side_margin, height - top_margin - banner_height, 
                width - 2 * side_margin, banner_height, 
                preserveAspectRatio=True, anchor='n')

def create_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4  # Usar el tamaño de página A4

    # Extrae el nombre base del archivo para usarlo como título del PDF
    set_pdf_title(c, filename)

    # Definir los márgenes y dimensiones del banner
    top_margin = 22 * mm
    side_margin = 21 * mm
    banner_height = 30 * mm
    sub_banner_text_size = 8


    # Cargar y dibujar la imagen del banner con márgenes
    draw_banner(c, width, height, side_margin, top_margin, banner_height)

    # Texto debajo del banner
    sub_banner_text_left_1 = "Cooperativa de Trabajo MADYGRAF LTDA"
    sub_banner_text_left_2 = "Ruta panamerica 36.700 - Garin - 1618"
    sub_banner_text_left_3 = "C.U.I.T.: 33 71465177 9"
    sub_banner_text_left_4 = "Teléfono: 11 4035-5771"
    sub_banner_text_left_5 = "Presupuesto para:"
    sub_banner_text_left_6 = "Cliente" # deberá ser dinámico
    sub_banner_text_right_1_a = "Fecha"
    sub_banner_text_right_1_b = "26/12/2023" # deberá ser dinámico
    sub_banner_text_right_2_a = "N° de presupuesto"
    sub_banner_text_right_2_b = "0001" # deberá ser dinámico
    sub_banner_text_right_3_a = "Presupuesto válido hasta:" 
    sub_banner_text_right_3_b = "31/12/2023" # deberá ser dinámico
    
    sub_banner_text_size = 8
    c.setFont("Helvetica-Bold", sub_banner_text_size)  
    c.drawString(side_margin,                   height - top_margin - banner_height - 4 * mm,   sub_banner_text_left_1)
    c.drawString(width - side_margin - 40 * mm, height - top_margin - banner_height - 4 * mm,   sub_banner_text_right_1_a)
    c.drawString(width - side_margin - 55 * mm, height - top_margin - banner_height - 8 * mm,  sub_banner_text_right_2_a)
    c.drawString(side_margin,                   height - top_margin - banner_height - 24 * mm,  sub_banner_text_left_5)
    c.drawString(width - side_margin - 60 * mm, height - top_margin - banner_height - 24 * mm,  sub_banner_text_right_3_a)
    c.setFont("Helvetica", sub_banner_text_size)  
    c.drawRightString(width - side_margin,      height - top_margin - banner_height - 4 * mm,   sub_banner_text_right_1_b)
    c.drawString(side_margin,                   height - top_margin - banner_height - 8 * mm,  sub_banner_text_left_2)
    c.drawString(side_margin,                   height - top_margin - banner_height - 12 * mm,  sub_banner_text_left_3)
    c.drawString(side_margin,                   height - top_margin - banner_height - 16 * mm,  sub_banner_text_left_4)
    c.drawRightString(width - side_margin,      height - top_margin - banner_height - 10 * mm,  sub_banner_text_right_2_b)
    c.drawString(side_margin,                   height - top_margin - banner_height - 28 * mm,  sub_banner_text_left_6)
    c.drawRightString(width - side_margin,      height - top_margin - banner_height - 24 * mm,  sub_banner_text_right_3_b)


    c.save()
