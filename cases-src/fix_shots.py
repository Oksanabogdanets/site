#!/usr/bin/env python3
"""Скріни кейсів 01 (Звільнимо) і 04 (Muza Body) — з оригіналів КП (PDF), а не з Canva-сторінок.

У Canva-варіанті кружечок-логотип Звільнимо різався краєм картки (Оксана 26.09: «не взято в круг»),
у Muza Body на скрін ПІСЛЯ налазив стікер Instagram, а ДО обрізав аватар («вирізано некрасиво»).
Джерела: kp/*.png — картинки з КомерційнаПропПрезентація.pdf (стор. 6–7), витягнуті pypdf.
Запуск: python3 fix_shots.py  → assets/zvilnymo_before.jpg, zvilnymo_after_tt.jpg, mbody_before.jpg, mbody_after.jpg
"""
import os
from PIL import Image, ImageDraw, ImageFilter

S = os.path.dirname(os.path.abspath(__file__))
KP, A = os.path.join(S, 'kp'), os.path.join(S, 'assets')


def rounded(im, r, inset=0):
    """Скрін з заокругленими кутами → RGBA з прозорими кутами (рамку джерела вже зрізано crop-ом)."""
    im = im.crop((inset, inset, im.width - inset, im.height - inset)).convert('RGBA')
    m = Image.new('L', (im.width * 4, im.height * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width * 4 - 1, im.height * 4 - 1), r * 4, fill=255)
    im.putalpha(m.resize(im.size, Image.LANCZOS))
    return im


def card(src, out, ratio, bg, crop=None, pad=0.05, width=1440, r=12):
    """Вирізка → на чисте тло потрібної пропорції з полями → апскейл до ширини картки на сайті."""
    im = Image.open(os.path.join(KP, src)).convert('RGB')
    if crop:
        im = im.crop(crop)
    im = rounded(im, r)
    w, h = im.size
    tw = w * (1 + 2 * pad); th = tw / ratio
    if th < h * (1 + 2 * pad):
        th = h * (1 + 2 * pad); tw = th * ratio
    canvas = Image.new('RGB', (int(round(tw)), int(round(th))), bg)
    canvas.paste(im, (int((tw - w) / 2), int((th - h) / 2)), im)
    canvas = canvas.resize((width, int(round(width / ratio))), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 3))
    canvas.save(os.path.join(A, out), quality=90)
    print(out, canvas.size)


def zv_after_tt():
    """Композит «ПІСЛЯ + TikTok-стрічка» (assets/zvilnymo_after_tt.jpg, 1432×1580): міняємо лише верхній скрін."""
    p = os.path.join(A, 'zvilnymo_after_tt.jpg')
    comp = Image.open(p).convert('RGB')
    ImageDraw.Draw(comp).rectangle((0, 0, comp.width, 600), fill=(0, 0, 0))
    shot = rounded(Image.open(os.path.join(KP, 'zv_after.png')).convert('RGB').crop((14, 9, 416, 146)), 16)
    W = 1250; H = int(round(W * shot.height / shot.width))
    shot = shot.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 3))
    comp.paste(shot, ((comp.width - W) // 2, 62), shot)
    comp.save(p, quality=90); print('zvilnymo_after_tt.jpg', comp.size, 'скрін', shot.size)


if __name__ == '__main__':
    # у джерелах чорна (Звільнимо, 12/7px) або оливкова (Muza Body, 6/3px) рамка — зрізаємо crop-ом
    card('zv_before.png', 'zvilnymo_before.jpg', 1432 / 564, (255, 255, 255), crop=(14, 9, 390, 146), r=16)
    zv_after_tt()
    card('mb_before.png', 'mbody_before.jpg', 1440 / 567, (12, 12, 12), crop=(7, 4, 256, 118), r=10)
    card('mb_after.png', 'mbody_after.jpg', 1440 / 627, (255, 255, 255), crop=(7, 4, 288, 110), r=10)
