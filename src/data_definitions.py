from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.units import mm

# Definiciones de colores personalizados
custom_color1 = colors.Color(31/255, 73/255, 125/255)
custom_color2 = colors.Color(240/255, 240/255, 255/255)

# Datos predeterminados para la generación de PDF
data_test = {
    'left_1': "Cooperativa de Trabajo MADYGRAF LTDA",
    'left_2': "Ruta panamericana 36.700 - Garin - 1618",
    'left_3': "C.U.I.T.: 33 71465177 9",
    'left_4': "Teléfono: 11 4035-5771",
    'left_5': "Presupuesto para:",
    'left_6': "Cliente ",
    'right_1_a': "Fecha",
    'right_1_b': datetime.now().strftime("%d/%m/%Y"),
    'right_2_a': "N° de presupuesto",
    'right_2_b': "123",
    'right_3_a': "Presupuesto válido hasta:",
    'right_3_b': (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y"),
    'table1_data': [
        ["Vendedor", "Nombre", "Fecha de envío", "Condiciones"],
        [1497, "Najarro Eymy", "a convenir", "50% anticipo"]
    ],
    'table2_data': [
        ["Cantidad", "Descripción", "Precio por unidad", "Importe"],
        [100, "26x12x36 Bolsa Marron 100 grs - c/manijas"   , 140.40, 14040.00],
        [100, "22x10x30 Bolsa Marron 100 grs - c/manijas"   , 124.40, 12440.00],
        [100, "22x10x30 Bolsa Marron 100 grs"               ,  88.38,  8838.00],
        [],
        [],
        [],
        [],
        [],
        []
    ],
    'footer_text_info': [
        ("HORARIO DE RETIRO MERCADERÍA DE 08 A 15HS", 32 * mm, "Helvetica"),
        ("Subtotal", "$35,318.00", 42 * mm, "Helvetica-Bold", "Helvetica"),
        ("IVA 21%", "$7,416.78", 52 * mm, "Helvetica-Bold", "Helvetica"),
        ("Total", "$42,734.78", 62 * mm, "Helvetica-Bold", "Helvetica"),
        ("Gracias por su confianza", 72 * mm, "Helvetica"),
        ("Comentarios o Instrucciones especiales:", 82 * mm, "Helvetica"),
        ("Entrega:", "No incluye envío", 92 * mm, "Helvetica-Bold", "Helvetica"),
        ("Condiciones:", "50% Anticipo, 50% contra entrega", 102 * mm, "Helvetica-Bold", "Helvetica")
    ]
}
