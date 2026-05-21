from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether
import os

# Colors
BURG   = colors.HexColor('#641C2A')
BURG2  = colors.HexColor('#4A1320')
CREAM  = colors.HexColor('#F8F0E8')
CREAM2 = colors.HexColor('#EDE0CF')
GOLD   = colors.HexColor('#B8926A')
MUTED  = colors.HexColor('#7A5840')
TEXT   = colors.HexColor('#2C1A10')
WHITE  = colors.white

W, H = A4

doc = SimpleDocTemplate(
    '/home/user/site/public/dental-training.pdf',
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=18*mm, bottomMargin=18*mm
)

def header_canvas(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BURG2)
    canvas.rect(0, H - 110, W, 110, fill=1, stroke=0)
    # Gold line
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, H - 112, W - 20*mm, H - 112)
    # Script line
    canvas.setFillColor(colors.HexColor('#C4A882'))
    canvas.setFont('Helvetica', 9)
    canvas.drawCentredString(W/2, H - 30, 'індивідуальна програма')
    # Title
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 26)
    canvas.drawCentredString(W/2, H - 56, 'НАВЧАННЯ SMM')
    canvas.setFont('Helvetica', 13)
    canvas.setFillColor(colors.HexColor('#C4A882'))
    canvas.drawCentredString(W/2, H - 74, 'для стоматологічної клініки')
    # Sub
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.HexColor('#9B8060'))
    canvas.drawCentredString(W/2, H - 90, '5 днів  ·  10 годин  ·  від нуля до самостійного ведення соцмереж')
    # Price badge
    bw, bh = 90, 26
    bx = W/2 - bw/2
    by = H - 118
    canvas.setFillColor(GOLD)
    canvas.roundRect(bx, by, bw, bh, 4, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 16)
    canvas.drawCentredString(W/2, by + 7, '$450')
    canvas.restoreState()

def footer_canvas(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BURG2)
    canvas.rect(0, 0, W, 22, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor('#C4A882'))
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(W/2, 7, 'Оксана Богданець  ·  SMM-стратег  ·  Reels-продюсер')
    canvas.restoreState()

def on_page(canvas, doc):
    header_canvas(canvas, doc)
    footer_canvas(canvas, doc)

days = [
    {
        'num': '01',
        'title': 'СТОРІТЕЛІНГ',
        'topics': ['Експертні', 'Кейси', 'Болі клієнтів', 'Заперечення'],
        'result': 'Навчимося прописувати Stories які привертають увагу цільової аудиторії, викликають довіру та залучають нових пацієнтів у клініку'
    },
    {
        'num': '02',
        'title': 'КАРУСЕЛІ',
        'topics': ['Експертні', 'Продуктові', 'Знайомство з фахівцями', 'Кейси', 'Особисті'],
        'result': 'Вмієш створювати каруселі які люди гортають до кінця, зберігають і пересилають — це органічне просування сторінки'
    },
    {
        'num': '03',
        'title': 'ВОРОНКИ',
        'topics': ['Через Stories', 'Через каруселі', 'Запис на консультацію'],
        'result': 'Розумієш як вибудувати систему контенту яка веде людину від першого перегляду до запису на консультацію'
    },
    {
        'num': '04',
        'title': 'ЗЙОМКА',
        'topics': ['Налаштування камери', 'Виставлення світла', 'Розкадрування'],
        'result': 'Знімаєш на телефон так що виглядає як у справжнього фотографа — клієнти бачать якісну клініку ще до першого візиту'
    },
    {
        'num': '05',
        'title': 'МОНТАЖ',
        'topics': ['Базовий монтаж відео', 'Stories', 'Reels'],
        'result': 'Монтуєш Stories та Reels сама, без фрілансерів і без паніки — повна самостійність у веденні соцмереж'
    },
]

story = []
story.append(Spacer(1, 52*mm))

for d in days:
    topics_str = '   ✦   '.join(d['topics'])
    tbl_data = [[
        Paragraph(f"<font color='#C4A882' size=8>день</font><br/><font size=22><b>{d['num']}</b></font>", ParagraphStyle('n', fontName='Helvetica-Bold', alignment=1, leading=26)),
        [
            Paragraph(f"<b>{d['title']}</b>", ParagraphStyle('t', fontName='Helvetica-Bold', fontSize=11, textColor=BURG, spaceAfter=6)),
            Paragraph(topics_str, ParagraphStyle('top', fontName='Helvetica', fontSize=8.5, textColor=MUTED, spaceAfter=10)),
            Paragraph('РЕЗУЛЬТАТ', ParagraphStyle('rl', fontName='Helvetica-Bold', fontSize=7, textColor=GOLD, spaceAfter=4, letterSpacing=1)),
            Paragraph(d['result'], ParagraphStyle('res', fontName='Helvetica-Oblique', fontSize=9, textColor=MUTED, leading=14)),
        ]
    ]]
    tbl = Table(tbl_data, colWidths=[28*mm, 130*mm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), BURG),
        ('BACKGROUND', (1,0), (1,0), WHITE),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('VALIGN', (1,0), (1,0), 'TOP'),
        ('TOPPADDING', (0,0), (0,0), 10),
        ('BOTTOMPADDING', (0,0), (0,0), 10),
        ('TOPPADDING', (1,0), (1,0), 14),
        ('BOTTOMPADDING', (1,0), (1,0), 14),
        ('LEFTPADDING', (1,0), (1,0), 16),
        ('RIGHTPADDING', (1,0), (1,0), 12),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#D4B896')),
        ('LINEAFTER', (0,0), (0,0), 0.5, colors.HexColor('#D4B896')),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [None]),
    ]))
    story.append(KeepTogether(tbl))
    story.append(Spacer(1, 8))

# Price block
story.append(Spacer(1, 10))
story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=16))

price_data = [
    [
        Paragraph('<font size=20 color="#641C2A"><b>5</b></font><br/><font size=8 color="#7A5840">днів навчання</font>', ParagraphStyle('p', alignment=1, leading=18)),
        Paragraph('<font size=20 color="#641C2A"><b>10</b></font><br/><font size=8 color="#7A5840">годин практики</font>', ParagraphStyle('p', alignment=1, leading=18)),
        Paragraph('<font size=20 color="#B8926A"><b>$450</b></font><br/><font size=8 color="#7A5840">вартість програми</font>', ParagraphStyle('p', alignment=1, leading=18)),
    ]
]
price_tbl = Table(price_data, colWidths=[52*mm, 52*mm, 52*mm])
price_tbl.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), CREAM2),
    ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#D4B896')),
    ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D4B896')),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
]))
story.append(price_tbl)

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print('PDF created successfully')
