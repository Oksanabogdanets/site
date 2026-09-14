#!/usr/bin/env python3
"""Generate Oksana's replacement assets for the reels-agency clone."""
import os, subprocess, sys, glob
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(S, 'assets'); os.makedirs(A, exist_ok=True)
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PH = '/Users/bogdanets94gmail.com/Desktop/всі проекти /фото для сторіс та каруселей'
VID = ['/Users/bogdanets94gmail.com/Desktop/всі проекти /відео кейси/БачилиСайт.mov',
       '/Users/bogdanets94gmail.com/Desktop/всі проекти /target/reels_кейс.mp4',
       '/Users/bogdanets94gmail.com/Desktop/всі проекти /target/REELS під ключ (3).mp4']
KVIZ = '/Users/bogdanets94gmail.com/Desktop/всі проекти /створення сайтів /my-landing/kviz'
GOLD = '#f6d4aa'

FONTS = "<link href='https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Montserrat:wght@400;500;600;700;800&display=swap' rel='stylesheet'>"
BASE = ("*{box-sizing:border-box;margin:0;padding:0}body{background:#000;color:#fff;font-family:'Montserrat',Arial,sans-serif;overflow:hidden}"
        ".osw{font-family:'Oswald',sans-serif;text-transform:uppercase}.g{color:%s}" % GOLD)

def render(name, w, h, body, css='', transparent=False):
    html = f"<!doctype html><html><head><meta charset='utf-8'>{FONTS}<style>{BASE}body{{width:{w}px;height:{h}px;{'background:transparent' if transparent else ''}}}{css}</style></head><body>{body}</body></html>"
    hp = os.path.join(S, f'_{name}.html'); open(hp, 'w').write(html)
    out = os.path.join(A, name + '.png')
    args = [CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--window-size={w},{h}',
            '--virtual-time-budget=4000', f'--screenshot={out}', 'file://' + hp]
    if transparent: args.insert(1, '--default-background-color=00000000')
    subprocess.run(args, capture_output=True)
    print('render', name, os.path.exists(out))

# ---------- 1. frames from videos (vertical covers 609x1095) ----------
def frames():
    specs = [(0, 2), (0, 9), (0, 18), (0, 27), (0, 36), (1, 3), (1, 9), (1, 14), (1, 20), (1, 26), (2, 1), (2, 4), (2, 6), (0, 13)]
    for i, (v, t) in enumerate(specs, 1):
        out = os.path.join(A, f'c{i}.jpg')
        subprocess.run(['ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', VID[v], '-frames:v', '1',
                        '-vf', 'scale=-2:1095,crop=609:1095', '-q:v', '4', out], capture_output=True)
    print('frames', len(glob.glob(os.path.join(A, 'c*.jpg'))))

# ---------- 2. photos (portraits) ----------
def photos():
    srcs = sorted(f for f in os.listdir(PH) if f.lower().endswith('.jpg') and ' 2' not in f)
    srcs += [f for f in os.listdir(PH) if f.upper().endswith('.JPG')]
    n = 0
    for f in srcs:
        n += 1
        im = Image.open(os.path.join(PH, f)); im = im.convert('RGB')
        im.thumbnail((1200, 1600)); im.save(os.path.join(A, f'p{n}.jpg'), quality=82, optimize=True)
    print('photos', n)
    # avatar from kviz
    im = Image.open(os.path.join(KVIZ, 'ksyusha-v2.jpg')).convert('RGB').resize((888, 888)); im.save(os.path.join(A, 'ava_oksana.jpg'), quality=85)

# ---------- 3. icon recolor (purple/lime -> gold) ----------
def recolor(src_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    gold = (246, 212, 170)
    cnt = 0
    for f in os.listdir(src_dir):
        p = os.path.join(src_dir, f)
        if not f.lower().endswith('.png'): continue
        im = Image.open(p)
        if max(im.size) > 600: continue
        im = im.convert('RGBA'); px = im.load(); ch = 0
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                r, g, b, a = px[x, y]
                if a == 0: continue
                purple = b > 180 and r > 150 and b > r and b > g and (b - g) > 40
                lime = g > 200 and b < 170 and r > 170 and g > r
                if purple or lime:
                    px[x, y] = (gold[0], gold[1], gold[2], a); ch += 1
        if ch: im.save(os.path.join(out_dir, f)); cnt += 1
    print('recolored icons', cnt)

# ---------- 4. rendered cards ----------
def cards():
    # monogram logo 540x540 and 180x180
    logo = "<div style='width:100%;height:100%;border-radius:50%;background:#000;border:6px solid {g};display:flex;flex-direction:column;align-items:center;justify-content:center'><div class='osw g' style='font-size:{fs}px;font-weight:700;line-height:.95;text-align:center'>OKSANA<br>BOGDANETS</div></div>"
    render('logo540', 540, 540, logo.format(g=GOLD, fs=78), transparent=True)
    render('logo180', 180, 180, logo.format(g=GOLD, fs=26), transparent=True)
    render('wordmark', 66, 35, f"<div class='osw g' style='font-size:13px;font-weight:700;line-height:1;text-align:center;padding-top:4px'>OKSANA<br>BOGDANETS</div>", transparent=True)
    # badge 321x289 rotated card "15+ ніш"
    render('badge', 321, 289, f"<div style='position:absolute;left:28px;top:36px;width:265px;height:215px;border-radius:26px;background:linear-gradient(160deg,#2a2a2a,#111);border:1.5px solid {GOLD};transform:rotate(-8deg);display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 20px 50px rgba(0,0,0,.6)'><div style='font-size:20px;color:#ddd'>у роботі</div><div class='osw g' style='font-size:84px;font-weight:700;line-height:1'>15+</div><div style='font-size:22px;color:#ddd'>ніш</div></div>", transparent=True)
    # case avatars 320x320 (initial)
    for nm, ch in [('avaZ', 'З'), ('avaN', 'Н'), ('avaY', 'Ю'), ('avaM', 'M')]:
        render(nm, 320, 320, f"<div style='width:320px;height:320px;border-radius:50%;background:linear-gradient(135deg,{GOLD},#a8813f);display:flex;align-items:center;justify-content:center'><div class='osw' style='font-size:150px;font-weight:700;color:#000'>{ch}</div></div>", transparent=True)
    for nm, ch in [('team1', 'С'), ('team2', 'О'), ('team3', 'М')]:
        render(nm, 888, 888, f"<div style='width:888px;height:888px;border-radius:50%;background:#1a1a1a;border:10px solid {GOLD};display:flex;align-items:center;justify-content:center'><div class='osw g' style='font-size:380px;font-weight:700'>{ch}</div></div>", transparent=True)
    # profile stat cards
    def prof(name, w, h, handle, title, stats, bio):
        st = ''.join(f"<div style='text-align:center'><div class='osw' style='font-size:{int(h*.11)}px;font-weight:600'>{v}</div><div style='font-size:{int(h*.05)}px;color:#bbb'>{k}</div></div>" for k, v in stats)
        bi = ''.join(f"<div style='font-size:{int(h*.05)}px;color:#ddd;line-height:1.35'>{b}</div>" for b in bio)
        body = (f"<div style='width:{w}px;height:{h}px;background:#111;border:2px solid #2a2a2a;border-radius:{int(h*.08)}px;padding:{int(h*.09)}px {int(h*.1)}px;display:flex;flex-direction:column;justify-content:center;gap:{int(h*.06)}px'>"
                f"<div style='display:flex;align-items:center;gap:{int(h*.1)}px'><div style='width:{int(h*.3)}px;height:{int(h*.3)}px;border-radius:50%;background:linear-gradient(135deg,{GOLD},#a8813f);flex:0 0 auto;display:flex;align-items:center;justify-content:center'><span class='osw' style='font-size:{int(h*.16)}px;color:#000;font-weight:700'>{handle[0].upper()}</span></div>"
                f"<div style='display:flex;gap:{int(h*.16)}px;flex:1;justify-content:space-around'>{st}</div></div>"
                f"<div><div style='font-size:{int(h*.06)}px;font-weight:700'>{handle} <span style='color:#999;font-weight:500'>| {title}</span></div>{bi}</div></div>")
        render(name, w, h, body)
    prof('card_nina_before', 1432, 564, 'nina_demidenko_coach', 'Психолог', [('дописи', '135'), ('підписники', '1 201'), ('стежить', '1 043')], ['Психолог · транзакційний аналіз', 'Не розуміла, що постити і які продукти створювати'])
    prof('card_nina_after', 1432, 624, 'nina_demidenko_coach', 'Психолог', [('дописи', '233'), ('підписники', '6 210'), ('стежить', '1 071')], ['Тут переключаєш сценарій: з ролі жертви — у творця свого життя', 'Клієнти пишуть у Direct після роликів'])
    prof('card_julia_after', 1440, 616, 'glebova_julia', 'Кар\'єра | Гроші | Свобода', [('дописи', '51'), ('підписники', '943'), ('стежить', '63')], ['>12 років у рекрутингу · >4 000 співбесід', 'Курс «Рекрутер з 0» · набирає групу на менторство'])
    prof('card_mbody', 720, 308, 'mbodyclinic', 'Естетична медицина', [('дописи', '107'), ('підписники', '1 263'), ('стежить', '527')], ['Апаратна косметологія · Київ', 'Перші запити в Direct — через 3 тижні'])
    # format cards 1504x812
    def fmt(name, title, sub):
        render(name, 1504, 812, f"<div style='width:1504px;height:812px;border-radius:60px;background:radial-gradient(120% 100% at 20% 0%,#2a2416 0%,#0c0b09 55%,#000 100%);border:2px solid {GOLD};display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:60px'><div class='osw g' style='font-size:86px;font-weight:700;line-height:1.05'>{title}</div><div style='font-size:34px;color:#ddd;margin-top:26px;max-width:1100px'>{sub}</div></div>")
    fmt('fmt1', 'Reels без зйомки', 'Стратегія, сценарії, монтаж вашого матеріалу і публікація')
    fmt('fmt2', 'Reels під ключ зі зйомкою', 'Повний цикл: студія, оператор, монтаж, публікація — у Києві та виїзно')
    fmt('fmt3', 'Сценарії + супровід', 'Знімаєте самі — ми пишемо сценарії з хуками і ведемо за цифрами')
    # gradient bg 1680x675, bar 1210x160, card 1210x380
    render('grad', 1680, 675, f"<div style='width:100%;height:100%;background:radial-gradient(90% 120% at 50% 100%,#3a2f1c 0%,#151109 50%,#000 100%)'></div>")
    render('bar', 1210, 160, f"<div style='width:100%;height:100%;border-radius:80px;background:linear-gradient(90deg,{GOLD},#c9a465)'></div>", transparent=True)
    render('consult', 1210, 380, f"<div style='width:100%;height:100%;border-radius:40px;background:#111;border:2px solid #2a2a2a;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:40px'><div class='osw' style='font-size:44px;font-weight:600'>Записатись на безкоштовну консультацію</div><div style='font-size:22px;color:#bbb;margin-top:18px'>Розберемо вашу нішу, підберемо формат зйомки і дамо поради з підготовки</div><div style='font-size:18px;color:{GOLD};margin-top:22px'>*Напишіть нам зручним способом</div></div>")
    # reviews chat screenshots 1680x461
    bub = lambda t: f"<div style='background:#1d1d1d;border-radius:22px 22px 22px 6px;padding:22px 26px;font-size:24px;line-height:1.35;color:#eee;max-width:520px'>{t}</div>"
    render('chats', 1680, 461, "<div style='display:flex;gap:30px;padding:30px;align-items:flex-start'>"
           + f"<div style='flex:1;display:flex;flex-direction:column;gap:14px'>{bub('Оксан, це вогонь 🔥🔥 Все супер, дякую!')}{bub('А підписників було багато? — Десь близько 200')}</div>"
           + f"<div style='flex:1;display:flex;flex-direction:column;gap:14px'>{bub('Так, і воно продовжує набирати, у мене завдяки цьому +140 підписників вже))) і це тік ток з нуля тиждень тому почала вести')}</div>"
           + f"<div style='flex:1;display:flex;flex-direction:column;gap:14px'>{bub('дякую ♥ я від сьогоднішнього дня отримала більше, ніж очікувала')}{bub('На тік току відео про ерозію набрало 215 тис')}</div></div>")
    # IG profile card 800x602
    render('igprof', 800, 602, f"<div style='width:800px;height:602px;background:#000;border-radius:30px;padding:40px;display:flex;flex-direction:column;gap:26px'><div style='display:flex;align-items:center;gap:30px'><img src='file://{KVIZ}/ksyusha-v2.jpg' style='width:150px;height:150px;border-radius:50%;object-fit:cover;border:4px solid {GOLD}'><div style='display:flex;gap:40px;flex:1;justify-content:space-around;text-align:center'><div><div class='osw' style='font-size:44px'>Reels</div><div style='color:#aaa;font-size:18px'>під ключ</div></div><div><div class='osw' style='font-size:44px'>15+</div><div style='color:#aaa;font-size:18px'>ніш</div></div><div><div class='osw' style='font-size:44px'>7 000 $</div><div style='color:#aaa;font-size:18px'>з одного Reels</div></div></div></div><div><div style='font-size:24px;font-weight:700'>ksysha.bogdanets</div><div style='font-size:20px;color:#ddd;line-height:1.5;margin-top:8px'>Reels для експертів і власників бізнесу 🎬<br>Сценарії · студія · монтаж · публікація<br>📍 Київ · знімаємо і виїзно</div></div><div style='margin-top:auto;display:flex;gap:14px'><div style='flex:1;border-radius:14px;background:{GOLD};color:#000;text-align:center;padding:16px;font-weight:700;font-size:20px'>Написати</div><div style='flex:1;border-radius:14px;background:#222;text-align:center;padding:16px;font-weight:700;font-size:20px'>Стежити</div></div></div>")
    # site screenshot 1280x865
    render('siteshot', 1280, 865, f"<div style='width:100%;height:100%;background:#000;display:flex;align-items:center;justify-content:center'><img src='file:///Users/bogdanets94gmail.com/Desktop/всі проекти /створення сайтів /my-landing/cases/og-cases.jpg' style='width:1200px;border-radius:24px;border:2px solid #2a2a2a'></div>")

if __name__ == '__main__':
    what = sys.argv[1:] or ['frames', 'photos', 'icons', 'cards']
    if 'frames' in what: frames()
    if 'photos' in what: photos()
    if 'icons' in what: recolor(os.path.join(S, 'ra-img'), os.path.join(A, 'icons'))
    if 'cards' in what: cards()
