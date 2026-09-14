#!/usr/bin/env python3
"""Колаж відгуків 1680x461 з повнорозмірних скріншотів чатів — як у конкурента
(reels-agency.ru): скріни в ТЕМНІЙ темі Telegram на темному тлі, без шпалер.

Використання:
    python3 make_reviews.py скрін1.png скрін2.png скрін3.png
Кожен скрін: обрізаємо однорідні краї (шапка/поле вводу/рамка телефону не потрібні —
зроби скрін лише зони повідомлень), масштабуємо до висоти ~400, кладемо на #0a0a0a
з округленими кутами. Результат -> assets/chats.jpg, далі build.py.
"""
import sys, os
from PIL import Image, ImageDraw
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'chats.jpg')
W, H, GAP, PAD, BG, R = 1680, 461, 24, 24, (10, 10, 10), 22


def trim(im, thr=8):
    """Зрізає однорідні поля по краях (рамка телефону, порожні смуги)."""
    a = np.asarray(im.convert('RGB')).astype(int)
    ref = np.median(np.concatenate([a[:3].reshape(-1, 3), a[-3:].reshape(-1, 3)]), axis=0)
    d = np.abs(a - ref).sum(axis=2)
    rows = np.where((d > thr).mean(axis=1) > 0.01)[0]; cols = np.where((d > thr).mean(axis=0) > 0.01)[0]
    if len(rows) == 0 or len(cols) == 0:
        return im
    return im.crop((cols.min(), rows.min(), cols.max() + 1, rows.max() + 1))


def rounded(im, r=R):
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), r, fill=255)
    out = Image.new('RGB', im.size, BG); out.paste(im, (0, 0), m); return out


def main(files):
    n = len(files); slot_w = (W - 2 * PAD - GAP * (n - 1)) // n
    canvas = Image.new('RGB', (W, H), BG); x = PAD
    for f in files:
        im = trim(Image.open(f))
        sc = min(slot_w / im.width, (H - 2 * PAD) / im.height)
        im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
        im = rounded(im)
        canvas.paste(im, (x + (slot_w - im.width) // 2, (H - im.height) // 2)); x += slot_w + GAP
        print(os.path.basename(f), '->', im.size)
    canvas.save(OUT, quality=92); print('->', OUT, canvas.size)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('дай шляхи до скріншотів')
    main(sys.argv[1:])
