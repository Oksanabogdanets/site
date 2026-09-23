#!/usr/bin/env python3
"""Clone reels-agency.ru page -> Oksana's site: local images, gold palette, Ukrainian texts, her links."""
import os, re, shutil, sys
S = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(S, 'assets'); IMG = os.path.join(S, 'ra-img')
OUT = os.environ.get('CASES_OUT') or os.path.join(os.path.dirname(S), 'cases')
OUTIMG = os.path.join(OUT, 'img')
if os.path.isdir(OUTIMG): shutil.rmtree(OUTIMG)
os.makedirs(OUTIMG, exist_ok=True)
GOLD = '#f6d4aa'
# порядок роликів у стрічці «Приклади відео» (номери файлів video/vN.mp4).
# Додати, прибрати чи переставити відео = правити тільки цей список.
VIDEOS = [8, 4, 9, 6, 7, 10, 11, 12, 13, 14,
          16, 17, 18, 19, 20, 21, 22, 23, 24]   # 15 = міноксидил, прибрано 14.09
SITE = 'https://oksanabogdanets.github.io/site/cases/'
DIRECT = 'https://ig.me/m/ksysha.bogdanets'; TG = 'https://t.me/ksysha_bogdanets'

s = open(os.path.join(S, 'ra.html'), encoding='utf-8', errors='ignore').read()
files = sorted(os.listdir(IMG))

# ---------- image mapping: index -> replacement asset (None = keep original, 'svg' = recolor svg) ----------
# Рухома мозаїка у hero (rec1570791861) — дві колонки, що повільно їдуть.
# 12 плиток; раніше на них розкладались лише чотири фото, тому в кадрі
# постійно висіли ті самі обличчя. Тепер дев'ять: m01–m04 + нові m05–m09.
# Індекс 29 — окрема плитка в іншому блоці, не частина мозаїки.
MOSAIC = {20: 'm05.jpg', 22: 'm06.jpg', 26: 'm07.jpg', 27: 'm08.jpg',
          38: 'm09.jpg', 51: 'm01.jpg', 52: 'm02.jpg', 58: 'm03.jpg',
          72: 'm04.jpg', 74: 'm05.jpg', 76: 'm06.jpg', 82: 'm07.jpg',
          29: 'm08.jpg'}
covers_idx = [13, 15, 16, 21, 35, 42, 44, 63, 80, 92]
rep = dict(MOSAIC)
STRIP = ['k01.jpg', 'k02.jpg', 'k03.jpg', 'k04.jpg', 'k25.jpg', 'k07.jpg', 'k13.jpg', 'k11.jpg', 'k08.jpg', 'k05.jpg']
for i, idx in enumerate(covers_idx): rep[idx] = STRIP[i]
rep.update({5: 'bar.png', 6: 'consult.png', 8: 'logo540.png', 14: 'logo180.png', 36: 'wordmark.png',
            9: 'team1.png', 86: 'team2.png', 61: 'team3.png', 37: 'ava_oksana.jpg',
            18: 'chats.png', 23: 'avaZ.png', 47: 'avaZ.png', 40: 'card_mbody.png', 46: 'badge2.png',
            48: 'card_julia_after.png', 50: 'siteshot.png', 43: 'fmt1.png', 53: 'fmt2.png', 67: 'fmt3.png',
            55: 'c11.jpg', 69: 'c12.jpg', 75: 'c13.jpg', 85: 'c14.jpg', 64: 'grad.png', 65: 'card_nina_before.png',
 66: 'vcover1.jpg', 90: 'vcover2.jpg', 85: 'vcover3.jpg',
            # real screenshots from the Canva deck
            78: 'tile78.jpg', 88: 'oksana_tile.jpg', 65: 'nina_before.jpg', 91: 'nina_after.jpg', 48: 'julia_after.jpg', 40: 'mbody.jpg',
            # кейс 01 «Звільнимо»: замість зібраної вручну картки (аватарка + цифри
            # текстом) — справжні скріни профілю, як в інших кейсах
            23: 'zvilnymo_before.jpg', 47: 'zvilnymo_after.jpg',
            18: 'chats.jpg'})
# обкладинки шести готових слотів у порядку VIDEOS (див. нижче)
SLOT_IMG = [66, 90, 85, 55, 75, 69]
for _i, _idx in enumerate(SLOT_IMG):
    if _i < len(VIDEOS):
        rep[_idx] = 'vcover%d.jpg' % VIDEOS[_i]

import hashlib

def local_name(idx, f, src):
    ext = (rep[idx] if idx in rep else f).rsplit('.', 1)[-1].lower()
    h = hashlib.md5(open(src, 'rb').read()).hexdigest()[:8]
    return f'{idx:02d}-{h}.{ext}'


# PNG без прозорості важче 100 КБ (fmt1–3, grad, siteshot — по 300–450 КБ) віддаємо як JPEG:
# у 4–5 разів легше, різниці на око немає. Файли з альфою (лого, аватарки) не чіпаємо.
def _heavy_png(src):
    if not src.lower().endswith('.png') or os.path.getsize(src) < 100 * 1024:
        return False
    from PIL import Image
    im = Image.open(src)
    return not (im.mode in ('RGBA', 'LA', 'P') and 'transparency' in im.info or im.mode in ('RGBA', 'LA'))


def _png_to_jpg(idx, src):
    from PIL import Image
    import io
    buf = io.BytesIO()
    Image.open(src).convert('RGB').save(buf, 'JPEG', quality=84, optimize=True, progressive=True)
    dst = f'{idx:02d}-{hashlib.md5(buf.getvalue()).hexdigest()[:8]}.jpg'
    open(os.path.join(OUTIMG, dst), 'wb').write(buf.getvalue())
    return dst

hashmap = {}
for idx, f in enumerate(files):
    m = re.match(r'(tild[0-9a-f-]+)_', f)
    key = m.group(1) if m else f
    src = os.path.join(A, rep[idx]) if idx in rep else os.path.join(IMG, f)
    dst = local_name(idx, f, src)
    if f.lower().endswith('.svg') and idx not in rep:
        t = open(src, encoding='utf-8', errors='ignore').read()
        t = re.sub(r'#(?:cbafff|caaeff|ccafff|dfff5e)', GOLD, t, flags=re.I)
        open(os.path.join(OUTIMG, dst), 'w', encoding='utf-8').write(t)
    elif _heavy_png(src):
        dst = _png_to_jpg(idx, src)
    else:
        shutil.copy(src, os.path.join(OUTIMG, dst))
    hashmap[key] = dst
    if not m: hashmap[f] = dst

def img_sub(m):
    key = m.group(1)
    return 'img/' + hashmap[key] if key in hashmap else m.group(0)
s = re.sub(r'https?://(?:static|thb|optim)\.tildacdn\.[a-z]+/(tild[0-9a-f-]+)/[^"\'\s)]+', img_sub, s)
s = s.replace('https://static.tildacdn.com/img/tildacopy.png', 'img/' + hashmap['img_tildacopy.png'])

# ---------- colors ----------
COL = [(r'#cbafff|#caaeff|#ccafff|#dfff5e', GOLD), (r'rgb\(203,\s*175,\s*255\)|rgb\(223,\s*255,\s*94\)', 'rgb(246, 212, 170)'),
       (r'rgba\(203,175,255,1\)|rgba\(157,139,193,1\)', 'rgba(246,212,170,1)'),
       (r'#36313f|#3c374e', '#222222'), (r'rgba\(53,46,71,1\)', 'rgba(34,34,34,1)'), (r'rgba\(53,46,71,0\.95\)', 'rgba(34,34,34,0.95)'), (r'rgba\(42,36,59,1\)', 'rgba(20,20,20,1)'),
       (r'rgba\(52,37,89,0\.84\)', 'rgba(20,20,20,0.9)'), (r'#141622|#111111', '#000000'), (r'rgba\(7,8,14,1\)', 'rgba(0,0,0,1)'),
       (r'rgba\(20,22,34,0\.80\)', 'rgba(0,0,0,0.85)')]
for pat, to in COL: s = re.sub(pat, to, s, flags=re.I)

# ---------- links ----------
s = re.sub(r'https://t\.me/(?:chernovstas1|Dinabeili)', TG, s)
s = re.sub(r'https://wa\.me/79261313982[^"\']*', DIRECT, s)
s = re.sub(r'https://reels-agency\.ru/(?:agreement|politics)', '#', s)
s = s.replace('https://reels-agency.ru', SITE.rstrip('/'))
QUIZ = 'https://oksanabogdanets.github.io/site/kviz-strategy/'
# hero CTA + all 'Отримати стратегію' buttons -> strategy quiz
s = re.sub(r'href="#popup:myform"', 'href="' + QUIZ + '" target="_blank" rel="noopener"', s)
popups = set(re.findall(r'href="(#popup:[^"]+)"', s)); print('popups', popups)
for p in popups:
    if p != '#popup:infoblock': s = s.replace(f'href="{p}"', 'href="#popup:infoblock"')

# ---------- remove trackers / form / cookie / badge ----------
s = re.sub(r'<script[^>]*>(?:(?!</script>).)*?(?:dataLayer|mc\.yandex|ym\(|gtag\()(?:(?!</script>).)*?</script>', '', s, flags=re.S)
s = re.sub(r'<noscript>(?:(?!</noscript>).)*?mc\.yandex(?:(?!</noscript>).)*?</noscript>', '', s, flags=re.S)
s = re.sub(r'<form\b.*?</form>', '', s, flags=re.S)
PLAY = ['15580593611763050065983', '15580593611763704880587000002', '1558059361176346352523176810',
        '1558059361176353668710869030', '15580593611763704917239000005', '15580593611763704923446000006',
        '15580593611763704917239000007', '15580593611763704917239000008',
        '15580593611763704917239000009', '15580593611763704917239000010',

        '15580593611763704917239000011', '15580593611763704917239000012', '15580593611763704917239000013'
        '15580593611763704917239000014', '15580593611763704917239000015', '15580593611763704917239000016'
        '15580593611763704917239000017', '15580593611763704917239000018', '15580593611763704917239000019'
        '15580593611763704917239000020', '15580593611763704917239000021', '15580593611763704917239000022']
sel = ','.join('.tn-elem__%s .tn-atom' % x for x in PLAY)
play_css = (sel + '{position:relative!important;cursor:pointer}' +
            ','.join('.tn-elem__%s .tn-atom::after' % x for x in PLAY) +
            '{content:"";position:absolute;top:50%;left:50%;width:74px;height:74px;margin:-37px 0 0 -37px;border-radius:50%;'
            'background:rgba(0,0,0,.55) url("data:image/svg+xml;utf8,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 24 24\' fill=\'%23f6d4aa\'><path d=\'M8 5v14l11-7z\'/></svg>") center/32px no-repeat;'
            'border:2px solid #f6d4aa;box-shadow:0 8px 30px rgba(0,0,0,.5);pointer-events:none;z-index:5}')
HERO_TXT = '1768889182141000001'
hero_css = ('#rec1558021021 .tn-elem[data-elem-id="%s"]{top:196px!important;width:300px!important}'
            '#rec1558021021 .tn-elem[data-elem-id="%s"] .tn-atom{font-size:17px!important;line-height:1.25!important;letter-spacing:0!important}'
            '@media screen and (max-width:959px){#rec1558021021 .tn-elem[data-elem-id="%s"] .tn-atom{font-size:15px!important}}'
            '@media screen and (max-width:479px){#rec1558021021 .tn-elem[data-elem-id="%s"]{top:186px!important;width:250px!important}'
            '#rec1558021021 .tn-elem[data-elem-id="%s"] .tn-atom{font-size:13.5px!important}}') % ((HERO_TXT,)*5)
BADGE = '1763109677657'
badge_css = ('#rec1558021021 .tn-elem[data-elem-id="%s"]{left:calc(50%% - 640px + 515px)!important;top:170px!important}'
             '@media screen and (max-width:1279px){#rec1558021021 .tn-elem[data-elem-id="%s"]{left:calc(50%% - 480px + 395px)!important;top:170px!important}}'
             '@media screen and (max-width:959px){#rec1558021021 .tn-elem[data-elem-id="%s"]{left:calc(50%% - 320px + 250px)!important;top:150px!important;transform:scale(.85);transform-origin:top left}}'
             # на телефоні бейдж стояв на кнопці «Отримати стратегію» — тепер у вільній зоні
             # праворуч від підзаголовка, над кнопкою (перевірено на 360/375/390/414/540)
             '@media screen and (max-width:639px){#rec1558021021 .tn-elem[data-elem-id="%s"]{display:table!important;left:calc(50%% - 240px + 330px)!important;top:190px!important;transform:scale(.72);transform-origin:top left}}'
             '@media screen and (max-width:479px){#rec1558021021 .tn-elem[data-elem-id="%s"]{left:calc(50%% - 180px + 252px)!important;top:170px!important;transform:scale(.66);transform-origin:top left}}') % ((BADGE,)*5)
CAPS = ['1763047549777', '1763047549803', '1763047549839', '176312696555815890']
caps_css = ''.join('#rec1556224301 .tn-elem[data-elem-id="%s"] .tn-atom,#rec1571158361 .tn-elem[data-elem-id="%s"] .tn-atom'
                   '{font-size:11.5px!important;line-height:1.3!important;letter-spacing:.02em!important}' % (c, c) for c in CAPS)
# перша картка: трохи більший кегль, щоб підпис ліг у два рядки і не налазив на іконку
caps_css += ('#rec1556224301 .tn-elem[data-elem-id="1763047549777"] .tn-atom,#rec1571158361 .tn-elem[data-elem-id="1763047549777"] .tn-atom'
             '{font-size:12.5px!important;line-height:1.3!important}'
             '@media screen and (min-width:960px){#rec1556224301 .tn-elem[data-elem-id="1763047549777"],#rec1571158361 .tn-elem[data-elem-id="1763047549777"]{top:514px!important}}')
# фото чужої клієнтки в сітці болей (низ праворуч) — Оксана попросила прибрати
hide_css = ('#rec1556224301 .tn-elem[data-elem-id="1763394719628"],'
            '#rec1571158361 .tn-elem[data-elem-id="176340044197483570"]{display:none!important}')
# ---------- мобільні накладання (зі скрінів 16.09) ----------
MOBILE_FIX = (
    '@media screen and (max-width:479px){'
    # «Для кого»: заголовок першої картки був шириною 400px при картці 345 — вилазив за краї
    # (заголовок лежить у flex-колонці шириною ~298px, а сам був 400px зі зсувом left:-51px —
    #  тому просто підганяємо його під ширину колонки)
    '#rec1571158361 .tn-elem[data-elem-id="1763047549768"]{width:100%!important;left:0!important}'
    '#rec1571158361 .tn-elem[data-elem-id="1763047549768"] .tn-atom{font-size:14px!important;line-height:1.15!important}'
    # «8 год вашого часу» (70px, три рядки) лягало на підзаголовок «Від стратегічної сесії…»
    '#rec1575165041 .tn-elem[data-elem-id="1763049679183"] .tn-atom{font-size:46px!important;line-height:.95!important}'
    '}'
)
import packages, niches, team, blocks, form, services
# старий Tilda-блок форматів роботи (дві копії) міняємо на власний — там не було місця
# під четвертий пакет, а пункт «Підбір локації…» дублювався
hide_css += '#rec1558101811,#rec1575209271{display:none!important}'
# блок «Команда» Tilda (4 картки) → власний на 5 людей (team.py)
hide_css += '#rec1558093791{display:none!important}'
# кейс 01: скріни на місце аватарок (пропорції збігаються зі слотами інших кейсів),
# а текстові цифри й опис профілю ховаємо — вони дублюють те, що видно на скріні
ZV_SHOTS = [('1763049596474', 141), ('1763049596500', 395)]   # «після» вище: + TikTok-стрічка (cases_tall.TT_H)
ZV_HIDE = ['1763049596486', '1763049596490', '1763049596481', '1763049596488',
           '1763049596492', '1763049596483', '1763049596475', '1763049596510',
           '1763049596514', '1763049596524', '1763049596512', '1763049596526',
           '1763049596516', '1763049596502', '1763049596507']
case_css = ''.join('#rec1558030471 .tn-elem[data-elem-id="%s"]{width:358px!important;'
                   'height:%dpx!important}'
                   '#rec1558030471 .tn-elem[data-elem-id="%s"] .tn-atom{border-radius:14px!important;'
                   'background-size:cover!important;background-position:center top!important}'
                   % (e, h, e) for e, h in ZV_SHOTS)
case_css += ','.join('#rec1558030471 .tn-elem[data-elem-id="%s"]' % e for e in ZV_HIDE)
case_css += '{display:none!important}'
play_css += hero_css + badge_css + caps_css + hide_css + MOBILE_FIX + packages.CSS + niches.CSS + team.CSS + blocks.CSS + form.CSS + services.CSS + case_css
s = s.replace('</head>', '<style>#rec1698062081,#rec1590641921,#rec1998611892,.t-tildalabel,.t887{display:none!important}' + play_css + '</style>\n</head>')

# ---------- meta ----------
s = re.sub(r'<title>.*?</title>', '<title>Reels-просування для експертів і бізнесу · Оксана Богданець</title>', s, flags=re.S)
s = re.sub(r'(<meta name="description" content=")[^"]*', r'\1Reels під ключ: від сценарію до зйомки в студії, монтажу й публікації. Кейси з результатами до/після.', s)
s = re.sub(r'(<meta name="keywords" content=")[^"]*', r'\1reels, рілс, reels під ключ, рілсмейкер київ, зйомка reels, продакшн reels', s)
s = re.sub(r'(<meta property="og:title" content=")[^"]*', r'\1Reels-просування для експертів і бізнесу', s)
s = re.sub(r'(<meta property="og:description" content=")[^"]*', r'\1Повний супровід: сценарій, студія, монтаж, публікація. 7 000 $ з одного Reels.', s)
s = re.sub(r'(<meta property="og:image" content=")[^"]*', r'\1' + SITE + 'og-cases.jpg', s)
s = re.sub(r'(<meta property="og:url" content=")[^"]*', r'\1' + SITE, s)
s = re.sub(r'(<link rel="canonical" href=")[^"]*', r'\1' + SITE, s)
s = s.replace('lang="ru"', 'lang="uk"')

# ---------- прелоадер: привітання замість «Загрузка», без штучної паузи ----------
# Було: «Загрузка» по літерах (80 мс/символ) + пауза 2 с + повільний fadeOut ≈ 3 с чорного екрана.
# Стало: коротке привітання швидко (28 мс/символ), fadeOut одразу після набору.
PRE_TXT = 'Вітаю! Зараз покажу, як Reels приводять клієнтів'
for _a, _b in [
    ('var text = "Загрузка"; var speed = 80;', 'var text = "%s"; var speed = 28;' % PRE_TXT),
    ('"preloaderText":"Загрузка","typeSpeed":"80","fadeOutShort":"2000"', '"preloaderText":"%s","typeSpeed":"28","fadeOutShort":"250"' % PRE_TXT),
    ("if (contentLoaded) { setTimeout(function() { $('#preloader').fadeOut('slow'); }, 2000); } else { setTimeout(function() { $('#preloader').fadeOut('slow'); }, ); }",
     "setTimeout(function() { $('#preloader').fadeOut(400); }, 250);"),
    ('#preloader-quote { margin-top: 40px; width: 90%; text-align: center; font-size: 80px; color: #382F4C;',
     '#preloader-quote { margin-top: 0; width: 90%; text-align: center; font-size: 44px; line-height: 1.25; color: #f6d4aa;'),
    ('linear-gradient(90deg, #f6d4aa, #382F4C, #f6d4aa)', 'linear-gradient(90deg, #f6d4aa, #8a744f, #f6d4aa)'),
    ('@media all and (max-width: 480px) { #preloader-quote { font-size: 16px; } }',
     '@media all and (max-width: 480px) { #preloader-quote { font-size: 24px; } }'),
]:
    assert _a in s, 'прелоадер: не знайдено ' + _a[:50]
    s = s.replace(_a, _b)
print('прелоадер:', PRE_TXT in s)
# 23.09, Оксана: «не потрібно слово Загрузка взагалі, хай починається одразу з Reels-просування» —
# прибираємо блок прелоадера цілком (rec1597478921: чорний оверлей + скрипт набору тексту)
_pa = s.find('<div id="rec1597478921"'); _pb = s.find('<div id="rec', _pa + 10)
assert _pa > 0 and _pb > _pa, 'прелоадер: rec1597478921 не знайдено'
s = s[:_pa] + s[_pb:]
print('прелоадер прибрано:', s.count('rec1597478921') == 0 and s.count('id="preloader"') == 0)

# ---------- відео: не тягнути всі ролики при відкритті ----------
# Tilda ставить preload=metadata кожному з 19 <video> — телефон качає мегабайти ще до
# першого скролу. Тепер preload=none, а замість першого кадру — обкладинка video/vN-cover.jpg.
_n = s.count('preload=${(false && isMobile) || false ? "none" : "metadata"}')
s = s.replace('${\'\' ? "poster=\'\'" : ""}', 'poster="${link.replace(/\\.mp4.*$/, \'-cover.jpg\')}"')
s = s.replace('preload=${(false && isMobile) || false ? "none" : "metadata"}', 'preload="none"')
print('відео preload=none:', _n, '| poster:', s.count("'-cover.jpg')"))

# ---------- texts ----------
T = [
 ('Reels продвижение для экспертов и бизнесов', 'Reels-просування для експертів та бізнесу'),
 ('Рилс продвижение', 'Reels-просування'), ('для экспертов и бизнесов', 'для експертів та бізнесу'),
 ('Полноценное сопровождение от написания сценария до съемки и монтажа', 'Повний супровід: від сценарію до зйомки в студії, монтажу і публікації'),
 ('Получите индивидуальную стратегия продвижения через reels',
  'Отримайте індивідуальну стратегію, яка побудує ваш особистий бренд та збільшить потік клієнтів'),
 ('Получить индивидуальную стратегию', 'Отримати індивідуальну стратегію'), ('Получить стратегию', 'Отримати стратегію'),
 ('О НАС', 'ПРО НАС'), ('КЕЙСЫ', 'КЕЙСИ'), ('УСЛУГИ', 'ПОСЛУГИ'), ('КОНТАКТЫ', 'КОНТАКТИ'),
 ('О нас', 'Про нас'), ('Кейсы', 'Кейси'), ('Услуги', 'Послуги'), ('Контакты', 'Контакти'),
 ('*Записаться на бесплатную консультацию', '*Записатись на безкоштовну консультацію'),
 ('свяжитесь с нами удобным способом', 'напишіть нам зручним способом'),
 ('СТРОИМ СТРАТЕГИЮ ПРОДВИЖЕНИЯ ПОД ВАШУ НИШУ', 'БУДУЄМО СТРАТЕГІЮ ПРОСУВАННЯ ПІД ВАШУ НІШУ'),
 ('Вам нужен рилсмейкер, если', 'Вам потрібен Reels Producer, якщо'),
 ('Нет системы создания контента?', 'Не розумієте, якою має бути система створення контенту'),
 ('Снимаете, как получится, без чёткого плана?', 'Знімаєте навмання, без чіткого плану, і не маєте жодних результатів'),
 ('ПУБЛИКУЕМ РОЛИКИ ЕЖЕДНЕВНО, ЧТО ГЕНЕРИРУЕТ СТАБИЛЬНЫЙ ТРАФИК И ЗАЯВКИ', 'СТВОРЮЄМО РОЛИКИ ЛИШЕ ПІСЛЯ АНАЛІЗУ КОНКУРЕНТІВ, ЦА І РИНКУ — І ВЖЕ ТОДІ ФОРМУЄМО ФОРМАТИ ТА ТЕМИ'),
 ('Не знаете с чего начать?', 'Хочете мати особистий бренд в Instagram, але не знаєте, з чого почати'),
 ('Конкуренты успешно продвигаются в рилс, чувствуете , что отстаёте?', 'Конкуренти вже просуваються через Reels, і ви відчуваєте, що відстаєте'),
 ('Нет времени на рилс?', 'Немає часу на Reels'),
 ('Хочется заниматься бизнесом, а не быть сам себе рилсмейкером?', 'Хочете повністю делегувати сценарії, зйомку і монтаж, а не бути самому собі рілсмейкером'),
 ('БЕРЁМ ВСЮ РАБОТУ ПО КОНТЕНТУ НА СЕБЯ', 'БЕРЕМО ВСЮ РОБОТУ ПІД КЛЮЧ НА СЕБЕ'),
 ('Рилс набирают мало просмотров?', 'Робите Reels, але вони не дають жодних результатів'),
 ('Тратите время и силы, а результата нет?', 'Витрачаєте час і сили, а заявок з Instagram немає'),
 ('СОЗДАЁМ REELS КОТОРЫЕ ГЕНЕРИРУЮТ ПОДПИСЧИКОВ И КЛИЕНТОВ', 'СТВОРЮЄМО REELS, ЯКІ МАЮТЬ ЦІЛЬ — ПРИВОДЯТЬ ПІДПИСНИКІВ ТА КЛІЄНТІВ'),
 ('Создаём ролики по уникальной стратегии на основе работы с', 'Знімаємо ролики за стратегією під нішу — на основі досвіду з'),
 ('150+ проектами', '20+ нішами'), ('ОПЫТ РАБОТЫ В НИШАХ', 'НІШ У РОБОТІ'),
 ('ГОРОДОВ И СТРАН. РАБОТАЕМ ПО ВСЕЙ РОССИИ И ЗАРУБЕЖОМ', 'РОКИ НА РИНКУ REELS PRODUCTION ТА ІНФОБІЗНЕСУ'),
 ('РОЛИКОВ МИЛЛИОННИКОВ', 'РОЛИКИ-МІЛЬЙОННИКИ'),
 ('Наши работы', 'Наші роботи'), ('набирают миллионы', 'набирають мільйони'), ('и делают вас лидером', 'і роблять вас лідером'),
 ('КЕЙС 01', 'КЕЙС 01'), ('НЕДВИЖИМОСТЬ', 'ЮРИДИЧНА КОМПАНІЯ'), ('+10 000 ПОДПИСЧИКОВ', '7 000 $ З ОДНОГО REELS'),
 ('Оксана Никитюк | Недвижимость Краснодар', 'Звільнимо | Банкрутство фізосіб'),
 ('подписки', 'стежить'), ('подписчики', 'підписники'), ('публикации', 'вподобання'),
 ('💎 Ипотека не есть кабала', '⚖️ Банкрутство фізичних осіб — законно'),
 ('💎 Сделала +100 человек с 0 в кармане МИЛЛИОНЕРАМИ', '⚖️ Безкоштовна консультація'), ('через недвижимость', 'за посиланням'),
 ('6 113', '23'), ('349', '112'), ('16,9 тыс.', '225,7 тис.'), ('492', '1,2 млн'),
 ('РЕЗУЛЬТАТ 10+ ТЫС. ПОДПИСЧИКОВ', 'РЕЗУЛЬТАТ: 7 000 $ З ОДНОГО REELS'),
 ('1,5 месяца', 'перші місяці'), ('работы. Самый популярный ролик набрал', 'роботи. Найпопулярніший ролик набрав'),
 ('4,1 млн.', '2,4 млн'), ('просмотров', 'переглядів'),
 ('ДЕТСКАЯ ПСИХОЛОГИЯ', 'ПСИХОЛОГ'), ('+50 000 ПОДПИСЧИКОВ', '+4 000 ПІДПИСНИКІВ'),
 ('РЕЗУЛЬТАТ С 0 ДО 50 ТЫС. ПОДПИСЧИКОВ', 'РЕЗУЛЬТАТ: З 1 201 ДО 6 210 ПІДПИСНИКІВ'),
 ('5 месяцев.', 'перший місяць в Instagram і TikTok.'), ('Самый популярный ролик набрал', 'Найпопулярніший ролик набрав'), ('6,3 млн.', '382 тис.'),
 ('АГЕНТСТВО ПО ИПОТЕКЕ', 'КАР\'ЄРНИЙ КОНСУЛЬТАНТ'), ('20+ ЗАЯВОК В ДЕНЬ', '+700 ЦІЛЬОВИХ ПІДПИСНИКІВ'),
 ('РЕЗУЛЬТАТ 20+ ЛИДОВ В ДЕНЬ С REELS', 'РЕЗУЛЬТАТ: +700 ЦІЛЬОВИХ З 10 REELS'),
 ('Количество просмотров роликов увеличилось', 'Набирає групу на менторство. Аудиторія зросла'), ('в 5 раз', 'у 7 разів'),
 ('ПОСЛЕ', 'ПІСЛЯ'),
 ('ЖЕНСКИЙ ПСИХОЛОГ', 'КЛІНІКА ЕСТЕТИЧНОЇ МЕДИЦИНИ'), ('10 МЛН. ОХВАТ', 'ЗАЯВКИ ЗА 3 ТИЖНІ'),
 ('РЕЗУЛЬТАТ СДЕЛАЛИ ОХВАТ В 10 МЛН.', 'РЕЗУЛЬТАТ: ПЕРШІ ЗАПИТИ ЧЕРЕЗ 3 ТИЖНІ'),
 ('Через прогрев в Reels увеличили запуск курса в 2 раза', '100% органічний трафік — без жодного долара на таргет'),
 ('Проводим стратегическую сессию, где презентуем стратегию продвижения и задаем вопросы для дальнейшего написания сценариев.', 'Бриф і стратегічна сесія в Zoom, договір і оплата. Аналізуємо конкурентів, ринок і продукт, формуємо УТП.'),
 ('Готовая стратегия продвижения — с прописанными рубриками, частотой публикаций', 'Команда має все, щоб за 2 тижні зібрати стратегію'),
 ('и форматами контента.', 'і форматами контенту.'), ('1 час', '1 год'), ('4 часа', '1 год'),
 ('Утверждаем сценарии', 'Створення стратегії'),
 ('Создаем 30 качественных сценариев с воронками продаж и описаниями.', 'Підбираємо теми й референси, пишемо сценарії, коригуємо і репетируємо їх у Zoom, затверджуємо.'),
 ('Готовый сценарий – документ, по которому можно быстро снимать и не терять фокус на цели.', 'Затверджені сценарії з хуками, воронками й описами.'),
 ('Снимаем 30 видео за день', 'Погодження стилю зйомки'),
 ('Организовываем съёмку с оператором, проф. камерой, светом и звуком. Не надо думать над ракурсом и форматом для съёмки, мы все это берём на себя.', 'Погоджуємо образ, локації, акторів і реквізит, фіксуємо дату зйомки — усе в Telegram.'),
 ('Готовый материал на месяц вперёд – видео высокого качества, готовые к монтажу.', 'Зафіксовані дата, образ, локація і реквізит — на майданчику нічого не вирішуємо.'),
 ('Утверждаем монтаж и выкладываем', 'Організація і зйомка'),
 ('Монтируем ролики в заранее утвержденном дизайне. Добавляем субтитры, фото, видео и музыку.', 'Відпрацьовуємо жестикуляцію і подачу, знімаємо за один день, монтуємо.'),
 ('Каждый день выкладывается Reels в 3 социальные сети. Стабильный поток контента –растущий аккаунт.', 'Готові змонтовані ролики. Від стратегічної сесії до цього моменту — місяць.'),
 ('Стратегическая сессия', 'Підготовка'), ('Что делаем:', 'Що робимо:'),
 ('столько понадобится вашего времени, для создания контента на месяц', 'Від стратегічної сесії до готових відео — місяць. Від вас потрібно лише це:'),
 ('7 часов', '8 год'), ('в месяц', 'вашого часу'), ('Этапы работы', 'Етапи роботи'), ('Обсудить проект', 'Обговорити проєкт'),
 ('Примеры видео', 'Приклади відео'), ('снятых и смонтированных нами', 'знятих і змонтованих нами'),
 ('Отзывы', 'Відгуки'), ('Нам доверяют — и возвращаются', 'Нам довіряють — і повертаються'),
 ('Команда с опытом работы в', 'Команда з досвідом роботи в'), ('50+ нишах', '20+ нішах'),
 ('Станислав', 'Оксана'), ('Основатель агенства', 'Засновниця, продюсерка'), ('Миэль', 'Сценаристка'), ('Сценарист', 'Сценарії та хуки'),
 ('Андрей', 'Оператор'), ('Видеооператор', 'Зйомка в студії'), ('Вероника', 'Монтажерка'), ('Монтажер', 'Монтаж і субтитри'),
 ('Пришла пора выбирать', 'Прийшов час обирати'), ('Форматы взаимодействия', 'Формати співпраці'),
 ('Создание индивидуальной стратегии продвижения', 'Індивідуальна стратегія просування'),
 ('Написание 30 качественных сценариев с воронками и описанием', 'Сценарії з хуками, воронками й описами'),
 ('Монтаж роликов с ИИ аватаром', 'Розбір статистики і супровід'), ('Монтаж роликов', 'Монтаж роликів'),
 ('Публикация роликов с описанием, хештегами и обложкой', 'Публікація з описом, хештегами й обкладинкою'),
 ('Подбор локации, организация и курирование съемки', 'Підбір локації, організація і курування зйомки'),
 ('Съемка с оператором с проф. камерой, светом и звуком', 'Зйомка з оператором: профкамера, світло, звук'),
 ('Проведение съемки для создания вашего ИИ аватара', 'Щотижневі рекомендації за цифрами'),
 ('То, что вы точно хотели спросить', 'Те, що ви точно хотіли спитати'), ('Какие этапы работы ?', 'Які етапи роботи?'),
 ('В начале мы проводим стратегическую сессию, обсуждаем форматы и идеи, затем расписываем и утверждаем сценарии, после этого проводим съемку и монтируем ролики', 'Спочатку стратегічна сесія: обговорюємо формати та ідеї, далі розписуємо і погоджуємо сценарії, потім знімальний день у студії, монтаж і публікація'),
 ('Сколько дней занимает создание рилс?', 'Скільки часу до перших роликів?'),
 ('От начала работы до первых роликов, которые начинают публиковаться в вашем аккаунте проходит 12-14 дней', 'Від старту до перших роликів, які виходять у вашому акаунті, минає 10–14 днів'),
 ('В КАКИХ ГОРОДАХ ВЫ РАБОТАЕТЕ ?', 'А ЯКЩО Я НЕ В КИЄВІ?'),
 ('Мы проводим съемки в любом городе.', 'Студія в Києві, але знімаємо і виїзно.'),
 ('У нас клиенты из Москвы, Питера, Екб, Дубай, Бали и тд. Оставьте заявку, чтобы мы обсудили варианты сотрудничества в зависимости от вашего места', 'Сценарії, монтаж і публікація — повністю дистанційно. Напишіть, і обговоримо варіант під ваше місто'),
 ('А У ВАС ЕСТЬ СТУДИЯ ДЛЯ СЪеМки ?', 'Я НЕ ВМІЮ ГОВОРИТИ НА КАМЕРУ'),
 ('Мы не привязываемся к одной конкретной студии.', 'Більшість клієнтів приходять саме такими.'),
 ('Съемки организуются в локациях исходя из стратегии продвижения и пожеланий клиента', 'У кадрі є підказки, сценарій написаний вашими словами, а на майданчику допомагаємо триматись природно'),
 ('Давайте обсудим ваш проект!', 'Обговоримо проєкт!'), ('Запишитесь', 'Запишіться'), ('на бесплатную консультацию', 'на безкоштовну консультацію'),
 ('Выявим ваши потребности и подберем подходящий формат съемки, а также дадим ценные советы по подготовке', 'Розберемо вашу нішу, підберемо формат зйомки і дамо поради з підготовки — 20 хвилин у Zoom'),
 ('*Свяжитесь с нами удобным способом', '*Напишіть нам зручним способом'), ('Навигация', 'Навігація'),
 ('ИП Чернов Станислав Андреевич', 'ФОП Богданець Оксана'), ('ИНН: 771618689808', 'Київ, Україна'), ('Разработка сайта', ''), ('Главная', 'Головна'),
 ('©2026 Все права защищены', '©2026 Усі права захищені'), ('Политика конфиденциальности', 'Політика конфіденційності'),
 ('Согласие на обработку персональных данных', 'Згода на обробку персональних даних'),
 ('Whats’App', 'Instagram Direct'), ('Закрыть диалоговое окно', 'Закрити'), ('Закрыть уведомление', 'Закрити'), ('Соц. сети', 'Соцмережі'),
 ('Ошибки при заполнении формы', 'Помилка'),
 ('Продолжая использовать сайт, вы соглашаетесь с нашей Политикой использования файлов cookie', ''),
]
T.sort(key=lambda p: -len(p[0]))
for ru, uk in T:
    pat = re.escape(ru).replace(r'\ ', r'(?:\s|&nbsp;)+')
    if len(ru) <= 12:
        pat = r'(?<=>)(\s*)' + pat + r'(\s*)(?=<)'
        s, n = re.subn(pat, lambda m, uk=uk: m.group(1) + uk + m.group(2), s)
    else:
        s, n = re.subn(pat, lambda m, uk=uk: uk, s)
    if n == 0: print('MISS', ru[:50])
# stats numbers inside the 'about' zero block only
for a, b in [('20', '4'), ('100', '3'), ('50', '20')]:
    s, n = re.subn(r'(?<=>)(\s*)' + a + r'(\s*)(?=<)', lambda m, b=b: m.group(1) + b + m.group(2), s); print('num', a, n)
# inline SVG logos -> wordmark image
def svg_sub(m):
    x = m.group(0)
    return '<img src="img/wordmark2.png" alt="Oksana Bogdanets" style="width:100%;height:100%;object-fit:contain;display:block">' if len(x) > 3000 else x
s = re.sub(r'<svg[^>]*>(?:(?!</svg>).)*</svg>', svg_sub, s, flags=re.S)
s = re.sub(r'просмотров', 'переглядів', s)
cnt = [0]
def _foll(m):
    cnt[0] += 1
    return m.group(1) + ('12' if cnt[0] == 1 else '30') + m.group(2)
s = re.sub(r'(?<=>)(\s*)250(\s*)(?=<)', _foll, s); print('follow numbers replaced:', cnt[0])
# generic alt / aria-label with Cyrillic
s = re.sub(r'(alt|aria-label)="[^"]*[А-Яа-яЁё][^"]*"', r'\1="Reels під ключ · Оксана Богданець"', s)
s = re.sub(r"(alt|aria-label)='[^']*[А-Яа-яЁё][^']*'", r"\1='Reels під ключ · Оксана Богданець'", s)

# ---------- стрічка «Приклади відео» ----------
# VIDEOS — порядок роликів на сайті; додати/прибрати відео = правити тільки цей список.
# Перші шість лягають у готові слоти Tilda, решта — нові картки праворуч (extra_cards).
SLOT_KIN = ['5GaP11iJpdMpX7eaYNktdY', 'ojJWzhRC5cmzvXCjbAFwei', 'pZHMq8PdFoBGTW3pQQvVnQ',
            '91dQhEijdECsXMoRUzM6vb', 'g42ABRdgwynimcKG4hn1uv', 'rnTFCDEHF4FYboWydfXVi3']
for i, kin in enumerate(SLOT_KIN):
    url = SITE + 'video/v%d.mp4' % VIDEOS[i] if i < len(VIDEOS) else ''
    s = s.replace('https://kinescope.io/' + kin, url)
print('kinescope left:', s.count('kinescope.io/'))
# counter animation script (custom Tilda snippet): 50/100/20 -> 15/4/10
s = s.replace('let numberfinish = ["50","100","20"];', 'let numberfinish = ["20","3","4"];')
s = s.replace('"endDigit":"50"', '"endDigit":"20"').replace('"endDigit":"100"', '"endDigit":"3"').replace('"endDigit":"20"', '"endDigit":"4"')
print('counter fixed:', 'numberfinish = ["20","3","4"]' in s)
# drop the '+' atom that follows the middle counter (4 ролики-мільйонники — точна цифра)
i = s.find('myClass02'); j = s.find(">+</div>", i)
if 0 < j < i + 6000: s = s[:j] + "></div>" + s[j + len(">+</div>"):]; print('plus dropped')
wm = 'wordmark2-' + hashlib.md5(open(os.path.join(A, 'wordmark2.png'),'rb').read()).hexdigest()[:8] + '.png'
shutil.copy(os.path.join(A, 'wordmark2.png'), os.path.join(OUTIMG, wm))
s = s.replace('img/wordmark2.png', 'img/' + wm)
# ---------- нові картки в стрічці «Приклади відео» (7, 8) ----------
import extra_cards
EXTRA = []
for _i, _v in enumerate(VIDEOS[len(SLOT_KIN):], start=len(SLOT_KIN) + 1):
    cov = 'vcover%d.jpg' % _v
    h = hashlib.md5(open(os.path.join(A, cov), 'rb').read()).hexdigest()[:8]
    name = 'vcover%d-%s.jpg' % (_v, h)
    shutil.copy(os.path.join(A, cov), os.path.join(OUTIMG, name))
    EXTRA.append((_i, SITE + 'video/v%d.mp4' % _v, 'img/' + name))   # _i — номер слоту в ряду
s, _play = extra_cards.add(s, EXTRA, SITE + 'video/v%d.mp4' % VIDEOS[4])
print('додано карток:', len(EXTRA), '| відео у стрічці:', s.count('/video/v'))

# хвіст результату картки «Бриф» (у джерелі розбитий <br> і &nbsp;)
for _t in ('и&nbsp;форматами контента.', 'і&nbsp;форматами контенту.', 'і форматами контенту.'):
    s = s.replace(_t, 'і написати сценарії.')
s = s.replace("tn_text_176314310323332090'>1 год<", "tn_text_176314310323332090'>2 год<")
s = s.replace("tn_text_176314294694146400'>1 год<", "tn_text_176314294694146400'>Telegram<")
# ---------- FAQ: відповіді словами Оксани (13.09) ----------
FAQ = [
 ('Спочатку стратегічна сесія: обговорюємо формати та ідеї, далі розписуємо і погоджуємо сценарії, потім знімальний день у студії, монтаж і публікація',
  'Чотири етапи: підготовка (бриф, стратегічна сесія, аналіз ринку), створення стратегії і сценаріїв, погодження стилю зйомки, зйомка з монтажем. <br>Команда працює 2 тижні до готових сценаріїв, і весь шлях — під керівництвом Оксани'),
 ('Від старту до перших роликів, які виходять у вашому акаунті, минає 10–14 днів',
  'Місяць — від стратегічної сесії до готових відео. <br>Перші два тижні команда готує стратегію і сценарії, далі зйомка і монтаж'),
 ('Студія в Києві, але знімаємо і виїзно. <br>Сценарії, монтаж і публікація — повністю дистанційно. Напишіть, і обговоримо варіант під ваше місто',
  'Наша команда працює по всій Україні — хороші оператори є в кожному місті. <br>А головне — стратегію і сценарії повністю курує Оксана, і це не залежить від міста'),
 ('Більшість клієнтів приходять саме такими. <br>У кадрі є підказки, сценарій написаний вашими словами, а на майданчику допомагаємо триматись природно',
  'Майже всі клієнти, яких ви бачите на цій сторінці, починали з нами — це була їхня перша зйомка. <br>Перед зйомкою ми проводимо достатньо часу, щоб у кадрі ви почувалися впевнено'),
 ('А ЯКЩО Я НЕ В КИЄВІ?', 'А якщо я не в Києві?'),
 ('Я НЕ ВМІЮ ГОВОРИТИ НА КАМЕРУ', 'Що, якщо я не вмію говорити на камеру?'),
]
for _a, _b in FAQ:
    assert _a in s, 'FAQ не знайдено: ' + _a[:40]
    s = s.replace(_a, _b)
print('FAQ замінено:', len(FAQ))
# картка «Зйомка» у блоці годин: 5 год (обидві копії блоку мають той самий id)
s = s.replace("tn_text_176314294699174820'>1 год<", "tn_text_176314294699174820'>5 год<")
print('5 год у картці Зйомка:', s.count("tn_text_176314294699174820'>5 год<"))
s = s.replace('<div id="rec1558101811"', packages.html(DIRECT) + '<div id="rec1558101811"', 1)
# перед заголовком пакетів (rec1564228961 + його css-блок rec1578894761): що вміємо → як ведемо → старт
s = s.replace('<div id="rec1578894761"', services.skills() + services.process() + services.start() + '<div id="rec1578894761"', 1)
s = s.replace('<div id="rec1577011231"', niches.html() + '<div id="rec1577011231"', 1)
def _asset_url(fn):
    h = hashlib.md5(open(os.path.join(A, fn), 'rb').read()).hexdigest()[:8]
    name = os.path.splitext(fn)[0] + '-' + h + os.path.splitext(fn)[1]
    shutil.copy(os.path.join(A, fn), os.path.join(OUTIMG, name)); return 'img/' + name
s = s.replace('<div id="rec1558093791"', team.html(_asset_url) + blocks.about(_asset_url('ava_oksana.jpg')) + '<div id="rec1558093791"', 1)
# «Наша місія» — після ВСЬОГО першого екрана (hero = текст + рухома мозаїка), перед «Для кого»
s = s.replace('<div id="rec1556224301"', blocks.mission() + '<div id="rec1556224301"', 1)
# результати — перед заголовком «Приклади відео»
s = s.replace('<div id="rec1558049271"', blocks.results() + '<div id="rec1558049271"', 1)
# форма — перед фінальним CTA з кнопками Telegram/Direct
s = s.replace('<div id="rec1580410031"', form.html() + '<div id="rec1580410031"', 1)
# кейси 03 і 04 — високі картки з «до/після», клони колонки кейса 02
import cases_tall
s = cases_tall.apply(s, _asset_url)
print('кейси 03/04: клонів', s.count("data-elem-id='8763049596"), s.count("data-elem-id='9763049596"),
      '| старих елементів:', s.count("data-elem-id='1763049596573'") + s.count("data-elem-id='176345641403933930'"))
print('нові блоки:', s.count('id="oks-mission"'), s.count('id="oks-res"'), s.count('id="oks-about"'), s.count('id="oks-form"'))
print('команда:', s.count('class="tm-card"'), 'карток')
print('рядок ніш:', s.count('id="oks-niches"'))
print('блок пакетів:', s.count('id="oks-pk"'), '| карток:', s.count('class="pk-card'))
print('послуги/етапи/старт:', s.count('id="oks-skills"'), s.count('id="oks-process"'), s.count('id="oks-start"'))

open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(s)
left = re.findall(r'[^<>"]{0,40}[ыЫэЭъЪёЁ][^<>"]{0,40}', re.sub(r'<script.*?</script>|<style.*?</style>', '', s, flags=re.S))
print('written', len(s), 'bytes; russian leftovers:', len(left)); print('\n'.join(sorted(set(left))[:40]))
