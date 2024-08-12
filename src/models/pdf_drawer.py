# src/models/pdf_drawer.py

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

class PDFDrawer:
    """Class responsible for drawing elements on the PDF."""

    def set_pdf_title(self, c, filename):
        """Set the title of the PDF."""
        ...

    def draw_banner(self, c, width, height, side_margin, top_margin, banner_height, data):
        """Draw the banner on the PDF."""
        ...

    def draw_header(self, c, width, height, top_margin, banner_height, side_margin, sub_banner_text_size, data):
        """Draw the header on the PDF."""
        ...

    def draw_table(self, c, width, height, start_y, side_margin, table_data):
        """Draw a table on the PDF."""
        ...

    def draw_footer(self, c, width, height, top_margin, footer_text_info):
        """Draw the footer on the PDF."""
        ...