"""
Geração de PDF do Relatório Completo usando fpdf2 com suporte a Unicode.
Usa fonte DejaVuSans para acentos corretos em português.
"""

from fpdf import FPDF
import os


class RelatorioPDF(FPDF):
    def __init__(self):
        super().__init__(format="A4")
        # Tenta carregar fonte Unicode; fallback para Helvetica
        font_dir = os.path.join(os.path.dirname(__file__), "fonts")
        try:
            self.add_font("DejaVu", "", os.path.join(font_dir, "DejaVuSans.ttf"), uni=True)
            self.add_font("DejaVu", "B", os.path.join(font_dir, "DejaVuSans-Bold.ttf"), uni=True)
            self.default_font = "DejaVu"
        except Exception:
            self.default_font = "Helvetica"

    def header(self):
        if self.page_no() == 1:
            self.set_font(self.default_font, "B", 20)
            self.set_text_color(30, 41, 59)
            self.cell(0, 15, "Relatório Estratégico — SIPE10", ln=True, align="C")
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font(self.default_font, "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")


def markdown_to_pdf_bytes(markdown_text: str) -> bytes:
    pdf = RelatorioPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    text = markdown_text.lstrip("\ufeff")

    for raw_line in text.split("\n"):
        line = raw_line.rstrip()

        if line.startswith("# "):
            pdf.set_font(pdf.default_font, "B", 18)
            pdf.set_text_color(30, 41, 59)
            pdf.ln(4)
            pdf.multi_cell(0, 10, line[2:])
            pdf.ln(2)
        elif line.startswith("## "):
            pdf.set_font(pdf.default_font, "B", 14)
            pdf.set_text_color(37, 99, 235)
            pdf.ln(3)
            pdf.multi_cell(0, 8, line[3:])
            pdf.ln(1)
        elif line.startswith("### "):
            pdf.set_font(pdf.default_font, "B", 12)
            pdf.set_text_color(15, 23, 42)
            pdf.multi_cell(0, 7, line[4:])
        elif line.startswith("- "):
            pdf.set_font(pdf.default_font, "", 11)
            pdf.set_text_color(15, 23, 42)
            pdf.multi_cell(0, 6, f"  •  {line[2:]}")
        elif line.strip() == "":
            pdf.ln(2)
        else:
            pdf.set_font(pdf.default_font, "", 11)
            pdf.set_text_color(15, 23, 42)
            pdf.multi_cell(0, 6, line)

    return bytes(pdf.output())
