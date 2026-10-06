#!/usr/bin/env python3
"""Картинка-прев'ю посилання (og:image) 1200x630 — все важливе в центральному квадраті 630x630.

Оксана 06.10: у Direct Instagram прев'ю обрізалось (Instagram показує лише середину картинки):
текст був ліворуч, фото праворуч. Тепер фото, заголовок і ім'я — по центру, по боках лише тло.
Запуск: python3 cases-src/og_image.py → cases/og-cases.jpg
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(S), 'cases', 'og-cases.jpg')
W, H = 1200, 630
GOLD, WHITE, MUTED = (246, 212, 170), (255, 255, 255), (170, 160, 150)


def font(size, weight=700):
    f = ImageFont.truetype(os.path.join(S, 'fonts', 'oswald.ttf'), size)
    f.set_variation_by_axes([weight])
    return f


def center_text(d, y, text, f, fill, spacing=0):
    w = d.textlength(text, font=f) + spacing * (len(text) - 1)
    x = (W - w) / 2
    if not spacing:
        d.text((x, y), text, font=f, fill=fill)
        return
    for ch in text:                       # розрідження для дрібних капсів
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + spacing


img = Image.new('RGB', (W, H), (10, 8, 7))
glow = Image.new('L', (W, H), 0)
ImageDraw.Draw(glow).ellipse((W / 2 - 420, -260, W / 2 + 420, 520), fill=70)
glow = glow.filter(ImageFilter.GaussianBlur(120))
img = Image.composite(Image.new('RGB', (W, H), (60, 44, 28)), img, glow)

# фото — коло по центру
src = Image.open(os.path.join(S, 'assets', 'oksana_about_suit.jpg')).convert('RGB')
src = src.crop((170, 40, 630, 500)).resize((210, 210), Image.LANCZOS)   # ближче до обличчя
mask = Image.new('L', (210 * 4, 210 * 4), 0)
ImageDraw.Draw(mask).ellipse((0, 0, 210 * 4 - 1, 210 * 4 - 1), fill=255)
mask = mask.resize((210, 210), Image.LANCZOS)
d = ImageDraw.Draw(img)
cx, top = W // 2, 46
d.ellipse((cx - 109, top - 4, cx + 109, top + 214), outline=GOLD, width=3)
img.paste(src, (cx - 105, top), mask)

d = ImageDraw.Draw(img)
center_text(d, 282, 'REELS ПІД КЛЮЧ · КИЇВ', font(22, 500), GOLD, spacing=4)
center_text(d, 322, 'REELS, ЯКІ', font(60), WHITE)
center_text(d, 394, 'ПРИВОДЯТЬ КЛІЄНТІВ', font(60), GOLD)
center_text(d, 488, 'ОКСАНА БОГДАНЕЦЬ', font(28, 600), WHITE, spacing=3)
center_text(d, 530, 'oksanabogdanets.com.ua', font(24, 400), MUTED)
img.save(OUT, quality=90, optimize=True, progressive=True)
print('og-cases.jpg', img.size)
