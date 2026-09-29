#!/usr/bin/env python3
"""Сайт кейсів БЕЗ Tilda (29.09.2026, Оксана: «перезібрати, щоб був швидкий і працював незалежно»).

Той самий дизайн і ті самі тексти, що й у старій версії (build.py збирав її з клону Tilda-сторінки),
але чистий HTML/CSS і трохи JS — без jQuery, без 20+ файлів з static.tildacdn.com.

Запуск:  cd cases-src && python3 site2.py            → ../cases/new.html  (тестова адреса)
         cd cases-src && python3 site2.py --live     → ../cases/index.html (основна адреса)
Картинки → ../cases/v2/ (WebP, імена з хешем, щоб браузер не тримав старі).
Відео лишаються в ../cases/video/ (vN.mp4 + vN-cover.webp).

Тексти й порядок блоків — у цьому файлі (секції нижче) і в модулях, які вже були без Tilda:
blocks.py (місія, «Що ви отримуєте», «Хто веде проєкт»), niches.py, team.py, packages.py, faq.py, form.py.
"""
import hashlib, io, os, re, sys
from PIL import Image

S = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(S, 'assets')
RA = os.path.join(S, 'ra-img')
OUT = os.path.join(os.path.dirname(S), 'cases')
IMGDIR = os.path.join(OUT, 'v2')
LIVE = '--live' in sys.argv
PAGE = 'index.html' if LIVE else 'new.html'

GOLD = '#f6d4aa'
SITE = 'https://oksanabogdanets.github.io/site/cases/'
DIRECT = 'https://ig.me/m/ksysha.bogdanets'
TG = 'https://t.me/ksysha_bogdanets'
KVIZ = 'https://oksanabogdanets.github.io/site/kviz-strategy/'

sys.path.insert(0, S)
import blocks, niches, team, packages, faq, form  # noqa: E402  (модулі без Tilda — перевикористовуємо)

# ---------------------------------------------------------------- картинки
os.makedirs(IMGDIR, exist_ok=True)
_RA_FILES = sorted(os.listdir(RA))
_cache = {}


def img(src, w=None, q=86):
    """Картинка для сторінки: 'file.jpg' з assets/ або 'ra:NN' (оригінал з клону за індексом).
    Растр → WebP (з оригіналу, без повторного стискання), SVG → як є (фіолетовий Tilda → золотий).
    w — максимальна ширина (не збільшуємо). Повертає відносний шлях 'v2/…'."""
    key = (src, w, q)
    if key in _cache:
        return _cache[key]
    path = os.path.join(RA, _RA_FILES[int(src[3:])]) if src.startswith('ra:') else os.path.join(A, src)
    base = re.sub(r'[^a-z0-9]+', '-', os.path.splitext(os.path.basename(src if not src.startswith('ra:') else 'ra' + src[3:]))[0].lower()).strip('-')
    if path.lower().endswith('.svg'):
        data = open(path, encoding='utf-8', errors='ignore').read()
        data = re.sub(r'#(?:cbafff|caaeff|ccafff|dfff5e)', GOLD, data, flags=re.I).encode()
        ext = 'svg'
    else:
        im = Image.open(path)
        im = im.convert('RGBA' if im.mode in ('RGBA', 'LA', 'P') and ('transparency' in im.info or im.mode != 'P') else 'RGB')
        if w and im.width > w:
            im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        buf = io.BytesIO(); im.save(buf, 'WEBP', quality=q, method=6); data = buf.getvalue(); ext = 'webp'
    name = '%s-%s.%s' % (base, hashlib.md5(data).hexdigest()[:8], ext)
    fp = os.path.join(IMGDIR, name)
    if not os.path.exists(fp):
        open(fp, 'wb').write(data)
    _cache[key] = 'v2/' + name
    return _cache[key]


def fonts():
    """Inter (variable, 400–700) з cases-src/fonts → cases/v2. Повертає (css @font-face, теги preload)."""
    css, pre = '', ''
    for sub in ('cyrillic', 'latin'):
        data = open(os.path.join(S, 'fonts', 'inter-%s.woff2' % sub), 'rb').read()
        rng = open(os.path.join(S, 'fonts', 'inter-%s.range' % sub)).read().strip()
        name = 'inter-%s-%s.woff2' % (sub, hashlib.md5(data).hexdigest()[:8])
        fp = os.path.join(IMGDIR, name)
        if not os.path.exists(fp):
            open(fp, 'wb').write(data)
        css += ("@font-face{font-family:'Inter';font-style:normal;font-weight:400 700;font-display:swap;"
                "src:url(v2/%s) format('woff2');unicode-range:%s}" % (name, rng))
        pre += '<link rel="preload" href="v2/%s" as="font" type="font/woff2" crossorigin>' % name
    return css, pre


def favicon():
    im = Image.open(os.path.join(A, 'logo180.png')).convert('RGBA').resize((64, 64), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True); data = buf.getvalue()
    name = 'favicon-%s.png' % hashlib.md5(data).hexdigest()[:8]
    if not os.path.exists(os.path.join(IMGDIR, name)):
        open(os.path.join(IMGDIR, name), 'wb').write(data)
    return 'v2/' + name


def img_size(src):
    path = os.path.join(A, src)
    with Image.open(path) as im:
        return im.size


# ---------------------------------------------------------------- іконки (inline SVG, без зовнішніх файлів)
ARROW = ('<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path d="M4 12h15M13 5l7 7-7 7" '
         'fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
IG = ('<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" '
      'fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" '
      'stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/></svg>')
TGI = ('<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M21.5 4.2 2.9 11.4c-1 .4-1 1.6.1 1.9l4.6 1.4 '
       '1.8 5.6c.3.9 1.4 1.1 2 .4l2.6-2.6 4.8 3.5c.8.6 1.9.1 2.1-.9l3-14.4c.2-1.1-.8-1.9-1.7-1.5zM9.4 14.3l8.4-7.4-6.3 8.6-.3 3.1z" '
       'fill="currentColor"/></svg>')

# ---------------------------------------------------------------- спільні стилі
BASE_CSS = """
:root{--gold:#f6d4aa;--line:#222}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:#000;color:#fff;font-family:'Inter',Arial,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{display:block;max-width:100%;height:auto}
a{color:inherit}
h1,h2,h3,p{margin:0}
.wrap{max-width:1280px;margin:0 auto;padding:0 30px}
.gold{color:var(--gold)}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:16px;z-index:99;background:#fff;color:#000;padding:8px 12px;border-radius:8px}
/* мітка секції: «Для кого», «Про нас»… */
.tag{display:inline-flex;align-items:center;justify-content:center;height:32px;padding:0 22px;border:1px solid var(--line);
  border-radius:50px;font-size:13px;font-weight:600;color:#fff;white-space:nowrap}
/* заголовок секції: мітка зліва, заголовок по центру (як у старій версії); на телефоні — одне під одним */
.sh{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:20px}
.sh .tag{justify-self:start}
.sh h2{grid-column:2;text-align:center}
/* стара сторінка підвантажувала Inter лише до 700, тож усі «800/900» на ній фактично 700 — робимо так само */
.h2{font-size:40px;font-weight:700;line-height:1;letter-spacing:-1px}
/* кнопка «таблетка + коло зі стрілкою» */
.cta{display:inline-flex;align-items:center;text-decoration:none;color:#000;cursor:pointer;border:0;background:none;padding:0;font:inherit}
.cta-t{height:55px;display:flex;align-items:center;padding:0 20px;border-radius:30px;background:var(--gold);
  font-size:16px;font-weight:600;letter-spacing:-1px;white-space:nowrap}
.cta-i{width:55px;height:55px;margin-left:-6px;border-radius:50%;background:var(--gold);display:grid;place-items:center;
  transition:transform .6s ease}
.cta:hover .cta-i{transform:rotate(-37deg)}
@media (max-width:900px){.sh{display:flex;flex-direction:column;gap:16px;text-align:center}.sh .tag{justify-self:auto}}
@media (max-width:640px){.wrap{padding:0 16px}.h2{font-size:28px}
  .cta-t{height:46px;font-size:14px;padding:0 18px}.cta-i{width:46px;height:46px}.cta-i svg{width:22px;height:22px}}
"""

# ---------------------------------------------------------------- шапка + меню
NAV = [('Про нас', '#about'), ('Кейси', '#cases'), ('Послуги', '#services'), ('Контакти', '#contacts')]

HEADER_CSS = """
/* шапка закріплена зверху, як у старій версії; напівпрозоре тло, щоб меню читалось поверх фото */
.hdr{position:fixed;top:0;left:0;right:0;z-index:40;padding-top:7px;pointer-events:none}
.hdr .wrap{pointer-events:auto}
[id]{scroll-margin-top:84px}
.hdr-bar{position:relative;height:66px;border:1px solid var(--line);border-radius:32px;display:flex;align-items:center;
  background:rgba(0,0,0,.55);-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);
  justify-content:space-between;padding:0 10px 0 20px}
.hdr-logo img{width:66px;height:auto}
.hdr-nav{position:absolute;left:50%;transform:translateX(-50%);display:flex;gap:14px}
.hdr-nav a{display:block;padding:16px 16px;color:var(--gold);text-decoration:none;font-size:14px;font-weight:500;
  text-transform:uppercase;letter-spacing:-.2px}
.hdr-nav a:hover{color:#fff}
.hdr-ic{display:flex;gap:10px}
.hdr-ic a,.hdr-burger{width:48px;height:48px;border-radius:50%;border:1px solid var(--line);display:grid;place-items:center;color:var(--gold)}
.hdr-burger{display:none;background:none;cursor:pointer;padding:0}
.hdr-burger span,.hdr-burger span::before,.hdr-burger span::after{display:block;width:20px;height:2px;background:var(--gold);position:relative;content:""}
.hdr-burger span::before{position:absolute;top:-6px}.hdr-burger span::after{position:absolute;top:6px}
.mnav{position:fixed;inset:0;z-index:50;background:rgba(0,0,0,.96);display:none;flex-direction:column;padding:24px 24px 32px}
.mnav.open{display:flex}
.mnav-top{display:flex;justify-content:space-between;align-items:center}
.mnav-top img{width:80px}
.mnav-x{width:48px;height:48px;border-radius:50%;border:1px solid var(--line);background:none;color:#fff;font-size:26px;cursor:pointer}
.mnav nav{display:flex;flex-direction:column;gap:6px;margin:48px 0 auto}
.mnav nav a{font-size:30px;font-weight:700;text-decoration:none;padding:6px 0}
.mnav p{color:#9b9b9b;font-size:14px;line-height:1.4;margin-bottom:14px}
.mnav-btns{display:flex;gap:10px;flex-wrap:wrap}
.mnav-btns a{flex:1;min-width:140px;text-align:center;text-decoration:none;background:var(--gold);color:#000;font-weight:600;border-radius:30px;padding:14px 16px}
@media (max-width:900px){.hdr-nav,.hdr-ic{display:none}.hdr-burger{display:grid}}
@media (max-width:640px){.hdr-bar{height:56px;padding:0 6px 0 16px}.hdr-burger{width:44px;height:44px}}
"""


def header():
    links = ''.join('<a href="%s">%s</a>' % (h, t) for t, h in NAV)
    logo = img('wordmark2.png', w=200)
    return ('<header class="hdr"><div class="wrap"><div class="hdr-bar">'
            '<a class="hdr-logo" href="#top" aria-label="На початок"><img src="%s" alt="Oksana Bogdanets" width="66" height="28"></a>'
            '<nav class="hdr-nav" aria-label="Меню">%s</nav>'
            '<div class="hdr-ic"><a href="%s" target="_blank" rel="noopener" aria-label="Instagram Direct">%s</a>'
            '<a href="%s" target="_blank" rel="noopener" aria-label="Telegram">%s</a></div>'
            '<button class="hdr-burger" type="button" aria-label="Відкрити меню" data-menu-open><span></span></button>'
            '</div></div></header>'
            '<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Меню">'
            '<div class="mnav-top"><img src="%s" alt="Oksana Bogdanets"><button class="mnav-x" type="button" aria-label="Закрити меню" data-menu-close>×</button></div>'
            '<nav>%s</nav>'
            '<p>*Записатись на безкоштовну консультацію — напишіть нам зручним способом</p>'
            '<div class="mnav-btns"><a href="%s" target="_blank" rel="noopener">Telegram</a><a href="%s" target="_blank" rel="noopener">Instagram Direct</a></div>'
            '</div>') % (logo, links, DIRECT, IG, TG, TGI, logo, links, TG, DIRECT)


# ---------------------------------------------------------------- перший екран + мозаїка
HERO_CSS = """
.hero{background:linear-gradient(180deg,#000 0%,#141414 42%,#222 69%,#222 100%)}
.hero-in{position:relative;display:flex;justify-content:space-between;align-items:flex-start;padding:159px 0 50px;min-height:429px}
.hero h1{font-size:60px;font-weight:700;line-height:54px;letter-spacing:-3px;max-width:560px}
.hero-sub{margin-top:16px;max-width:340px;font-size:18px;font-weight:500;line-height:18px;letter-spacing:-1px}
.hero-badge{position:absolute;left:485px;top:170px;width:200px;filter:drop-shadow(0 18px 30px rgba(0,0,0,.45))}
.hero-r{width:300px;margin:36px 99px 0 0}
.hero-txt{font-size:17px;font-weight:500;line-height:1.25}
.hero-r .cta{margin-top:24px}
.mos{position:relative;height:742px;overflow:hidden;background:linear-gradient(180deg,#222 0%,#1b1b1b 55%,#f6d4aa 80%,#f6d4aa 100%)}
.mos-cols{position:absolute;top:0;left:50%;transform:translateX(-50%);display:flex;gap:20px}
.mos-col{width:328px;display:flex;flex-direction:column;gap:20px;animation:mos 90s linear infinite;will-change:transform}
.mos-col:nth-child(even){animation-direction:reverse}
.mos-col:nth-child(2){animation-delay:-30s}.mos-col:nth-child(3){animation-delay:-55s}.mos-col:nth-child(4){animation-delay:-12s}
.mos-col img{width:328px;height:473px;object-fit:cover;border-radius:26px;background:#1b1b1b}
@keyframes mos{from{transform:translateY(0)}to{transform:translateY(-50%)}}
@media (prefers-reduced-motion:reduce){.mos-col{animation:none}}
@media (max-width:1100px){.hero-badge{left:400px}.hero-r{margin-right:0}}
@media (max-width:900px){.hero-in{flex-direction:column}.hero-badge{left:auto;right:0;top:143px;width:150px}.hero-r{margin:28px 0 0}
  .mos{height:520px}.mos-col{width:230px;gap:14px}.mos-col img{width:230px;height:332px;border-radius:20px}.mos-cols{gap:14px}}
@media (max-width:640px){
  .hero-in{padding:73px 0 34px;min-height:0}
  .hero h1{font-size:37px;line-height:34px;letter-spacing:-1.6px}
  .hero-sub{display:none}
  .hero-badge{top:188px;right:4px;width:84px}
  .hero-r{width:252px;margin-top:26px}
  .hero-txt{font-size:13.5px}
  .hero-r .cta{margin-top:12px}
  .mos{height:309px}.mos-cols{gap:7px}.mos-col{width:116px;gap:15px}
  .mos-col img{width:116px;height:167px;border-radius:14px}
  .mos-col:nth-child(4){display:none}}
"""

MOSAIC_COLS = [['m01.jpg', 'm04.jpg', 'm07.jpg'], ['m02.jpg', 'm05.jpg', 'm08.jpg'],
               ['m03.jpg', 'm06.jpg', 'm09.jpg'], ['m04.jpg', 'm08.jpg', 'm02.jpg']]


def hero():
    cols = ''
    for col in MOSAIC_COLS:
        tiles = ''.join('<img src="%s" srcset="%s 260w, %s 480w" sizes="(max-width:640px) 116px, (max-width:900px) 230px, 328px" '
                        'alt="" width="328" height="473" %s>'
                        % (img(f, w=480), img(f, w=260), img(f, w=480), 'loading="lazy"' if n else '')
                        for n, f in enumerate(col + col))   # двічі — для безшовної прокрутки
        cols += '<div class="mos-col" aria-hidden="true">%s</div>' % tiles
    return ('<section class="hero" id="top">%s<div class="wrap"><div class="hero-in">'
            '<div><h1>Reels-просування <br><span class="gold">для експертів та бізнесу</span></h1>'
            '<p class="hero-sub">Повний супровід: від сценарію до зйомки в студії, монтажу і публікації</p></div>'
            '<img class="hero-badge" src="%s" alt="У роботі 20+ ніш" width="200" height="180">'
            '<div class="hero-r"><p class="hero-txt">Отримайте індивідуальну стратегію, яка побудує ваш особистий бренд та збільшить потік клієнтів</p>'
            '<a class="cta" href="%s"><span class="cta-t">Отримати стратегію</span><span class="cta-i">%s</span></a></div>'
            '</div></div></section>'
            '<div class="mos"><div class="mos-cols">%s</div></div>') % (header(), img('badge2.png', w=400), KVIZ, ARROW, cols)


# ---------------------------------------------------------------- «Для кого»
FW_CARDS = [('ra:34', 'Хочете мати особистий бренд в Instagram, але не знаєте, з чого почати',
             'Конкуренти вже просуваються через Reels, і ви відчуваєте, що відстаєте',
             'Будуємо стратегію просування під вашу нішу'),
            ('ra:71', 'Не розумієте, якою має бути система створення контенту',
             'Знімаєте навмання, без чіткого плану, і не маєте жодних результатів',
             'Створюємо ролики лише після аналізу конкурентів, ЦА і ринку — і вже тоді формуємо формати та теми'),
            ('ra:19', 'Немає часу на Reels',
             'Хочете повністю делегувати сценарії, зйомку і монтаж, а не бути самому собі рілсмейкером',
             'Беремо всю роботу під ключ на себе'),
            ('ra:10', 'Робите Reels, але вони не дають жодних результатів',
             'Витрачаєте час і сили, а заявок з Instagram немає',
             'Створюємо Reels, які мають ціль — приводять підписників та клієнтів')]

FW_CSS = """
.fw2{padding:110px 0 70px}
.fw2 .sh{margin-bottom:60px}
.fw2-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px 20px;align-items:stretch}
.fw2-card{background:#000;border:1px solid var(--line);border-radius:20px;padding:30px 20px 20px;text-align:center;display:flex;flex-direction:column;align-items:center}
.fw2-ic{width:40px;height:40px}
.fw2-t{margin:22px 0 12px;font-size:25px;font-weight:600;line-height:1;letter-spacing:-1px}
.fw2-d{color:#a3a3a3;font-size:16px;font-weight:500;line-height:1.1;letter-spacing:-.6px}
.fw2-hr{width:100%;height:1px;margin:18px 0 14px;background:linear-gradient(90deg,transparent,#3a3a3a 20%,#3a3a3a 80%,transparent)}
.fw2-star{width:21px;height:21px;margin-bottom:10px}
.fw2-c{font-size:12.5px;font-weight:600;line-height:1.3;letter-spacing:.25px;text-transform:uppercase;margin-top:auto}
.fw2-ph{border-radius:20px;overflow:hidden;margin-top:-24px;min-height:309px;background:#333}
.fw2-ph img{width:100%;height:100%;object-fit:cover;object-position:50% 25%}
@media (max-width:900px){.fw2-grid{grid-template-columns:repeat(2,1fr)}.fw2-ph{grid-column:1/-1;order:-1;margin-top:0;aspect-ratio:16/9;min-height:0}}
@media (max-width:640px){.fw2{padding:56px 0 30px}.fw2 .sh{margin-bottom:22px}.fw2 .h2{font-size:28px}
  .fw2-grid{grid-template-columns:1fr;gap:12px}.fw2-ph{aspect-ratio:4/3}
  .fw2-card{padding:22px 18px 18px}.fw2-t{font-size:19px;letter-spacing:-.3px;margin:12px 0 8px;line-height:1.2}
  .fw2-d{font-size:14px;line-height:1.4;letter-spacing:0}.fw2-c{font-size:11px;letter-spacing:.04em;line-height:1.35}}
"""


def forwhom():
    star = img('ra:11')
    card = lambda c: ('<div class="fw2-card"><img class="fw2-ic" src="%s" alt="" width="40" height="40" loading="lazy">'
                      '<h3 class="fw2-t">%s</h3><p class="fw2-d">%s</p><div class="fw2-hr"></div>'
                      '<img class="fw2-star" src="%s" alt="" width="21" height="21" loading="lazy"><p class="fw2-c">%s</p></div>'
                      % (img(c[0]), c[1], c[2], star, c[3]))
    photo = ('<div class="fw2-ph"><img src="%s" alt="Оксана Богданець" width="760" height="618" loading="lazy"></div>'
             % img('oksana_forwhom.jpg', w=800))   # нове фото Оксани (біла сукня-костюм), 29.09
    cards = [card(c) for c in FW_CARDS]
    return ('<section class="fw2" id="for"><div class="wrap"><div class="sh"><span class="tag">Для кого</span>'
            '<h2 class="h2">Вам потрібен <span class="gold">Reels Producer</span>, якщо</h2></div>'
            '<div class="fw2-grid">%s%s%s%s%s</div></div></section>') % (cards[0], photo, cards[1], cards[2], cards[3])


# ---------------------------------------------------------------- «Про нас»: лічильники + обкладинки з переглядами + ніші
COUNTERS = [(20, 'ніш у роботі'), (3, 'роки на ринку Reels Production та інфобізнесу'), (10, 'млн переглядів на роликах клієнтів')]
COVERS = ['k07.jpg', 'k03.jpg', 'k26.jpg', 'k01.jpg', 'k25.jpg', 'k04.jpg', 'k27.jpg', 'k02.jpg', 'k05.jpg', 'k11.jpg', 'k13.jpg', 'k08.jpg']
# k26/k27 — Ніна, TikTok 290,4 тис. і 289,5 тис. (скрін Оксани 29.09), пропорція 3:4 — картки стрічки однакової висоти

ABOUT_CSS = """
.ab2{padding:120px 0 0}
.ab2 .sh{margin-bottom:62px}
.ab2-band{padding:0 0 60px;background:linear-gradient(180deg,#000 0%,#171717 19%,#f5d3a9 54%,#000 89%)}
.cnt{display:flex;justify-content:center;gap:10px}
.cnt-c{position:relative;flex:0 1 257px;min-height:233px;background:#000;border:1px solid var(--line);border-radius:20px;
  display:flex;flex-direction:column;align-items:center;padding:30px 24px 26px}
.cnt-c:nth-child(2){flex-basis:313px}
.cnt-pin{position:absolute;top:18px;right:18px;width:28px;height:28px}
.cnt-n{font-size:100px;font-weight:700;line-height:1;letter-spacing:-1px;font-variant-numeric:tabular-nums}
.cnt-l{margin-top:auto;font-size:16px;font-weight:600;line-height:1;letter-spacing:-1px;text-transform:uppercase;text-align:center;color:#d6d6d6;max-width:240px}
.cov{display:flex;gap:15px;overflow-x:auto;scroll-snap-type:x mandatory;padding:28px 30px 4px;scroll-padding:0 30px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.cov::-webkit-scrollbar{display:none}
.cov img{flex:0 0 auto;width:auto;height:365px;object-fit:cover;border-radius:12px;scroll-snap-align:start;background:#1b1b1b}
@media (min-width:1300px){.cov{padding-left:calc((100vw - 1220px)/2);scroll-padding-left:calc((100vw - 1220px)/2)}}
@media (max-width:640px){.ab2{padding-top:56px}.ab2 .sh{margin-bottom:24px}.ab2 .h2{font-size:28px}
  .ab2-band{padding:0 0 30px}
  .cnt{flex-direction:column;padding:0 0}.cnt-c,.cnt-c:nth-child(2){flex:none;min-height:147px;padding:18px 16px 16px}
  .cnt-n{font-size:70px}.cnt-l{font-size:15px;margin-top:10px}.cnt-pin{width:24px;height:24px}
  .cov{gap:10px;padding:22px 16px 4px;scroll-padding:0 16px}.cov img{height:286px}}
"""


def about():
    pin = img('ra:54')
    cnt = ''.join('<div class="cnt-c"><img class="cnt-pin" src="%s" alt="" width="28" height="28" loading="lazy">'
                  '<div class="cnt-n"><span data-count="%d">%d</span>+</div><div class="cnt-l">%s</div></div>'
                  % (pin, n, n, l) for n, l in COUNTERS)
    covers = ''.join('<img src="%s" alt="Обкладинка ролика з переглядами" width="%d" height="365" loading="lazy">'
                     % (img(f, w=560), round(365 * img_size(f)[0] / img_size(f)[1])) for f in COVERS)
    return ('<section class="ab2" id="about"><div class="wrap"><div class="sh"><span class="tag">Про нас</span>'
            '<h2 class="h2">Знімаємо ролики за стратегією під нішу — <br>на основі досвіду з&nbsp;<span class="gold">20+ нішами</span></h2></div></div>'
            '<div class="ab2-band"><div class="wrap"><div class="cnt">%s</div></div><div class="cov">%s</div></div>'
            '%s</section>') % (cnt, covers, niches.html())


# ---------------------------------------------------------------- кейси
CASES = [
    dict(n='01', niche='Юридична компанія', badge=None,
         before='zvilnymo_before.jpg', after='zvilnymo_after_tt.jpg',
         tt=('https://www.tiktok.com/@zvilnymo.com.ua', 44.1),
         head='Результат: з 23 до 225 тис. підписників',
         text='Десятки роликів у TikTok приносять заявки постійно. <strong>7 000 $</strong> з одного Reels, і такі ролики виходять часто'),
    dict(n='02', niche='Психолог', badge='+4 000 підписників',
         before='nina_before.jpg', after='nina_after_tt.jpg',
         tt=('https://www.tiktok.com/@nina_demydenko', 44.1),
         head='Результат: з 1 201 до 6 210 підписників',
         text='За <strong>перший місяць в Instagram і TikTok.</strong> Найпопулярніший ролик набрав <em>382 тис.</em>&nbsp;переглядів<br>'
              'Тепер стабільно набирає терапевтичні групи.'),
    dict(n='03', niche="Кар'єрний консультант", badge='+700 цільових підписників',
         before='julia_before.jpg', after='julia_after.jpg', tt=None,
         head='Результат: +700 цільових з 10 Reels',
         text='Аудиторія зросла <em>у 7 разів</em>, і тепер набирає групу на менторство'),
    dict(n='04', niche='Клініка естетичної медицини', badge='Заявки за 2 тижні',
         before='mbody_before.jpg', after='mbody_after.jpg', tt=None,
         head='Результат: сторінка з 0 за 30 днів',
         text='З порожньої сторінки — до перших заявок <strong>через 2 тижні</strong>. <em>100% органіка</em>, без витрат на таргет'),
]

CASES_CSS = """
.cs{padding:110px 0 80px}
.cs .sh{margin-bottom:60px}
.cs .h2{max-width:680px}
.cs-grid{display:grid;grid-template-columns:repeat(2,400px);justify-content:center;column-gap:10px;row-gap:20px}
.cs-card{background:#000;border:1px solid var(--line);border-radius:20px;padding:20px 20px 12px;display:flex;flex-direction:column}
.cs-pills{display:flex;flex-wrap:wrap;gap:10px}
.pill{display:inline-flex;align-items:center;height:35px;padding:0 20px;border-radius:40px;font-size:12px;font-weight:700;
  text-transform:uppercase;white-space:nowrap}
.pill-w{background:#fff;color:#000}.pill-o{border:1px solid #fff;color:#fff}.pill-g{background:var(--gold);color:#000;padding:0 17px}
.cs-badge{margin-top:10px}
.cs-badge.ph{visibility:hidden}
.pill-s{display:inline-flex;align-self:flex-start;align-items:center;height:29px;padding:0 18px;border:1px solid #828282;border-radius:40px;
  font-size:13px;font-weight:600;text-transform:uppercase;margin:20px 0 20px}
.pill-s.after{margin-top:10px}
.cs-img{border-radius:14px;overflow:hidden;background:#fff}
.cs-img img{width:100%}
.cs-tt{position:relative;display:block;border-radius:14px;overflow:hidden;-webkit-tap-highlight-color:rgba(246,212,170,.25)}
.cs-tt span{position:absolute;right:6px;transform:translateY(-50%);background:var(--gold);color:#000;border-radius:30px;
  padding:8px 13px;font-size:12px;font-weight:600;line-height:1;white-space:nowrap}
.cs-tt .s{display:none}
.cs-res{background:#000;border:1px solid var(--line);border-radius:15px;padding:20px 20px 22px;text-align:center}
.cs-res h3{font-size:16px;font-weight:700;text-transform:uppercase;line-height:1.2}
.cs-res p{margin-top:12px;font-size:13px;font-weight:500;line-height:16px}
.cs-res strong{font-weight:700}
@media (min-width:960px){
  .cs-grid>:nth-child(1){grid-area:1/1}.cs-grid>:nth-child(2){grid-area:2/1}.cs-grid>:nth-child(3){grid-area:1/2}.cs-grid>:nth-child(4){grid-area:2/2}
  .cs-grid>:nth-child(5){grid-area:3/1}.cs-grid>:nth-child(6){grid-area:4/1}.cs-grid>:nth-child(7){grid-area:3/2}.cs-grid>:nth-child(8){grid-area:4/2}
  .cs-grid>:nth-child(4n+3),.cs-grid>:nth-child(4n+1){margin-top:0}}
@media (max-width:959px){.cs-grid{grid-template-columns:minmax(0,400px)}.cs-badge.ph{display:none}.cs-card+.cs-res{margin-top:-8px}}
@media (max-width:640px){.cs{padding:56px 0 50px}.cs .sh{margin-bottom:26px}.cs .h2{font-size:28px}
  .cs-grid{grid-template-columns:1fr}.cs-card{padding:16px 16px 10px}.pill{height:32px;padding:0 16px;font-size:11px}
  .pill-s{margin:16px 0 14px;height:27px;font-size:12px}.cs-res h3{font-size:14px}
  .cs-tt .l{display:none}.cs-tt .s{display:inline}}
"""


def cases():
    items = ''
    for c in CASES:
        badge = ('<div class="cs-badge"><span class="pill pill-g">%s</span></div>' % c['badge'] if c['badge']
                 else '<div class="cs-badge ph" aria-hidden="true"><span class="pill pill-g">&nbsp;</span></div>')
        w, h = img_size(c['after'])
        after_img = '<img src="%s" alt="Після: профіль і ролики" width="%d" height="%d" loading="lazy">' % (img(c['after'], w=760), w, h)
        if c['tt']:
            after = ('<a class="cs-tt" href="%s" target="_blank" rel="noopener" aria-label="Відкрити TikTok">%s'
                     '<span style="top:%s%%"><b class="l">Відкрити TikTok ↗</b><b class="s">Дивитись ↗</b></span></a>'
                     % (c['tt'][0], after_img, c['tt'][1]))
        else:
            after = '<div class="cs-img">%s</div>' % after_img
        bw, bh = img_size(c['before'])
        items += ('<article class="cs-card"><div class="cs-pills"><span class="pill pill-w">Кейс %s</span><span class="pill pill-o">%s</span></div>'
                  '%s<span class="pill-s">До</span><div class="cs-img"><img src="%s" alt="До: профіль" width="%d" height="%d" loading="lazy"></div>'
                  '<span class="pill-s after">Після</span>%s</article>'
                  '<div class="cs-res"><h3>%s</h3><p>%s</p></div>'
                  % (c['n'], c['niche'], badge, img(c['before'], w=760), bw, bh, after, c['head'], c['text']))
    return ('<section class="cs" id="cases"><div class="wrap"><div class="sh"><span class="tag">Кейси</span>'
            '<h2 class="h2">Працюємо не заради переглядів. Робимо так, щоб ви <span class="gold">отримували клієнтів</span></h2></div>'
            '<div class="cs-grid">%s</div></div></section>') % items


# ---------------------------------------------------------------- етапи роботи (+ спливне вікно «Обговорити проєкт»)
STAGES = [('Етап 1', 'Підготовка', 'Бриф і стратегічна сесія в Zoom, договір і оплата. Аналізуємо конкурентів, ринок і продукт, формуємо УТП.',
           'Команда має все, щоб за 2 тижні зібрати стратегію і написати сценарії.'),
          ('Етап 2', 'Створення стратегії', 'Підбираємо теми й референси, пишемо сценарії, коригуємо і репетируємо їх у Zoom, затверджуємо.',
           'Затверджені сценарії з хуками, воронками й описами.'),
          ('Етап 3', 'Погодження стилю зйомки', 'Погоджуємо образ, локації, акторів і реквізит, фіксуємо дату зйомки — усе в Telegram.',
           'Зафіксовані дата, образ, локація і реквізит — на майданчику нічого не вирішуємо.'),
          ('Етап 4', 'Організація і зйомка', 'Відпрацьовуємо жестикуляцію і подачу, знімаємо за один день, монтуємо.',
           'Готові змонтовані ролики. Від стратегічної сесії до цього моменту — місяць.')]

STAGES_CSS = """
.st2{padding:66px 0 0;background:linear-gradient(180deg,#000 0%,#131313 14%,#f3d1a8 51%,#100e0b 100%)}
.st2-top{display:flex;justify-content:flex-start;gap:60px;align-items:flex-start;padding-left:141px}
@media (max-width:1100px){.st2-top{padding-left:0;justify-content:center}}
.st2 h2{font-size:100px;font-weight:700;line-height:80px;letter-spacing:-3px;text-transform:uppercase}
.st2-side{padding-top:0;max-width:300px}
.st2-sub{margin:18px 0 32px;font-size:16px;font-weight:500;line-height:19px;text-transform:uppercase}
.st2-cards{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:66px;padding-bottom:20px}
.st2-card{background:#000;border:1px solid var(--line);border-radius:20px;padding:20px 20px 20px;display:flex;flex-direction:column}
.st2-hd{display:flex;align-items:center;justify-content:space-between;gap:10px;padding-bottom:16px;
  border-bottom:1px solid;border-image:linear-gradient(90deg,#2a2a2a,#4a4560,#2a2a2a) 1}
.st2-n{font-size:40px;font-weight:700;line-height:1;white-space:nowrap}
.st2-t{font-size:13px;line-height:1.1;max-width:105px}
.st2-w{display:flex;align-items:center;gap:6px;margin:30px 0 20px;font-size:13px;font-weight:700;text-transform:uppercase}
.st2-w img{width:21px;height:21px}
.st2-d{font-size:13px;line-height:1.15;margin-bottom:26px}
.st2-r{margin-top:auto;background:var(--gold);border-radius:10px;padding:16px 16px 20px;color:#000;min-height:110px}
.st2-r b{display:block;font-size:13px;font-weight:700;color:#7a6650;text-transform:uppercase;margin-bottom:14px}
.st2-r p{font-size:13px;font-weight:600;line-height:1.15}
@media (max-width:1100px){.st2-cards{grid-template-columns:repeat(2,1fr)}}
@media (max-width:640px){.st2{padding:40px 0 10px;background:linear-gradient(180deg,#000 0,#1a1a1a 18%,#222 30%,#000 60%)}
  .st2-top{flex-direction:column;align-items:center;text-align:center;gap:16px;padding:0}
  .st2 h2{font-size:56px;line-height:50px;letter-spacing:-2px;order:1}
  .st2-side{display:contents}.st2-side .tag{order:0}.st2-sub{margin:0;font-size:14px;order:2}.st2-side .cta{order:3;margin-top:4px}
  .st2-cards{grid-template-columns:1fr;gap:12px;margin-top:34px}
  .st2-card{padding:20px 18px 18px}.st2-n{font-size:30px}.st2-t{font-size:14px;max-width:none;text-align:right}
  .st2-w{margin:16px 0 8px}.st2-d{font-size:14px;line-height:1.4;margin-bottom:16px;color:#d2d2d2}
  .st2-r{min-height:0;padding:14px 16px}.st2-r b{font-size:12px;margin-bottom:6px}.st2-r p{font-size:14px;line-height:1.35}}
.mdl{position:fixed;inset:0;z-index:60;background:rgba(0,0,0,.85);display:none;align-items:center;justify-content:center;padding:20px}
.mdl.open{display:flex}
.mdl-box{position:relative;max-width:560px;width:100%;background:#111;border:1px solid var(--line);border-radius:24px;padding:40px 30px 30px;text-align:center}
.mdl-box h3{font-size:22px;font-weight:700;text-transform:uppercase;line-height:1.15}
.mdl-box p{color:#b5b5b5;font-size:15px;line-height:1.4;margin-top:12px}
.mdl-box .note{color:var(--gold);font-size:13px;margin-top:16px}
.mdl-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:22px}
.mdl-btns a{min-width:180px;text-decoration:none;background:var(--gold);color:#000;font-weight:600;border-radius:30px;padding:16px 20px}
.mdl-x{position:absolute;top:12px;right:12px;width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:none;color:#fff;font-size:24px;cursor:pointer}
"""


def stages():
    star = img('ra:62')
    cards = ''.join('<div class="st2-card"><div class="st2-hd"><span class="st2-n">%s</span><span class="st2-t">%s</span></div>'
                    '<div class="st2-w"><img src="%s" alt="" width="21" height="21" loading="lazy">Що робимо:</div><p class="st2-d">%s</p>'
                    '<div class="st2-r"><b>Результат:</b><p>%s</p></div></div>' % (n, t, star, d, r) for n, t, d, r in STAGES)
    return ('<section class="st2" id="stages"><div class="wrap"><div class="st2-top">'
            '<h2><span class="gold">4 етапи </span><br>роботи</h2>'
            '<div class="st2-side"><span class="tag">Етапи роботи</span><p class="st2-sub">Від стратегічної сесії до готових відео — місяць.</p>'
            '<button class="cta" type="button" data-modal-open><span class="cta-t">Обговорити проєкт</span><span class="cta-i">%s</span></button></div>'
            '</div><div class="st2-cards">%s</div></div></section>'
            '<div class="mdl" id="mdl" role="dialog" aria-modal="true" aria-label="Запис на консультацію"><div class="mdl-box">'
            '<button class="mdl-x" type="button" aria-label="Закрити" data-modal-close>×</button>'
            '<h3>Запишіться на безкоштовну консультацію</h3>'
            '<p>Розберемо вашу нішу, підберемо формат зйомки і дамо поради з підготовки</p>'
            '<p class="note">*Напишіть нам зручним способом</p>'
            '<div class="mdl-btns"><a href="%s" target="_blank" rel="noopener">Telegram</a><a href="%s" target="_blank" rel="noopener">Instagram Direct</a></div>'
            '</div></div>') % (ARROW, cards, TG, DIRECT)


# ---------------------------------------------------------------- приклади відео
VIDEOS = [8, 4, 9, 6, 7, 10, 11, 12, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23, 24]   # порядок = порядок на сайті (video/vN.mp4)

VIDEOS_CSS = """
.vd2{padding:90px 0 60px}
.sh-c{display:flex;flex-direction:column;align-items:center;gap:14px;text-align:center}
.vd2 .h2{max-width:520px}
.vd2-row{display:flex;gap:30px;overflow-x:auto;scroll-snap-type:x mandatory;padding:60px 30px 10px;scroll-padding:0 30px;scrollbar-width:none;-webkit-overflow-scrolling:touch}
.vd2-row::-webkit-scrollbar{display:none}
.vd{position:relative;flex:0 0 337px;width:337px;height:556px;border-radius:20px;overflow:hidden;background:#141414;scroll-snap-align:start;
  border:0;padding:0;cursor:pointer}
.vd img,.vd video{width:100%;height:100%;object-fit:cover;display:block}
.vd i{position:absolute;top:50%;left:50%;width:74px;height:74px;margin:-37px 0 0 -37px;border-radius:50%;background:rgba(0,0,0,.55);
  border:2px solid var(--gold);box-shadow:0 8px 30px rgba(0,0,0,.5);display:grid;place-items:center}
.vd i::after{content:"";margin-left:6px;border-style:solid;border-width:13px 0 13px 21px;border-color:transparent transparent transparent var(--gold)}
.vd.on i{display:none}
@media (min-width:1300px){.vd2-row{padding-left:calc((100vw - 1220px)/2);scroll-padding-left:calc((100vw - 1220px)/2)}}
@media (max-width:640px){.vd2{padding:50px 0 40px}.vd2 .h2{font-size:28px}
  .vd2-row{gap:14px;padding:26px 16px 6px;scroll-padding:0 16px}.vd{flex-basis:78vw;width:78vw;height:calc(78vw * 1.65);max-width:310px;max-height:512px}}
"""


def videos():
    # div, а не button: у <button> не можна класти <video> з кнопками керування
    cards = ''.join('<div class="vd" role="button" tabindex="0" data-video="video/v%d.mp4" aria-label="Відтворити відео %d">'
                    '<img src="video/v%d-cover.webp" alt="" width="337" height="556" loading="lazy"><i></i></div>' % (v, k + 1, v)
                    for k, v in enumerate(VIDEOS))
    return ('<section class="vd2" id="videos"><div class="wrap"><div class="sh-c"><span class="tag">Кейси</span>'
            '<h2 class="h2"><span class="gold">Приклади відео</span> знятих і змонтованих нами</h2></div></div>'
            '<div class="vd2-row">%s</div></section>') % cards


# ---------------------------------------------------------------- відгуки
import reviews_m  # noqa: E402

REV_CSS = """
.rv2{padding:80px 0 70px}
.rv2 .sh{margin-bottom:60px}
.rv2-img{max-width:1010px;margin:0 auto}
.rv2-img img{width:100%}
@media (max-width:639px){.rv2{padding:50px 0 10px}.rv2 .sh{margin-bottom:24px}.rv2 .h2{font-size:28px}.rv2-img{display:none}}
"""


def reviews():
    w, h = img_size('chats.jpg')
    return ('<section class="rv2" id="reviews"><div class="wrap"><div class="sh"><span class="tag">Відгуки</span>'
            '<h2 class="h2">Нам довіряють — і повертаються</h2></div>'
            '<div class="rv2-img"><img src="%s" alt="Відгук клієнтки в Telegram" width="%d" height="%d" loading="lazy"></div></div>'
            '%s</section>') % (img('chats.jpg', w=2020), w, h, reviews_m.html(lambda f: img(f, w=160)))


# ---------------------------------------------------------------- команда + «Хто веде проєкт»
def team_about():
    return team.html(lambda f: img(f, w=360)) + blocks.about(img('oksana_about45.jpg', w=720))


# ---------------------------------------------------------------- формати співпраці
# «Хто веде проєкт» (29.09, Оксана: «щоб було на всю лінію, а не збоку»): фото 4:5 на всю висоту картки,
# на телефоні — на всю ширину картки
ABOUT2_CSS = """
#oks-about .ab{grid-template-columns:360px 1fr;align-items:stretch;padding:28px}
#oks-about .ab-ph{aspect-ratio:4/5;height:100%}
#oks-about .ab>div:last-child{align-self:center}
@media (max-width:1000px){#oks-about .ab{grid-template-columns:260px 1fr}}
@media (max-width:640px){#oks-about .ab{grid-template-columns:1fr;padding:16px}#oks-about .ab-ph{max-width:none;width:100%;height:auto}}
"""

FMT_CSS = """
.fmt2{padding:60px 0 50px}
@media (max-width:640px){.fmt2{padding:40px 0 26px}.fmt2 .h2{font-size:28px}}
"""


def formats():
    return ('<section class="fmt2" id="services"><div class="wrap"><div class="sh"><span class="tag">Прийшов час обирати</span>'
            '<h2 class="h2">Формати співпраці</h2></div></div></section>' + packages.html(DIRECT))


# ---------------------------------------------------------------- форма + футер
def contact_form():
    return '<div id="contacts"></div>' + form.html()


FOOTER_CSS = """
.ft{padding:80px 0 30px}
.ft-card{display:grid;grid-template-columns:1fr auto 1fr;align-items:start;gap:30px;padding:40px 46px 30px}
.ft h4{font-size:16px;font-weight:700;margin:0 0 14px;line-height:1.2}
.ft-nav a{display:block;font-size:13px;line-height:1.1;padding:4px 0;text-decoration:none}
.ft-nav a:hover,.ft-bottom a:hover{color:var(--gold)}
.ft-logo{width:300px;max-width:100%;margin-top:-6px}
.ft-c{justify-self:end;min-width:180px}
.ft-ic{display:flex;gap:8px;margin-bottom:16px}
.ft-ic a{width:36px;height:30px;border-radius:15px;border:1px solid var(--line);display:grid;place-items:center;color:var(--gold)}
.ft-ic svg{width:16px;height:16px}
.ft-c p{font-size:13px;line-height:1.5}
.ft-bottom{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin:10px 46px 0;padding-top:24px;border-top:1px solid #2a2a2a;
  font-size:13px;color:#d2d2d2}
.ft-bottom a{text-decoration:none}
@media (max-width:640px){.ft{padding:50px 0 24px}
  .ft-card{grid-template-columns:1fr 1fr;padding:0;gap:26px 16px}
  .ft-logo{grid-column:1/-1;order:-1;width:200px;justify-self:center}
  .ft-c{justify-self:start}
  .ft-bottom{margin:30px 0 0;flex-direction:column;gap:10px}}
"""


def footer():
    links = ''.join('<a href="%s">%s</a>' % (h, t) for t, h in [('Головна', '#top')] + NAV)
    return ('<footer class="ft"><div class="wrap"><div class="ft-card">'
            '<div class="ft-nav"><h4>Навігація</h4>%s</div>'
            '<img class="ft-logo" src="%s" alt="Oksana Bogdanets" width="300" height="125" loading="lazy">'
            '<div class="ft-c"><h4>Контакти</h4><div class="ft-ic"><a href="%s" target="_blank" rel="noopener" aria-label="Telegram">%s</a>'
            '<a href="%s" target="_blank" rel="noopener" aria-label="Instagram Direct">%s</a></div>'
            '<p>ФОП Богданець Оксана<br>Київ, Україна</p></div></div>'
            '<div class="ft-bottom"><span>©2026 Усі права захищені</span><a href="#">Згода на обробку персональних даних</a>'
            '<a href="#">Політика конфіденційності</a></div></div></footer>') % (links, img('wordmark2.png', w=600), TG, TGI, DIRECT, IG)


# ---------------------------------------------------------------- збірка сторінки
SECTIONS = [hero, blocks.mission, forwhom, about, cases, stages, blocks.results, videos, reviews, team_about, formats, faq.html,
            contact_form, footer]
CSS_PARTS = [BASE_CSS, HEADER_CSS, HERO_CSS, blocks.CSS, FW_CSS, ABOUT_CSS, niches.CSS, CASES_CSS, STAGES_CSS, VIDEOS_CSS, reviews_m.CSS, REV_CSS,
             team.CSS, ABOUT2_CSS, FMT_CSS, packages.CSS, faq.CSS, form.CSS, FOOTER_CSS]

JS = """
(function(){
  var m=document.getElementById('mnav');
  document.querySelectorAll('[data-menu-open]').forEach(function(b){b.addEventListener('click',function(){m.classList.add('open')})});
  m.querySelectorAll('[data-menu-close],nav a').forEach(function(b){b.addEventListener('click',function(){m.classList.remove('open')})});
})();
// спливне вікно «Обговорити проєкт»
(function(){
  var m=document.getElementById('mdl'); if(!m) return;
  document.querySelectorAll('[data-modal-open]').forEach(function(b){b.addEventListener('click',function(){m.classList.add('open')})});
  m.addEventListener('click',function(e){if(e.target===m||e.target.hasAttribute('data-modal-close'))m.classList.remove('open')});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')m.classList.remove('open')});
})();
// відео: обкладинка → плеєр лише після натискання (не вантажимо 19 відео наперед), грає одне за раз
(function(){
  document.querySelectorAll('[data-video]').forEach(function(b){b.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();b.click()}});b.addEventListener('click',function(){
    if(b.classList.contains('on')) return;
    document.querySelectorAll('.vd.on video').forEach(function(v){v.pause()});
    var v=document.createElement('video'); v.src=b.getAttribute('data-video'); v.controls=true; v.playsInline=true; v.setAttribute('playsinline','');
    v.poster=b.querySelector('img').getAttribute('src'); b.classList.add('on'); b.querySelector('img').replaceWith(v); v.play();
    v.addEventListener('play',function(){document.querySelectorAll('.vd.on video').forEach(function(o){if(o!==v)o.pause()})});
  })});
})();
// лічильники «Про нас»: рахують від 0, коли з'являються на екрані
(function(){
  var els=[].slice.call(document.querySelectorAll('[data-count]'));
  function run(e){var to=+e.getAttribute('data-count'),t0=null;e.textContent='0';
    function f(t){t0=t0||t;var k=Math.min(1,(t-t0)/1400);e.textContent=Math.round(to*(1-Math.pow(1-k,3)));if(k<1)requestAnimationFrame(f)}requestAnimationFrame(f)}
  function chk(){els=els.filter(function(e){var r=e.getBoundingClientRect();if(r.top<innerHeight-40&&r.bottom>0){run(e);return false}return true});
    if(!els.length)removeEventListener('scroll',chk)}
  addEventListener('scroll',chk,{passive:true});chk();
})();
"""

HEAD = """<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Reels-просування для експертів і бізнесу · Оксана Богданець</title>
<meta name="description" content="Reels під ключ: від сценарію до зйомки в студії, монтажу й публікації. Кейси з результатами до/після.">
<meta property="og:type" content="website">
<meta property="og:title" content="Reels-просування для експертів і бізнесу">
<meta property="og:description" content="Повний супровід: сценарій, студія, монтаж, публікація. 7 000 $ з одного Reels.">
<meta property="og:image" content="%(site)sog-cases.jpg">
<meta property="og:url" content="%(site)s">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="%(site)s">
<link rel="icon" type="image/png" href="%(favicon)s">
%(fontpre)s
<style>%(css)s</style>
</head>
<body>
<a class="skip" href="#main">До основного змісту</a>
"""


def build():
    body = ''.join(f() for f in SECTIONS)
    fcss, fpre = fonts()
    css = fcss + re.sub(r'\n\s*', '\n', ''.join(CSS_PARTS)).strip()
    html = (HEAD % {'site': SITE, 'favicon': favicon(), 'css': css, 'fontpre': fpre}
            + '<main id="main">' + body + '</main>\n<script>' + JS + '</script>\n</body>\n</html>\n')
    open(os.path.join(OUT, PAGE), 'w', encoding='utf-8').write(html)
    used = set(re.findall(r'v2/[\w.-]+', html))
    for f in os.listdir(IMGDIR):                       # прибрати старі версії картинок
        if 'v2/' + f not in used:
            os.remove(os.path.join(IMGDIR, f))
    print('%s: %d КБ HTML, картинок %d (%.0f КБ)' % (PAGE, len(html.encode()) // 1024, len(used),
          sum(os.path.getsize(os.path.join(IMGDIR, f[3:])) for f in used) / 1024))


if __name__ == '__main__':
    build()
