from fpdf import FPDF
import io

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Movie Plot & Scene Script', align='C', ln=True)
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, title, ln=True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, body)
        self.ln()

def generate_pdf_bytes(plot_text: str, scene_text: str) -> io.BytesIO:
    pdf = PDF()
    pdf.add_page()

    pdf.chapter_title("MOVIE PLOT:")
    pdf.chapter_body(plot_text)

    pdf.chapter_title("KEY SCENE SCRIPT:")
    pdf.chapter_body(scene_text)

    # Get PDF as string of bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')

    # Wrap bytes in BytesIO
    pdf_buffer = io.BytesIO(pdf_bytes)
    pdf_buffer.seek(0)

    return pdf_buffer
