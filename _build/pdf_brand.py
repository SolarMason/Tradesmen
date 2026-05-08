"""
NEPA-PRO Tradesmen — Branded PDF generation library.

Provides consistent header, footer, typography, and styles across all
subcontractor and customer documents.

Brand:
- Primary navy: #0a1628
- Accent orange: #ff6b35
- Body: Helvetica
- Tagline: Veteran Owned. NEPA Local. Iron-Clad.
- Contact: 570-677-7971 · service@nepa-pro.com · Clarks Summit, PA 18411
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas


# ============================================================
# BRAND COLORS
# ============================================================
NAVY        = HexColor('#0a1628')
NAVY_DARK   = HexColor('#060f1f')
NAVY_LIGHT  = HexColor('#1a2c4a')
ORANGE      = HexColor('#ff6b35')
ORANGE_DARK = HexColor('#e04e12')
GREY_BG     = HexColor('#f4f5f7')
GREY_BORDER = HexColor('#d4d7dc')
GREY_TEXT   = HexColor('#5a6068')


# ============================================================
# PARAGRAPH STYLES
# ============================================================
def get_styles():
    base = getSampleStyleSheet()

    return {
        'title': ParagraphStyle(
            'BrandTitle', parent=base['Title'],
            fontName='Helvetica-Bold', fontSize=22, leading=27,
            textColor=NAVY, alignment=TA_LEFT, spaceAfter=4, spaceBefore=0,
        ),
        'subtitle': ParagraphStyle(
            'BrandSubtitle', parent=base['Normal'],
            fontName='Helvetica', fontSize=11, leading=14,
            textColor=GREY_TEXT, alignment=TA_LEFT, spaceAfter=18,
        ),
        'h2': ParagraphStyle(
            'BrandH2', parent=base['Heading2'],
            fontName='Helvetica-Bold', fontSize=12, leading=16,
            textColor=NAVY, spaceAfter=6, spaceBefore=14,
            keepWithNext=True,
        ),
        'h3': ParagraphStyle(
            'BrandH3', parent=base['Heading3'],
            fontName='Helvetica-Bold', fontSize=10.5, leading=14,
            textColor=NAVY, spaceAfter=4, spaceBefore=10,
            keepWithNext=True,
        ),
        'body': ParagraphStyle(
            'BrandBody', parent=base['Normal'],
            fontName='Helvetica', fontSize=9.5, leading=13.5,
            textColor=NAVY_DARK, alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        'bullet': ParagraphStyle(
            'BrandBullet', parent=base['Normal'],
            fontName='Helvetica', fontSize=9.5, leading=13.5,
            textColor=NAVY_DARK, leftIndent=18, bulletIndent=6,
            spaceAfter=4,
        ),
        'small': ParagraphStyle(
            'BrandSmall', parent=base['Normal'],
            fontName='Helvetica', fontSize=8, leading=11,
            textColor=GREY_TEXT, alignment=TA_LEFT, spaceAfter=4,
        ),
        'small_center': ParagraphStyle(
            'BrandSmallC', parent=base['Normal'],
            fontName='Helvetica', fontSize=8, leading=11,
            textColor=GREY_TEXT, alignment=TA_CENTER,
        ),
        'callout': ParagraphStyle(
            'BrandCallout', parent=base['Normal'],
            fontName='Helvetica-Bold', fontSize=9.5, leading=13.5,
            textColor=NAVY, alignment=TA_LEFT, spaceAfter=4,
            backColor=GREY_BG,
        ),
        'recital': ParagraphStyle(
            'BrandRecital', parent=base['Normal'],
            fontName='Helvetica-Oblique', fontSize=9.5, leading=13.5,
            textColor=NAVY_DARK, alignment=TA_JUSTIFY, spaceAfter=6,
            leftIndent=18, rightIndent=18,
        ),
    }


# ============================================================
# HEADER + FOOTER
# ============================================================
def draw_header_footer(canvas_obj, doc, doc_title, doc_code, doc_version):
    """Drawn on every page."""
    canvas_obj.saveState()
    page_width, page_height = letter

    # ===== TOP HEADER BAR =====
    # Navy band across the top
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, page_height - 0.65*inch, page_width, 0.65*inch, fill=1, stroke=0)

    # Orange accent stripe
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.rect(0, page_height - 0.7*inch, page_width, 0.05*inch, fill=1, stroke=0)

    # ----- Logo treatment (left) -----
    # NEPA-PRO mark: chevron/arrow emblem in orange + bold wordmark
    logo_x = 0.5 * inch
    logo_y = page_height - 0.42*inch

    # Orange diamond/chevron mark (geometric, looks like a roof/peak)
    canvas_obj.setFillColor(ORANGE)
    p = canvas_obj.beginPath()
    p.moveTo(logo_x, logo_y - 8)
    p.lineTo(logo_x + 8, logo_y + 6)
    p.lineTo(logo_x + 16, logo_y - 8)
    p.lineTo(logo_x + 12, logo_y - 8)
    p.lineTo(logo_x + 8, logo_y - 2)
    p.lineTo(logo_x + 4, logo_y - 8)
    p.close()
    canvas_obj.drawPath(p, fill=1, stroke=0)

    # NEPA-PRO wordmark
    canvas_obj.setFillColor(white)
    canvas_obj.setFont('Helvetica-Bold', 13)
    canvas_obj.drawString(logo_x + 24, logo_y - 2, 'NEPA-PRO')
    canvas_obj.setFont('Helvetica', 9.5)
    canvas_obj.setFillColor(HexColor('#cccccc'))
    canvas_obj.drawString(logo_x + 24, logo_y - 14, 'Tradesmen')

    # ----- Right side: vet badge + contact -----
    canvas_obj.setFillColor(ORANGE)
    canvas_obj.setFont('Helvetica-Bold', 8)
    badge_text = '★ VETERAN OWNED & OPERATED'
    badge_w = canvas_obj.stringWidth(badge_text, 'Helvetica-Bold', 8)
    badge_x = page_width - 0.5*inch - badge_w - 12
    canvas_obj.roundRect(badge_x - 6, logo_y - 4, badge_w + 12, 14, 3, fill=0, stroke=1)
    canvas_obj.drawString(badge_x, logo_y, badge_text)

    canvas_obj.setFillColor(HexColor('#cccccc'))
    canvas_obj.setFont('Helvetica', 7.5)
    contact_text = '570-677-7971  ·  service@nepa-pro.com  ·  Clarks Summit, PA 18411'
    contact_w = canvas_obj.stringWidth(contact_text, 'Helvetica', 7.5)
    canvas_obj.drawString(page_width - 0.5*inch - contact_w, logo_y - 14, contact_text)

    # ===== DOCUMENT META BAR (just below header) =====
    canvas_obj.setFillColor(GREY_BG)
    canvas_obj.rect(0, page_height - 0.95*inch, page_width, 0.25*inch, fill=1, stroke=0)
    canvas_obj.setFont('Helvetica-Bold', 8.5)
    canvas_obj.setFillColor(NAVY)
    canvas_obj.drawString(0.5*inch, page_height - 0.85*inch, doc_title.upper())

    canvas_obj.setFont('Helvetica', 7.5)
    canvas_obj.setFillColor(GREY_TEXT)
    meta = f'DOC {doc_code}  ·  v{doc_version}  ·  Page {canvas_obj.getPageNumber()}'
    meta_w = canvas_obj.stringWidth(meta, 'Helvetica', 7.5)
    canvas_obj.drawString(page_width - 0.5*inch - meta_w, page_height - 0.85*inch, meta)

    # ===== FOOTER =====
    canvas_obj.setStrokeColor(GREY_BORDER)
    canvas_obj.setLineWidth(0.5)
    canvas_obj.line(0.5*inch, 0.5*inch, page_width - 0.5*inch, 0.5*inch)

    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.setFillColor(GREY_TEXT)
    canvas_obj.drawString(0.5*inch, 0.35*inch,
        f'NEPA-PRO Tradesmen  ·  © NEPA-PRO LLC  ·  All Rights Reserved  ·  This document is proprietary and confidential.')
    canvas_obj.drawRightString(page_width - 0.5*inch, 0.35*inch,
        f'tradesmen.nepa-pro.com')

    canvas_obj.restoreState()


# ============================================================
# DOCUMENT TEMPLATE
# ============================================================
class BrandedDoc(BaseDocTemplate):
    def __init__(self, filename, doc_title, doc_code, doc_version='1.0', **kwargs):
        super().__init__(
            filename, pagesize=letter,
            leftMargin=0.6*inch, rightMargin=0.6*inch,
            topMargin=1.15*inch, bottomMargin=0.65*inch,
            title=doc_title, author='NEPA-PRO LLC',
            **kwargs,
        )
        self.doc_title = doc_title
        self.doc_code = doc_code
        self.doc_version = doc_version

        frame = Frame(
            self.leftMargin, self.bottomMargin,
            self.width, self.height,
            id='normal', showBoundary=0,
        )
        self.addPageTemplates([
            PageTemplate(id='Branded', frames=frame, onPage=self._on_page),
        ])

    def _on_page(self, canvas_obj, doc):
        draw_header_footer(canvas_obj, doc, self.doc_title, self.doc_code, self.doc_version)


# ============================================================
# REUSABLE FLOWABLES
# ============================================================
def doc_title_block(title, subtitle, styles):
    """The big title at the start of each document, below the header."""
    return [
        Paragraph(title, styles['title']),
        HRFlowable(width='100%', thickness=2, color=ORANGE, spaceAfter=6),
        Paragraph(subtitle, styles['subtitle']),
    ]


def signature_block(role_label, lines=None, styles=None):
    """Standardized signature block."""
    if lines is None:
        lines = ['Signature', 'Printed Name', 'Date']

    rows = []
    for label in lines:
        rows.append([
            Paragraph(f'<font color="#0a1628"><b>{label}</b></font>', styles['small']),
            Paragraph('_' * 50, styles['small']),
        ])

    tbl = Table(rows, colWidths=[1.4*inch, 5.5*inch])
    tbl.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
        ('TOPPADDING', (0,0), (-1,-1), 12),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))

    role_p = Paragraph(
        f'<font color="#ff6b35"><b>{role_label.upper()}</b></font>',
        styles['small'],
    )
    return [Spacer(1, 8), role_p, tbl]


def fillable_field(label, width=3.0, styles=None):
    """Inline fillable text field with underline."""
    return Table(
        [[Paragraph(f'<b>{label}:</b>', styles['body']),
          Paragraph('_' * int(width * 16), styles['body'])]],
        colWidths=[1.6*inch, (width)*inch],
        style=TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]),
    )


def callout_box(text, styles, color=ORANGE):
    """Highlighted callout box for important notices."""
    p = Paragraph(text, styles['callout'])
    tbl = Table([[p]], colWidths=[7.0*inch])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#fff4ee')),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('BOX', (0,0), (-1,-1), 0, GREY_BORDER),
        ('LINEBEFORE', (0,0), (0,-1), 3, color),
    ]))
    return tbl


def section_divider():
    return [Spacer(1, 6), HRFlowable(width='100%', thickness=0.5, color=GREY_BORDER), Spacer(1, 6)]


def numbered_clause(num, heading, body_html, styles):
    """A numbered legal clause with bold header."""
    out = []
    head = Paragraph(
        f'<font color="#0a1628"><b>{num}. {heading}</b></font>',
        styles['h3'],
    )
    out.append(head)
    if body_html:
        out.append(Paragraph(body_html, styles['body']))
    return out


def submission_instructions(styles, recipient_role='subcontractor onboarding'):
    """Standard 'how to return this document' instruction block."""
    text = (
        f'<b>Return instructions.</b> Once signed and dated, return this document by email to '
        f'<font color="#ff6b35"><b>service@nepa-pro.com</b></font> with the subject line including '
        f'your full legal name and the document code shown in the header. Mailed copies may be sent to: '
        f'NEPA-PRO LLC, 14012 Orchard Drive, Clarks Summit, PA 18411. Documents must be received and '
        f'countersigned by NEPA-PRO LLC before any {recipient_role} is finalized.'
    )
    return callout_box(text, styles)
