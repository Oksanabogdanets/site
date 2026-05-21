from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Spacer, Table, TableStyle, HRFlowable, Paragraph, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle

# Register Cyrillic fonts
FONT_PATH = '/usr/share/fonts/truetype/liberation/'
pdfmetrics.registerFont(TTFont('Sans',        FONT_PATH + 'LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Sans-Bold',   FONT_PATH + 'LiberationSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Sans-Italic', FONT_PATH + 'LiberationSans-Italic.ttf'))
pdfmetrics.registerFont(TTFont('Serif',       FONT_PATH + 'LiberationSerif-Regular.ttf'))
pdfmetrics.registerFont(TTFont('Serif-Bold',  FONT_PATH + 'LiberationSerif-Bold.ttf'))

BURG   = colors.HexColor('#641C2A')
BURG2  = colors.HexColor('#4A1320')
CREAM  = colors.HexColor('#F8F0E8')
CREAM2 = colors.HexColor('#EDE0CF')
GOLD   = colors.HexColor('#B8926A')
MUTED  = colors.HexColor('#7A5840')
TEXT   = colors.HexColor('#2C1A10')
WHITE  = colors.white
TAUPE2 = colors.HexColor('#C4A882')

W, H = A4

def on_page(canvas, doc):
    # Header
    canvas.saveState()
    canvas.setFillColor(BURG2)
    canvas.rect(0, H - 108, W, 108, fill=1, stroke=0)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(0.5)
    canvas.line(20*mm, H - 110, W - 20*mm, H - 110)

    canvas.setFillColor(TAUPE2)
    canvas.setFont('Sans', 9)
    canvas.drawCentredString(W/2, H - 26, 'індивідуальна програма')

    canvas.setFillColor(WHITE)
    canvas.setFont('Serif-Bold', 24)
    canvas.drawCentredString(W/2, H - 50, 'НАВЧАННЯ SMM')

    canvas.setFont('Sans', 12)
    canvas.setFillColor(TAUPE2)
    canvas.drawCentredString(W/2, H - 67, 'для стоматологічної клініки')

    canvas.setFont('Sans', 8)
    canvas.setFillColor(colors.HexColor('#9B8060'))
    canvas.drawCentredString(W/2, H - 82, '5 днів  ·  10 годин  ·  від нуля до самостійного ведення соцмереж')

    # Price badge
    bw, bh = 80, 24
    bx = W/2 - bw/2
    by = H - 112
    canvas.setFillColor(GOLD)
    canvas.roundRect(bx, by, bw, bh, 4, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Serif-Bold', 14)
    canvas.drawCentredString(W/2, by + 6, '$450')

    # Footer
    canvas.setFillColor(BURG2)
    canvas.rect(0, 0, W, 22, fill=1, stroke=0)
    canvas.setFillColor(TAUPE2)
    canvas.setFont('Sans', 8)
    canvas.drawCentredString(W/2, 7, 'Оксана Богданець  ·  SMM-стратег  ·  Reels-продюсер')
    canvas.restoreState()

doc = SimpleDocTemplate(
    '/home/user/site/public/dental-training.pdf',
    pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=18*mm, bottomMargin=18*mm
)

days = [
    {
        'num': '01',
        'title': 'СТОРІТЕЛІНГ',
        'topics': 'Експертні  ✦  Кейси  ✦  Болі клієнтів  ✦  Заперечення',
        'result': 'Навчимося прописувати Stories які привертають увагу цільової аудиторії, викликають довіру та залучають нових пацієнтів у клініку'
    },
    {
        'num': '02',
        'title': 'КАРУСЕЛІ',
        'topics': 'Експертні  ✦  Продуктові  ✦  Знайомство з фахівцями  ✦  Кейси  ✦  Особисті',
        'result': 'Вмієш створювати каруселі які люди гортають до кінця, зберігають і пересилають — це органічне просування сторінки'
    },
    {
        'num': '03',
        'title': 'ВОРОНКИ',
        'topics': 'Через Stories  ✦  Через каруселі  ✦  Запис на консультацію',
        'result': 'Розумієш як вибудувати систему контенту яка веде людину від першого перегляду до запису на консультацію'
    },
    {
        'num': '04',
        'title': 'ЗЙОМКА',
        'topics': 'Налаштування камери  ✦  Виставлення світла  ✦  Розкадрування',
        'result': 'Знімаєш на телефон так що виглядає як у справжнього фотографа — клієнти бачать якісну клініку ще до першого візиту'
    },
    {
        'num': '05',
        'title': 'МОНТАЖ',
        'topics': 'Базовий монтаж відео  ✦  Stories  ✦  Reels',
        'result': 'Монтуєш Stories та Reels сама, без фрілансерів і без паніки — повна самостійність у веденні соцмереж'
    },
]

s_title  = ParagraphStyle('t', fontName='Serif-Bold',  fontSize=11, textColor=BURG,  spaceAfter=7, leading=14)
s_topics = ParagraphStyle('tp', fontName='Sans',       fontSize=8.5, textColor=MUTED, spaceAfter=10, leading=13)
s_rlabel = ParagraphStyle('rl', fontName='Sans-Bold',  fontSize=7,  textColor=GOLD,  spaceAfter=4,  letterSpacing=0.8)
s_result = ParagraphStyle('r',  fontName='Sans-Italic',fontSize=9,  textColor=MUTED, leading=14)
s_daynum = ParagraphStyle('dn', fontName='Serif-Bold', fontSize=8,  textColor=TAUPE2,alignment=1, leading=10)
s_num    = ParagraphStyle('n',  fontName='Serif-Bold', fontSize=26, textColor=WHITE, alignment=1, leading=30)

story = [Spacer(1, 50*mm)]

for d in days:
    cell_left = [
        Paragraph('день', s_daynum),
        Paragraph(d['num'], s_num),
    ]
    cell_right = [
        Paragraph(d['title'], s_title),
        Paragraph(d['topics'], s_topics),
        Paragraph('РЕЗУЛЬТАТ', s_rlabel),
        Paragraph(d['result'], s_result),
    ]
    tbl = Table([[cell_left, cell_right]], colWidths=[26*mm, 132*mm])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,0), BURG),
        ('BACKGROUND',    (1,0), (1,0), WHITE),
        ('VALIGN',        (0,0), (0,0), 'MIDDLE'),
        ('VALIGN',        (1,0), (1,0), 'TOP'),
        ('ALIGN',         (0,0), (0,0), 'CENTER'),
        ('TOPPADDING',    (0,0), (0,0), 10),
        ('BOTTOMPADDING', (0,0), (0,0), 10),
        ('TOPPADDING',    (1,0), (1,0), 14),
        ('BOTTOMPADDING', (1,0), (1,0), 14),
        ('LEFTPADDING',   (1,0), (1,0), 16),
        ('RIGHTPADDING',  (1,0), (1,0), 12),
        ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#D4B896')),
        ('LINEAFTER',     (0,0), (0,0), 0.5, colors.HexColor('#D4B896')),
    ]))
    story.append(KeepTogether(tbl))
    story.append(Spacer(1, 7))

# Price block
story.append(Spacer(1, 8))
story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD, spaceAfter=14))

s_pval = ParagraphStyle('pv', fontName='Serif-Bold', fontSize=20, textColor=BURG,  alignment=1, leading=24)
s_p450 = ParagraphStyle('p4', fontName='Serif-Bold', fontSize=20, textColor=GOLD,  alignment=1, leading=24)
s_plab = ParagraphStyle('pl', fontName='Sans',       fontSize=8,  textColor=MUTED, alignment=1, spaceAfter=0)

price_tbl = Table([[
    [Paragraph('5',           s_pval), Paragraph('днів навчання',  s_plab)],
    [Paragraph('10',          s_pval), Paragraph('годин практики', s_plab)],
    [Paragraph('$450',        s_p450), Paragraph('вартість програми', s_plab)],
]], colWidths=[52*mm, 52*mm, 52*mm])
price_tbl.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), CREAM2),
    ('BOX',           (0,0), (-1,-1), 0.5, colors.HexColor('#D4B896')),
    ('INNERGRID',     (0,0), (-1,-1), 0.5, colors.HexColor('#D4B896')),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 12),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
]))
story.append(price_tbl)

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print('Done')
