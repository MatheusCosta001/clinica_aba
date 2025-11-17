from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageTemplate, Frame, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
from zoneinfo import ZoneInfo
import os


def _register_font():
    # Try common TTF fonts to support UTF-8 characters (accented letters)
    possible = [
        r"C:\Windows\Fonts\DejaVuSans.ttf",
        r"C:\Windows\Fonts\Arial.ttf",
        r"/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in possible:
        if os.path.exists(p):
            try:
                pdfmetrics.registerFont(TTFont('CustomSans', p))
                return 'CustomSans'
            except Exception:
                continue
    # fallback to Helvetica
    return 'Helvetica'


class NumberedCanvas(canvas.Canvas):
    """Canvas that adds header, footer, watermark, and page numbers."""
    
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._pages = []
        self.font_name = _register_font()

    def showPage(self):
        self._pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self._pages)
        for page_num, page in enumerate(self._pages, 1):
            self.__dict__.update(page)
            self._draw_header()
            self._draw_footer(page_num, page_count)
            self._draw_watermark()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def _draw_header(self):
        """Draw clinic header with name, logo placeholder, and contact."""
        y = self._pagesize[1] - 15*mm
        
        # Clinic name
        self.setFont(self.font_name, 16)
        self.setFillColor(colors.HexColor("#2D7FF9"))
        self.drawString(20*mm, y, "Clínica ABA de Mogi das Cruzes")
        
        # Contact info in smaller text
        self.setFont(self.font_name, 8)
        self.setFillColor(colors.HexColor("#6C757D"))
        contact_y = y - 5*mm
        self.drawString(20*mm, contact_y, "Telefone: (11) 1234-5678 | Email: contato@clinicaaba.com.br")
        self.drawString(20*mm, contact_y - 3*mm, "Endereço: Rua Exemplo, 123 – Mogi das Cruzes/SP")
        
        # Horizontal line
        self.setLineWidth(1)
        self.setStrokeColor(colors.HexColor("#2D7FF9"))
        self.line(20*mm, y - 10*mm, self._pagesize[0] - 20*mm, y - 10*mm)

    def _draw_footer(self, page_num, total_pages):
        """Draw footer with pagination and LGPD notice."""
        y = 10*mm
        
        # LGPD notice
        self.setFont(self.font_name, 7)
        self.setFillColor(colors.HexColor("#6C757D"))
        lgpd_text = "Este documento contém informações sensíveis e pessoais. Não deve ser compartilhado sem autorização."
        self.drawString(20*mm, y + 3*mm, lgpd_text)
        
        # Page number
        self.setFont(self.font_name, 8)
        page_text = f"Página {page_num} de {total_pages}"
        self.drawRightString(self._pagesize[0] - 20*mm, y + 3*mm, page_text)
        
        # Horizontal line above footer
        self.setLineWidth(0.5)
        self.setStrokeColor(colors.HexColor("#DDD"))
        self.line(20*mm, y + 8*mm, self._pagesize[0] - 20*mm, y + 8*mm)

    def _draw_watermark(self):
        """Draw subtle watermark on the page."""
        self.saveState()
        self.setFont(self.font_name, 60)
        self.setFillColor(colors.HexColor("#E0E0E0"))
        self.setFillAlpha(0.1)
        self.rotate(45)
        # Place watermark diagonally
        self.drawString(50, 50, "ABA")
        self.restoreState()


def gerar_relatorio_pdf(paciente, evolucoes, gerador_nome, comentarios="", user_papel="", data_inicio="", data_fim=""):
    """Generate a professional PDF report with header, footer, and styling."""
    buffer = BytesIO()
    font_name = _register_font()

    # Create doc with custom canvas class for header/footer/watermark
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20*mm,
        rightMargin=20*mm,
        topMargin=30*mm,
        bottomMargin=25*mm,
        title=f"Relatório - {paciente.nome}",
        creator="Clínica ABA"
    )
    
    # Override the canvas class
    doc.build_page_templates = []
    
    # Define styles with professional colors
    styles = getSampleStyleSheet()
    
    # Custom styles with softer color palette
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=font_name,
        fontSize=16,
        leading=18,
        textColor=colors.HexColor("#2D7FF9"),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontWeight='bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName=font_name,
        fontSize=12,
        leading=14,
        textColor=colors.HexColor("#1A66E0"),
        spaceAfter=8,
        spaceBefore=8,
        fontWeight='bold'
    )
    
    normal_style = ParagraphStyle(
        'normal',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=13,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1A1A1A")
    )
    
    comment_style = ParagraphStyle(
        'comment',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=13,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1A1A1A"),
        italic=True
    )

    flow = []

    # Title
    flow.append(Paragraph(f"Relatório Clínico — {paciente.nome}", title_style))
    flow.append(Spacer(1, 6*mm))

    # Report metadata
    now_sp = datetime.now(ZoneInfo('America/Sao_Paulo'))
    meta_date = f"Gerado em: {now_sp.strftime('%d/%m/%Y às %H:%M')}"
    meta_by = f"Gerado por: {gerador_nome}"
    if user_papel:
        meta_by += f" ({user_papel.title()})"
    
    flow.append(Paragraph(meta_date, normal_style))
    flow.append(Paragraph(meta_by, normal_style))
    
    # Date range info if provided
    if data_inicio or data_fim:
        date_range = "Período: "
        if data_inicio and data_fim:
            date_range += f"{data_inicio} a {data_fim}"
        elif data_inicio:
            date_range += f"A partir de {data_inicio}"
        elif data_fim:
            date_range += f"Até {data_fim}"
        flow.append(Paragraph(date_range, normal_style))
    
    flow.append(Spacer(1, 8*mm))

    # Patient data section
    flow.append(Paragraph("<b>Dados do Paciente:</b>", heading_style))
    patient_data = [
        f"<b>Nome:</b> {paciente.nome}",
        f"<b>Data de Nascimento:</b> {paciente.data_nascimento or 'Não informada'}",
        f"<b>Idade:</b> {paciente.idade or 'Não informada'}",
        f"<b>Diagnóstico:</b> {paciente.diagnostico or 'Não informado'}",
        f"<b>Responsável:</b> {paciente.responsavel or 'Não informado'}",
        f"<b>Endereço:</b> {paciente.rua or ''} - {paciente.bairro or ''} - {paciente.cidade or ''}/{paciente.uf or ''} - CEP: {paciente.cep or 'N/A'}"
    ]
    for item in patient_data:
        flow.append(Paragraph(item, normal_style))
    
    flow.append(Spacer(1, 8*mm))

    # Evolutions section
    if evolucoes:
        flow.append(Paragraph("<b>Evoluções Clínicas:</b>", heading_style))
        
        for e in evolucoes:
            dt = e.data_hora
            try:
                dt = dt.astimezone(ZoneInfo('America/Sao_Paulo'))
            except Exception:
                dt = datetime.now(ZoneInfo('America/Sao_Paulo'))
            
            usuario = getattr(e, 'usuario', None)
            nome = getattr(usuario, 'nome', '---') if usuario else '---'
            papel = getattr(usuario, 'papel', None) if usuario else None
            especialidade = e.profissional_especialidade or (getattr(usuario, 'especialidade', None) if usuario else None)
            
            if papel == 'adm':
                papel_label = 'ADM'
            elif papel == 'coordenador':
                papel_label = 'Coordenador'
            elif papel == 'profissional':
                papel_label = especialidade or 'Profissional'
            else:
                papel_label = papel or ''

            # Evolution header with date and professional
            header = f"<b>{dt.strftime('%d/%m/%Y às %H:%M')} — {nome} ({papel_label})</b>"
            flow.append(Paragraph(header, normal_style))
            
            # Evolution content
            flow.append(Paragraph(e.anotacao or '', normal_style))
            flow.append(Spacer(1, 4*mm))
    else:
        flow.append(Paragraph("Nenhuma evolução registrada para o período especificado.", normal_style))
    
    flow.append(Spacer(1, 8*mm))

    # Comments/Considerations section
    flow.append(Paragraph("<b>Comentários/Considerações Finais:</b>", heading_style))
    flow.append(Paragraph(comentarios, comment_style))
    
    flow.append(Spacer(1, 10*mm))

    # prepare function to draw logo on pages (top-left)
    def _draw_logo_on_page(canvas_obj, doc_obj):
        try:
            # path to static image
            logo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static', 'img', 'clinica_aba_logo.png'))
            if not os.path.exists(logo_path):
                return
            # desired size (approx 80x80 px -> ~25mm)
            iw = 25 * mm
            ih = 25 * mm
            # place near top-left within page margins
            x = doc_obj.pagesize[0] - iw - 20 * mm
            y = doc_obj.pagesize[1] - 1 * mm - ih
            canvas_obj.saveState()
            try:
                canvas_obj.setFillAlpha(0.80)
            except Exception:
                # some backends may not support alpha; ignore if so
                pass
            canvas_obj.drawImage(logo_path, x, y, width=iw, height=ih, mask='auto')
            canvas_obj.restoreState()
        except Exception:
            return

    # Build the document with custom canvas and add logo on first and later pages
    doc.build(flow, canvasmaker=NumberedCanvas, onFirstPage=_draw_logo_on_page, onLaterPages=_draw_logo_on_page)
    buffer.seek(0)
    return buffer
