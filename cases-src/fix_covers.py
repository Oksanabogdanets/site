#!/usr/bin/env python3
"""Обкладинки з переглядами у стрічці «Про нас» (k01 1.9M, k02 2.4M, k03 257 тис., k04 354 тис.).

Оксана 23.09 і 29.09: «там, де скріни з переглядами — зробити дуже акуратно, там жахливі скріни».
Старі k-файли були вирізані зі сторінок Canva: білі рамки, шматок сусідньої картки, обрізаний текст
«ПРОДАТИ НИРКУ?». Нові — з оригіналів у PDF комерційної пропозиції (стор. 6 і 8), збільшених у 4 рази
Real-ESRGAN (kp/cov_*.jpg), обрізаних до 9:16 без втрати тексту й цифри переглядів. Підпис на 1.9M —
з оригіналу (kp/cov_1_9m_src.png), бо нейромережа ламає дрібні літери.
2.4M у PDF має пропорцію 3:4 і текст на всю ширину — тож фон зверху добудовуємо з розмитого верху кадру.
Запуск: python3 fix_covers.py → assets/k01.jpg … k04.jpg, далі build.py.
"""
import os
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

S = os.path.dirname(os.path.abspath(__file__))
KP, A = os.path.join(S, 'kp'), os.path.join(S, 'assets')
W, H = 720, 1280


def save(im, name):
    im = im.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.0, 40, 2))
    im.save(os.path.join(A, name), quality=90, optimize=True, progressive=True)
    print(name, im.size)


def load(src):
    return Image.open(os.path.join(KP, src)).convert('RGB')


def crop916_im(im, x0):
    w = round(im.height * W / H)
    return im.crop((x0, 0, x0 + w, im.height))


def crop916(src, x0):
    return crop916_im(load(src), x0)


def extend_top(src, side):
    """Кадр 3:4 → 9:16: ширину лишаємо (текст на всю ширину), зверху добудовуємо розмитий фон."""
    im = Image.open(os.path.join(KP, src)).convert('RGB')
    im = im.crop((side, 0, im.width - side, im.height))
    w, h = im.size
    th = round(w * H / W); add = th - h
    top = im.crop((0, 0, w, 66)).resize((w, add), Image.BICUBIC)            # смуга стіни з неоном до маківки (голова з y≈75)
    top = top.filter(ImageFilter.GaussianBlur(36))
    top = ImageEnhance.Brightness(top).enhance(0.78)
    canvas = Image.new('RGB', (w, th)); canvas.paste(top, (0, 0)); canvas.paste(im, (0, add))
    feather = 90                                                            # м'який перехід у кадр
    band = canvas.crop((0, add - feather, w, add + feather)).filter(ImageFilter.GaussianBlur(10))
    mask = Image.linear_gradient('L').resize((w, 2 * feather))
    mask = Image.eval(mask, lambda v: 255 - abs(255 - 2 * v))            # 0 → 255 → 0 по висоті смуги
    canvas.paste(band, (0, add - feather), mask)
    shade = Image.linear_gradient('L').resize((w, add)).point(lambda v: int(v * .55 + 115))
    dark = Image.new('RGB', (w, add), (8, 6, 20))
    canvas.paste(Image.composite(canvas.crop((0, 0, w, add)), dark, shade), (0, 0))   # темніше до верху
    return canvas


def caption_from_source(im, src_small, box, feather=10):
    """Real-ESRGAN ламає дрібні літери (підпис «Топ 5 фраз, які бояться колектори» ставав кашею).
    На ділянці підпису беремо оригінал з PDF, збільшений звичайним LANCZOS, — він м'якший, але читається."""
    s = Image.open(os.path.join(KP, src_small)).convert('RGB').resize(im.size, Image.LANCZOS)
    s = s.filter(ImageFilter.UnsharpMask(1.6, 80, 2))
    x0, y0, x1, y1 = box
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle(box, (y1 - y0) // 2, fill=255)
    im.paste(s, (0, 0), m.filter(ImageFilter.GaussianBlur(feather / 2)))
    return im


if __name__ == '__main__':
    k01 = caption_from_source(load('cov_1_9m.jpg'), 'cov_1_9m_src.png', (214, 604, 618, 744))
    save(crop916_im(k01, 8), 'k01.jpg')                 # неон, підпис і «1.9M» — усе в кадрі
    save(extend_top('cov_2_4m.jpg', 24), 'k02.jpg')     # «КОЛЕКТОР ЗМУШУЄ ПРОДАТИ НИРКУ?» цілим
    save(crop916('cov_257k.jpg', 56), 'k03.jpg')
    save(crop916('cov_354k.jpg', 50), 'k04.jpg')        # «354 тис.» лишаємо, де його ставить Instagram
