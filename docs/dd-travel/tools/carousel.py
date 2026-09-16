#!/usr/bin/env python3
"""Карусель D&D Travel Club — фірмовий стиль (див. ../08-carousel-style.md).
1080x1350, фото на весь кадр, заголовок антиквою знизу ліворуч над сліпою зоною Instagram,
логотип угорі по центру, м'яке затемнення під текст.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os

import argparse, json
_ap = argparse.ArgumentParser(description='Рендер каруселі D&D Travel Club у фірмовому стилі')
_ap.add_argument('--photos', default='./photos', help='папка з фото')
_ap.add_argument('--out', default='./slides', help='куди зберігати PNG')
_ap.add_argument('--fonts', default=os.environ.get('DD_FONTS', '/mnt/skills/examples/canvas-design/canvas-fonts/'),
                 help='папка зі шрифтами Lora, Jura (Google Fonts)')
_ap.add_argument('--sysfonts', default='/usr/share/fonts/truetype/liberation/', help='папка з Liberation Sans')
_ap.add_argument('--slides', help='JSON зі списком слайдів (замість SLIDES у коді)')
_args = _ap.parse_args()
F = _args.fonts.rstrip('/') + '/'
PHOTOS = _args.photos
OUT = _args.out
os.makedirs(OUT, exist_ok=True)

W, H = 1080, 1350
MARGIN = 100

SYS = _args.sysfonts.rstrip('/') + '/'
BOLD = SYS + 'LiberationSans-Bold.ttf'
REG = SYS + 'LiberationSans-Regular.ttf'
SERIF = F + 'Lora-Regular.ttf'
ITAL = F + 'Lora-Italic.ttf'
CAPS = F + 'Jura-Medium.ttf'
FONT_VARIANTS = {
    'A': (F + 'Lora-Regular.ttf', 60, 70),        # елегантна антиква — перегук із серифом у логотипі
    'B': (F + 'PoiretOne-Regular.ttf', 66, 74),   # тонкий геометричний, ар-деко — «дорога простота»
}
HEAD, HEAD_SIZE, HEAD_LH = FONT_VARIANTS['A']


def font(p, s):
    return ImageFont.truetype(p, s)


# ---------- фото ----------

def photo(name, y_focus=0.5, trim=0.07):
    """Кроп 4:5 із фото, з відступом trim від краю (щоб зрізати іконки), ресайз до 1080x1350."""
    im = Image.open(f'{PHOTOS}/{name}').convert('RGB')
    w, h = im.size
    # спочатку відрізаємо краї
    tx, ty = int(w * trim), int(h * trim)
    im = im.crop((tx, ty, w - tx, h - ty))
    w, h = im.size
    target = W / H
    if w / h > target:            # занадто широке — ріжемо боки
        nw = int(h * target)
        x0 = (w - nw) // 2
        im = im.crop((x0, 0, x0 + nw, h))
    else:                          # занадто високе — ріжемо верх/низ
        nh = int(w / target)
        y0 = int((h - nh) * y_focus)
        im = im.crop((0, y0, w, y0 + nh))
    return im.resize((W, H), Image.LANCZOS)


def scrim(img, text_top, bottom_strength=160, top_strength=95):
    """Текст знизу: повне затемнення від text_top до низу, вгору сходить за ~280px; легке згори під логотип."""
    ys = np.arange(H)[:, None].astype(float)
    fade = np.clip((text_top - ys) / 340.0, 0, 1)
    bot = bottom_strength * (1 - fade) ** 1.3
    top = top_strength * np.clip(1 - ys / (H * 0.22), 0, 1) ** 1.5
    m = np.maximum(bot, top) * np.ones((1, W))
    mask = Image.fromarray(np.clip(m, 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(28))
    a = np.asarray(mask).astype(float)[..., None] / 255
    base = np.asarray(img).astype(float)
    return Image.fromarray((base * (1 - a)).astype('uint8'))


# ---------- текст ----------

def tracked(d, cx, y, text, fnt, fill, tracking=0):
    total = sum(d.textlength(c, font=fnt) for c in text) + tracking * (len(text) - 1)
    x = cx - total / 2
    for c in text:
        d.text((x, y), c, font=fnt, fill=fill)
        x += d.textlength(c, font=fnt) + tracking
    return total


def wrap(d, text, fnt, max_w):
    words, lines, cur = text.split(), [], ''
    for w in words:
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def logo(d):
    cx, y = W / 2, 56
    tracked(d, cx, y, 'D&D', font(SERIF, 50), (255, 255, 255), tracking=1)
    d.polygon([(cx, y + 62), (cx + 3, y + 65), (cx, y + 68), (cx - 3, y + 65)], fill=(255, 255, 255))
    tracked(d, cx, y + 74, 'TRAVEL CLUB', font(CAPS, 16), (255, 255, 255), tracking=7)


def divider(d, y, width=520, x0=None):
    x0 = W / 2 - width / 2 if x0 is None else x0
    x1 = x0 + width
    d.line([(x0, y), (x1, y)], fill=(255, 255, 255), width=2)
    x = x0
    while x < x1:
        d.line([(x, y + 7), (x + 3, y + 7)], fill=(255, 255, 255), width=1)
        x += 7


def callout(d, y, line1, line2):
    """Біла плашка з жовтим маркером і стрілкою (як на слайді 01 ЗАПИТ)."""
    f1, f2 = font(REG, 27), font(ITAL, 30)
    px, py = 30, 24
    w1, w2 = d.textlength(line1, font=f1), d.textlength(line2, font=f2)
    bw = max(w1, w2) + px * 2
    bh = py * 2 + 76
    bx = W / 2 - bw / 2 + 50
    d.rounded_rectangle([bx, y, bx + bw, y + bh], radius=12, fill=(255, 255, 255))
    d.text((bx + px, y + py), line1, font=f1, fill=(40, 40, 40))
    ty = y + py + 40
    d.rectangle([bx + px - 5, ty + 8, bx + px + w2 + 5, ty + 34], fill=(250, 232, 150))
    d.text((bx + px, ty), line2, font=f2, fill=(40, 40, 40))
    ax, ay = bx - 118, y - 26
    d.arc([ax, ay, ax + 120, ay + 96], start=180, end=312, fill=(255, 255, 255), width=4)
    d.polygon([(ax + 102, ay + 68), (ax + 122, ay + 80), (ax + 98, ay + 90)], fill=(255, 255, 255))


# ---------- слайд ----------

SAFE_BOTTOM = H - 270   # нижня межа тексту — над зоною підпису/кнопок Instagram

def render(idx, photo_name, heading, body='', emphasis='', y_focus=0.5, call=None, tag=''):
    img = photo(photo_name, y_focus=y_focus)
    d0 = ImageDraw.Draw(img)

    f_h, f_b = font(HEAD, HEAD_SIZE), font(REG, 31)
    X = 60
    maxw = W - X - 90
    hl = wrap(d0, heading, f_h, maxw)
    bl = wrap(d0, body, f_b, maxw) if body else []
    el = wrap(d0, emphasis, f_b, maxw) if emphasis else []
    lh_h, lh_b = HEAD_LH, 41
    block = len(hl) * lh_h + (16 + len(bl) * lh_b if bl else 0) + (20 + len(el) * lh_b if el else 0)
    y = SAFE_BOTTOM - block

    img = scrim(img, text_top=y - 30)
    d = ImageDraw.Draw(img)
    logo(d)

    for ln in hl:
        d.text((X, y), ln, font=f_h, fill=(255, 255, 255))
        y += lh_h
    if bl:
        y += 16
        for ln in bl:
            d.text((X, y), ln, font=f_b, fill=(235, 235, 235))
            y += lh_b
    if el:
        y += 20
        for ln in el:
            d.text((X, y), ln, font=f_b, fill=(255, 255, 255))
            y += lh_b

    p = f'{OUT}/slide{idx}{tag}.png'
    img.save(p)
    return p


SLIDES = [
    dict(photo_name='pool.jpg', y_focus=0.45,
         heading='D&D Travel Club',
         body='Туристична агенція про подорожі, які залишаються спогадами, що хочеться повторити.'),
    dict(photo_name='beach.jpg', y_focus=0.5,
         heading='Підбираємо під конкретну людину',
         body='Відпочинок з урахуванням ритму, звичок, складу сім’ї, очікувань від готелю, сервісу і самої подорожі.'),
    dict(photo_name='desk.jpg', y_focus=0.4,
         heading='Усвідомлений вибір замість списку варіантів',
         body='Для нас важливо, щоб клієнт не просто отримував список варіантів за заданим бюджетом,',
         emphasis='а зробив усвідомлений вибір, розуміючи, чому ці варіанти підходять саме йому.'),
]

if __name__ == '__main__':
    slides = json.load(open(_args.slides, encoding='utf-8')) if _args.slides else SLIDES
    for i, s in enumerate(slides, 1):
        print('✓', render(i, **s))
    n = len(slides)
    sheet = Image.new('RGB', (n * 370, 470), (18, 18, 18))
    for i in range(1, n + 1):
        th = Image.open(f'{OUT}/slide{i}.png'); th.thumbnail((360, 450))
        sheet.paste(th, ((i - 1) * 370 + 5, 10))
    sheet.save(f'{OUT}/_sheet.jpg', quality=90)
