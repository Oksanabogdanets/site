#!/usr/bin/env python3
"""Логотип в один рядок «OKSANA BOGDANETS» для шапки нової версії (Оксана 01.10: «зробити на весь ряд»).

Той самий шрифт і колір, що у wordmark2.png (Oswald 700, золото #f6d4aa), але одним рядком,
щоб на телефоні логотип тягнувся від лівого краю шапки до бургера.
Запуск: python3 wordmark_line.py → assets/wordmark_line.png, далі site2.py.
"""
import os
from PIL import Image, ImageDraw, ImageFont

S = os.path.dirname(os.path.abspath(__file__))
GOLD = (246, 212, 170, 255)

font = ImageFont.truetype(os.path.join(S, 'fonts', 'oswald.ttf'), 220)
font.set_variation_by_axes([700])
text = 'OKSANA BOGDANETS'
im = Image.new('RGBA', (4000, 400), (0, 0, 0, 0))
ImageDraw.Draw(im).text((20, 20), text, font=font, fill=GOLD)
im = im.crop(im.getbbox())
im.save(os.path.join(S, 'assets', 'wordmark_line.png'), optimize=True)
print('wordmark_line.png', im.size)
