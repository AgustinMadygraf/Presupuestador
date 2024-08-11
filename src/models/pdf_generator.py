# src/models/pdf_generator.py

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from src.data_definitions import custom_color1, custom_color2, data_test
from src.logs.config_logger import LoggerConfigurator
from src.models.directory_manager import DirectoryManager

class PDFGenerator:
    """Class to generate PDF documents."""

    def __init__(self):
        """Initialize the PDFGenerator with a logger."""
        self.logger = LoggerConfigurator().configure()

    def handle_generate_pdf(self):
        """Handle the process of generating a PDF."""
        try:
            presupuesto_id = self.get_presupuesto_id()
            file_path = DirectoryManager.prepare_output_directory()

            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            if presupuesto_id is None:
                file_name = f"test_{current_time}.pdf"
                data = None
            else:
                file_name = f"presupuesto_N{presupuesto_id}_{current_time}.pdf"
                data = None  # Provisorio. Obtener los datos del presupuesto desde la base de datos
            full_file_path = os.path.join(file_path, file_name)
            self.logger.debug("Ruta del archivo configurada: %s", full_file_path)
            print(f"Generando PDF en {full_file_path}")
            self.create_pdf(data, full_file_path)
            self.logger.info("PDF generado exitosamente.")

            os.startfile(full_file_path)
            print(f"Abriendo el archivo {full_file_path}")

        except Exception as e:
            self.logger.error("Error al generar el PDF: %s", e, exc_info=True)
            print(f"Se produjo un error al generar el PDF: {e}")

    def get_presupuesto_id(self):
        """Get the presupuesto ID from user input."""
        try:
            return int(input("ID del presupuesto para generar el PDF: "))
        except ValueError:
            self.logger.info("Modo TEST activado: Generando PDF vacío.")
            return None

    def prepare_output_directory(self):
        """Prepare the output directory for the PDF."""
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        output_dir = os.path.join(base_dir, 'Presupuestador', 'generated_pdfs')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return output_dir

    def create_pdf(self, data, filename):
        """Create a PDF with the given data and filename."""
        if data is None:
            data = data_test
        else:
            for key in data_test:
                data.setdefault(key, data_test[key])

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        self.set_pdf_title(c, filename)
        top_margin = 22 * mm
        side_margin = 21 * mm
        banner_height = 30 * mm
        sub_banner_text_size = 8

        self.draw_banner(c, width, height, side_margin, top_margin, banner_height, data)
        self.draw_header(c, width, height, top_margin, banner_height, side_margin, sub_banner_text_size, data)
        self.draw_table(c, width, height, height - top_margin - banner_height - 53 * mm, side_margin, data['table1_data'])
        self.draw_table(c, width, height, height - top_margin - banner_height - 120 * mm, side_margin, data['table2_data'])
        self.draw_footer(c, width, height, top_margin, data['footer_text_info'])
        c.save()

    def set_pdf_title(self, c, filename):
        """Set the title of the PDF."""
        title = os.path.splitext(os.path.basename(filename))[0]
        c.setTitle(title)

    def draw_banner(self, c, width, height, side_margin, top_margin, banner_height, data):
        """Draw the banner on the PDF."""
        banner_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'banner.jpg'))
        if not os.path.exists(banner_path):
            self.logger.error("El archivo de banner no se encontró en la ruta: %s", banner_path)
            return
        c.drawImage(banner_path, side_margin, height - top_margin - banner_height, width - 2 * side_margin, banner_height, preserveAspectRatio=True, anchor='n')

    def draw_header(self, c, width, height, top_margin, banner_height, side_margin, sub_banner_text_size, data):
        """Draw the header on the PDF."""
        left_text_info = [
            (data['left_1'], 4, "Helvetica-Bold"),
            (data['left_2'], 8, "Helvetica"),
            (data['left_3'], 12, "Helvetica"),
            (data['left_4'], 16, "Helvetica"),
            (data['left_5'], 24, "Helvetica-Bold"),
            (data['left_6'], 28, "Helvetica")
        ]

        right_text_info = [
            (data['right_1_a'], "Helvetica-Bold", data['right_1_b'], "Helvetica", 4),
            (data['right_2_a'], "Helvetica-Bold", data['right_2_b'], "Helvetica", 8),
            (data['right_3_a'], "Helvetica-Bold", data['right_3_b'], "Helvetica", 24)
        ]

        for text, offset, font_style in left_text_info:
            c.setFont(font_style, sub_banner_text_size)
            c.drawString(side_margin, height - top_margin - banner_height - offset * mm, text)

        for label, label_font, value, value_font, offset in right_text_info:
            c.setFont(label_font, sub_banner_text_size)
            label_width = c.stringWidth(label, label_font, sub_banner_text_size)
            c.drawString(width - side_margin - label_width - 15 * mm, height - top_margin - banner_height - offset * mm, label)
            c.setFont(value_font, sub_banner_text_size)
            c.drawRightString(width - side_margin, height - top_margin - banner_height - offset * mm, value)

    def draw_table(self, c, width, height, start_y, side_margin, table_data):
        """Draw a table on the PDF."""
        table_width = width - 2 * side_margin

        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), custom_color1),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, custom_color1),
            ('BOX', (0, 0), (-1, -1), 2, custom_color1),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, custom_color2])
        ])

        col_widths = [table_width * 0.16, table_width * 0.48, table_width * 0.18, table_width * 0.18]

        if not table_data:
            table_data = [["", "", "", ""]]
        table = Table(table_data, colWidths=col_widths)
        table.setStyle(table_style)

        table.wrapOn(c, table_width, height)
        table.drawOn(c, side_margin, start_y)

    def draw_footer(self, c, width, height, top_margin, footer_text_info):
        """Draw the footer on the PDF."""
        footer_start_y = height - top_margin - 155 * mm
        left_margin = 21 * mm
        interlinea = 10 * mm

        for index, info in enumerate(footer_text_info):
            line1_text = info[0] if len(info) > 0 else ""
            line2_text = info[1] if len(info) > 1 else ""
            right_label = info[2] if len(info) > 2 else ""
            right_value = info[3] if len(info) > 3 else ""

            c.setFont("Helvetica", 8)
            c.drawString(left_margin, footer_start_y - index * interlinea, line1_text)

            if line2_text:
                c.drawString(left_margin + 30 * mm, footer_start_y - index * interlinea, line2_text)

            right_text_x = width - 80 * mm
            if right_label:
                c.setFont("Helvetica-Bold", 8)
                c.drawString(right_text_x, footer_start_y - index * interlinea, right_label)
            if right_value:
                c.setFont("Helvetica", 8)
                c.drawString(right_text_x + 30 * mm, footer_start_y - index * interlinea, right_value)