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
    ImageDraw.Draw(comp).rectangle((0, 0, comp.width, 650), fill=(0, 0, 0))   # до 650: біла лінія старого скріна на 608–616
    shot = rounded(Image.open(os.path.join(KP, 'zv_after.png')).convert('RGB').crop((14, 9, 416, 146)), 16)
    W = 1250; H = int(round(W * shot.height / shot.width))
    shot = shot.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 60, 3))
    comp.paste(shot, ((comp.width - W) // 2, 62), shot)
    comp.save(p, quality=90); print('zvilnymo_after_tt.jpg', comp.size, 'скрін', shot.size)


def zv_tt_middle():
    """Середня плитка TikTok-стрічки кейсу 01 — дрібний скрін профілю, нічого не читалось (Оксана 29.09).
    Ставимо обкладинку ролика Звільнимо з переглядами (assets/k02.jpg, 2.4M) у ту саму рамку 456×812, радіус 28."""
    p = os.path.join(A, 'zvilnymo_after_tt.jpg')
    comp = Image.open(p).convert('RGB')
    x0, y0, x1, y1 = 488, 768, 944, 1580
    tile = Image.open(os.path.join(A, 'k02.jpg')).convert('RGB').resize((x1 - x0, y1 - y0), Image.LANCZOS)
    ImageDraw.Draw(comp).rectangle((x0, y0, x1 - 1, y1 - 1), fill=(0, 0, 0))
    comp.paste(tile, (x0, y0), rounded_mask(tile.size, 28))
    comp.save(p, quality=90); print('zvilnymo_after_tt.jpg: середня плитка = k02')


def zv_tt_label():
    """Підпис над стрічкою: «TikTok · @zvilnymo» → «@zvilnymo.com.ua» (справжній акаунт, 29.09).
    «TikTok ·» лишаємо як є; нік перемальовуємо Verdana Bold 50.5 тим самим кольором, по тій самій базовій лінії."""
    from PIL import ImageFont
    p = os.path.join(A, 'zvilnymo_after_tt.jpg'); im = Image.open(p).convert('RGB'); d = ImageDraw.Draw(im)
    f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Verdana Bold.ttf', 50.5)
    d.rectangle((284, 655, im.width, 745), fill=(0, 0, 0))
    d.text((290, 712), '@zvilnymo.com.ua', font=f, fill=(240, 212, 180), anchor='ls')
    im.save(p, quality=90); print('zvilnymo_after_tt.jpg: підпис @zvilnymo.com.ua')


def zv_after_new():
    """Кейс 01, «ПІСЛЯ» для нової версії сайту (Оксана 29.09: «Замени после»): свіжий скрін профілю TikTok
    @zvilnymo.ua — шапка (238,4 тис. підписників, 1,4 млн вподобань) + перший ряд роликів з переглядами.
    Без статус-бару телефона і рядків з малими переглядами. 2× для чіткості на телефонах."""
    im = Image.open(os.path.join(S, 'covers-src', 'zvilnymo_tiktok_profile_2909.jpg')).convert('RGB')
    c = im.crop((0, 145, im.width, 838))
    c = c.resize((c.width * 2, c.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 50, 2))
    c.save(os.path.join(A, 'zvilnymo_after_new.jpg'), quality=90); print('zvilnymo_after_new.jpg', c.size)


def zv_after_card():
    """Кейс 01, «ПІСЛЯ» для нової версії (Оксана 29.09: «той скрін має бути оформлений так само, як ДО»):
    біла картка того ж розміру, що й ДО (1432×564), з шапкою свіжого профілю @zvilnymo.ua (238,4 тис.),
    під нею — рядок «TikTok · @zvilnymo.ua» і три ролики з мільйонами (з попереднього композиту)."""
    from PIL import ImageFont
    src = Image.open(os.path.join(S, 'covers-src', 'zvilnymo_tiktok_profile_2909.jpg')).convert('RGB')
    head = src.crop((10, 140, 579, 460))
    ratio = 1432 / 564; w, h = head.size; pad = 0.05
    tw = w * (1 + 2 * pad); th = tw / ratio
    if th < h * (1 + 2 * pad):
        th = h * (1 + 2 * pad); tw = th * ratio
    card = Image.new('RGB', (round(tw), round(th)), (255, 255, 255))
    card.paste(head, (round((tw - w) / 2), round((th - h) / 2)))
    card = card.resize((1432, 564), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.2, 50, 2))
    tt = Image.open(os.path.join(A, 'zvilnymo_after_tt.jpg')).convert('RGB').crop((0, 650, 1432, 1580))
    gap = 40
    comp = Image.new('RGB', (1432, 564 + gap + tt.height), (0, 0, 0))
    comp.paste(card, (0, 0), rounded_mask(card.size, 56))
    comp.paste(tt, (0, 564 + gap))
    d = ImageDraw.Draw(comp); f = ImageFont.truetype('/System/Library/Fonts/Supplemental/Verdana Bold.ttf', 50.5)
    y0 = 564 + gap
    d.rectangle((284, y0 + 5, comp.width, y0 + 95), fill=(0, 0, 0))
    d.text((290, y0 + 62), '@zvilnymo.ua', font=f, fill=(240, 212, 180), anchor='ls')
    comp.save(os.path.join(A, 'zvilnymo_after_new.jpg'), quality=90)
    print('zvilnymo_after_new.jpg', comp.size, 'label center %.1f%%' % ((y0 + 46) / comp.height * 100))


def rounded_mask(size, r):
    m = Image.new('L', (size[0] * 4, size[1] * 4), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] * 4 - 1, size[1] * 4 - 1), r * 4, fill=255)
    return m.resize(size, Image.LANCZOS)


if __name__ == '__main__':
    # у джерелах чорна (Звільнимо, 12/7px) або оливкова (Muza Body, 6/3px) рамка — зрізаємо crop-ом
    card('zv_before.png', 'zvilnymo_before.jpg', 1432 / 564, (255, 255, 255), crop=(14, 8, 390, 147), r=36)   # r більший за радіус кутів оригіналу, інакше чорно-сірі дуги
    zv_after_tt()
    zv_tt_middle()
    zv_tt_label()
    card('mb_before.png', 'mbody_before.jpg', 1440 / 567, (4, 4, 6), crop=(9, 11, 254, 133), r=10)   # фон = колір країв скріна, щоб не було видно прямокутника; всередині оливкової рамки телефона, з рядком «Здоров'я/Краса»
    card('mb_after.png', 'mbody_after.jpg', 1440 / 627, (255, 255, 250), crop=(8, 5, 284, 102), r=10)    # всередині кремової рамки; низ — по проміжку перед біо (було посеред рядка)
