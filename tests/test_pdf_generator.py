#Presupuestador/tests/test_pdf_generator.py
import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
from datetime import datetime
from src.models.pdf_generator import PDFGenerator

class TestPDFGenerator(unittest.TestCase):
    def setUp(self):
        self.pdf_generator = PDFGenerator()

    @patch('builtins.input', return_value='123')
    def test_get_presupuesto_id_valid(self, mock_input):
        result = self.pdf_generator.get_presupuesto_id()
        self.assertEqual(result, 123)

    @patch('builtins.input', return_value='invalid')
    def test_get_presupuesto_id_invalid(self, mock_input):
        result = self.pdf_generator.get_presupuesto_id()
        self.assertIsNone(result)

    @patch('os.startfile')
    @patch.object(PDFGenerator, 'create_pdf')
    @patch.object(PDFGenerator, 'get_presupuesto_id', return_value=None)
    @patch.object(PDFGenerator, 'prepare_output_directory', return_value='/mocked/path')
    @patch('datetime.datetime')
    @patch('os.path.join', return_value='/mocked/path/test.pdf')
    def test_handle_generate_pdf(self, mock_path_join, mock_datetime, mock_prepare_output_directory, mock_get_presupuesto_id, mock_create_pdf, mock_startfile):
        mock_datetime.now.return_value.strftime.return_value = '20240704_094720'
        self.pdf_generator.handle_generate_pdf()
        mock_create_pdf.assert_called_once()
        mock_startfile.assert_called_once_with('/mocked/path/test.pdf')

    @patch('reportlab.pdfgen.canvas.Canvas')
    def test_create_pdf(self, mock_canvas):
        data = {
            'table1_data': [],
            'table2_data': [],
            'footer_text_info': []
        }
        self.pdf_generator.create_pdf(data, '/mocked/path/test.pdf')
        mock_canvas.assert_called_once_with('/mocked/path/test.pdf', pagesize=(595.2755905511812, 841.8897637795277))

if __name__ == '__main__':
    unittest.main()
