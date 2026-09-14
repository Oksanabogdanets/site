#!/usr/bin/env python3
"""Precisely crop real materials out of the exported Canva pages."""
import os, json
from PIL import Image
import numpy as np

S = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(S, 'canva'); A = os.path.join(S, 'assets')
OUT = os.path.join(S, 'cut'); os.makedirs(OUT, exist_ok=True)

def page(n): return Image.open(os.path.join(C, f'p{n:02d}.png')).convert('RGB')

def card(name, n, box, target_ratio, bg=(255, 255, 255), pad=0.06):
    """Crop a screenshot and letterbox it onto a clean canvas of the target ratio."""
    im = page(n).crop(box)
    w, h = im.size
    tw = w * (1 + pad * 2)
    th = tw / target_ratio
    if th < h * (1 + pad * 2):
        th = h * (1 + pad * 2); tw = th * target_ratio
    canvas = Image.new('RGB', (int(round(tw)), int(round(th))), bg)
    canvas.paste(im, (int((tw - w) / 2), int((th - h) / 2)))
    canvas = canvas.resize((1440, int(1440 / target_ratio)), Image.LANCZOS)
    canvas.save(os.path.join(OUT, name + '.jpg'), quality=92)
    print(name, box, '->', canvas.size)

def circle(name, n, box, size=320):
    im = page(n).crop(box)
    s = min(im.size)
    im = im.crop(((im.width - s) // 2, (im.height - s) // 2, (im.width + s) // 2, (im.height + s) // 2)).resize((size, size), Image.LANCZOS)
    mask = Image.new('L', (size * 4, size * 4), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4, size * 4), fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    out = Image.new('RGBA', (size, size), (0, 0, 0, 0)); out.paste(im, (0, 0), mask)
    out.save(os.path.join(OUT, name + '.png'))
    print(name, box, '-> circle')

def cover(name, n, box, W=609, H=1095):
    """Crop a vertical reel cover to exact 9:16 without losing the view-count badge."""
    im = page(n); l, t, r, b = box
    w, h = r - l, b - t
    want = W / H
    if w / h > want:                      # too wide -> trim sides
        nw = h * want; l += (w - nw) / 2; r -= (w - nw) / 2
    else:                                 # too tall -> widen if possible, else trim top
        nw = h * want
        if l - (nw - w) / 2 >= 0 and r + (nw - w) / 2 <= im.width:
            l -= (nw - w) / 2; r += (nw - w) / 2
        else:
            nh = w / want; t = b - nh
    im.crop((int(l), int(t), int(r), int(b))).resize((W, H), Image.LANCZOS).save(os.path.join(OUT, name + '.jpg'), quality=88)

# ---------- case screenshots ----------
card('nina_before', 8, (395, 190, 1105, 432), 1432 / 564)
card('nina_after', 9, (198, 272, 812, 497), 1432 / 624)
card('julia_before', 5, (322, 222, 990, 498), 1440 / 616)
card('julia_after', 6, (342, 240, 1018, 502), 1440 / 616)
card('mbody', 14, (168, 262, 842, 487), 720 / 308)
card('zvilnymo_before', 12, (145, 238, 838, 408), 1432 / 564)
card('zvilnymo_after', 12, (412, 332, 866, 498), 1432 / 624)

# ---------- avatars ----------
circle('ava_zv1', 12, (168, 260, 282, 376))
circle('ava_zv2', 12, (438, 352, 548, 464))
circle('ava_nina', 8, (400, 238, 554, 388))
circle('ava_julia', 6, (348, 298, 508, 468))
circle('ava_mbody', 14, (521, 306, 592, 378))

# ---------- reel covers ----------
boxes = json.load(open(os.path.join(C, 'boxes.json')))
manual = [(12, (866, 200, 1032, 482)), (12, (1028, 334, 1224, 616)), (9, (888, 312, 1054, 578)), (9, (1018, 152, 1198, 452))]
auto = []
for fn, bs in boxes.items():
    n = int(fn[1:3])
    if n in (3, 4, 5, 6, 8, 12, 14, 22): continue
    for x0, y0, x1, y1, area in bs:
        w, h = x1 - x0, y1 - y0
        if w < 140 or h < 190: continue
        if not (1.15 < h / w < 2.3): continue
        auto.append((n, (x0, y0, x1, y1)))
allb = manual + auto
for i, (n, bx) in enumerate(allb, 1):
    cover(f'k{i:02d}', n, bx)
print('covers', len(allb))

# ---------- reviews collage 1680x461 ----------
chats = [(22, (44, 133, 418, 352)), (22, (462, 168, 848, 418)), (22, (904, 208, 1258, 384)), (22, (44, 412, 420, 548)), (22, (730, 494, 1144, 656))]
canvas = Image.new('RGB', (1680, 461), (10, 10, 10))
x = 24
for n, bx in chats[:3]:
    im = page(n).crop(bx)
    k = min(413 / im.width, 413 / im.height * 1.0)
    sc = min((1680 - 96) / 3 / im.width, 400 / im.height)
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.LANCZOS)
    canvas.paste(im, (x, (461 - im.height) // 2)); x += im.width + 24
canvas.save(os.path.join(OUT, 'chats.jpg'), quality=92)
print('chats ->', canvas.size)

# ---------- client logos row (page 3) ----------
p3 = page(3)
print('done, files:', len(os.listdir(OUT)))
