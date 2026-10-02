#!/usr/bin/env python3
"""Блог і SEO-сторінки oksanabogdanets.com.ua: markdown із «фабрики SEO» -> статичний HTML.

Запуск (з кореня репо):
    python3 cases-src/blog.py           # пише сторінки з PAGES, blog/index.html, доповнює sitemap.xml
    python3 cases-src/blog.py --check   # лише збирає в пам'яті й перевіряє, нічого не пише

Джерело: ~/Desktop/фабрика SEO/03-статті/<файл>.md (інша папка — змінна SEO_SRC).
У PAGES додаємо ЛИШЕ матеріали з «ок» Оксани (дата «ока» в полі ok); без ok сторінка не збирається.
З markdown публікується тільки текст сторінки: від H1 до «## Нотатки для верстальника».
Рядки «[ПИТАННЯ ОКСАНІ: …]», «ГОТОВО ДО ПОКАЗУ» і службові поля над H1 на сайт не потрапляють.
Головну (site2.py), cases/ і robots.txt скрипт не чіпає. Стиль — як на головній: чорний, золото, Inter.
"""
import html
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = 'https://oksanabogdanets.com.ua'
SRC = Path(os.environ.get('SEO_SRC', Path.home() / 'Desktop' / 'фабрика SEO' / '03-статті'))
AUTHOR = 'Оксана Богданець'
OG_IMAGE = SITE + '/cases/og-cases.jpg'
TG = 'https://t.me/ksysha_bogdanets'
IG = 'https://ig.me/m/ksysha.bogdanets'
FORM = '/#oks-form'          # форма запису на головній
CTA_TEXT = 'Записатись на стратегічну сесію'

# kind: service — сторінка послуги в корені; article — стаття в /blog/<slug>/
PAGES = [
    dict(src='reels-pid-klyuch-kyiv.md', path='/reels-pid-klyuch-kyiv/', kind='service',
         date='2026-10-02', ok='2026-10-02', crumb='Reels під ключ', name='Reels під ключ у Києві', priority='0.9'),
    dict(src='strakh-kamery.md', path='/blog/strakh-kamery/', kind='article',
         date='2026-10-02', ok='2026-10-02', crumb='Страх камери', priority='0.7'),
]
BLOG = dict(path='/blog/', date='2026-10-02', priority='0.6',
            title='Блог про Reels для експертів · Оксана Богданець',
            description='Статті Оксани Богданець про Reels для експертів і бізнесу: '
                        'як готуватися до зйомки і подолати страх камери.',
            h1='Блог про Reels',
            lead='Статті Оксани Богданець про Reels для експертів і бізнесу.')

FORBIDDEN = ('ПИТАННЯ ОКСАНІ', 'Нотатки для верстальника', 'ГОТОВО ДО ПОКАЗУ', '[Кнопка')
QUESTION_LINE = re.compile(r'^\s*\[ПИТАННЯ ОКСАНІ:.*\]\s*$')
QUESTION_INLINE = re.compile(r'\s*\[ПИТАННЯ ОКСАНІ:[^\]]*\]')
BUTTON_LINE = re.compile(r'^\*\*\[Кнопка.*\*\*\s*$')
MONTHS = ['січня', 'лютого', 'березня', 'квітня', 'травня', 'червня',
          'липня', 'серпня', 'вересня', 'жовтня', 'листопада', 'грудня']

ARROW = ('<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true"><path d="M4 12h15M13 5l7 7-7 7" '
         'fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_TG = ('<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><path d="M21.5 4.2 2.9 11.4c-1 .4-1 1.6.1 1.9l4.6 1.4 '
           '1.8 5.6c.3.9 1.4 1.1 2 .4l2.6-2.6 4.8 3.5c.8.6 1.9.1 2.1-.9l3-14.4c.2-1.1-.8-1.9-1.7-1.5zM9.4 14.3l8.4-7.4-6.3 8.6-.3 3.1z" '
           'fill="currentColor"/></svg>')
ICON_IG = ('<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" '
           'fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4.2" fill="none" stroke="currentColor" '
           'stroke-width="2"/><circle cx="17.4" cy="6.6" r="1.3" fill="currentColor"/></svg>')

# Meta Pixel — той самий блок, що в кореневому index.html (набір «Оксана Богданець | Особистий бренд»)
PIXEL = ("<!-- Meta Pixel: набір даних «Оксана Богданець | Особистий бренд» (Events Manager), Оксана 02.10 -->\n"
         "<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):"
         "n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);"
         "t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script',"
         "'https://connect.facebook.net/en_US/fbevents.js');fbq('init','1478624944307903');fbq('track','PageView');</script>")
PIXEL_NOSCRIPT = ('<noscript><img height="1" width="1" style="display:none" alt="" '
                  'src="https://www.facebook.com/tr?id=1478624944307903&amp;ev=PageView&amp;noscript=1"></noscript>')
# як на головній: натискання на Direct або Telegram = подія Contact
CONTACT_JS = """<script>
document.addEventListener('click',function(e){
  var a=e.target.closest&&e.target.closest('a[href^="https://ig.me/"],a[href^="https://t.me/"]');
  if(a&&window.fbq) fbq('track','Contact',{content_name:a.href.indexOf('ig.me')>0?'Instagram Direct':'Telegram'});
});
</script>"""

CSS = r"""@font-face{font-family:'Inter';font-style:normal;font-weight:400 700;font-display:swap;src:url(/cases/v2/inter-cyrillic-4e255302.woff2) format('woff2');unicode-range:U+0301, U+0400-045F, U+0490-0491, U+04B0-04B1, U+2116}
@font-face{font-family:'Inter';font-style:normal;font-weight:400 700;font-display:swap;src:url(/cases/v2/inter-latin-65850a37.woff2) format('woff2');unicode-range:U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD}
:root{--gold:#f6d4aa;--line:#222;--text:#e8e8e8;--muted:#9b9b9b}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;background:#000;color:var(--text);font-family:'Inter',Arial,sans-serif;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{display:block;max-width:100%;height:auto}
a{color:inherit}
.wrap{max-width:1280px;margin:0 auto;padding:0 30px}
.skip{position:absolute;left:-9999px}.skip:focus{left:16px;top:16px;z-index:99;background:#fff;color:#000;padding:8px 12px;border-radius:8px}
[id]{scroll-margin-top:90px}
/* шапка — як на головній: чорна «таблетка» з рамкою */
.hdr{position:sticky;top:0;z-index:40;padding:7px 0;background:#000}
.hdr-bar{height:66px;border:1px solid var(--line);border-radius:32px;display:flex;align-items:center;justify-content:space-between;gap:12px;padding:0 10px 0 20px;background:#000}
.hdr-logo{display:block;line-height:0;flex:none}
.hdr-logo img{width:auto;height:18px}
.hdr-nav{display:flex;gap:4px}
.hdr-nav a{display:block;padding:14px 12px;color:var(--gold);text-decoration:none;font-size:14px;font-weight:500;text-transform:uppercase;letter-spacing:-.2px}
.hdr-nav a:hover,.hdr-nav a[aria-current]{color:#fff}
.hdr-cta{display:inline-flex;align-items:center;height:46px;padding:0 20px;border-radius:30px;background:var(--gold);color:#000;text-decoration:none;font-size:15px;font-weight:600;letter-spacing:-.4px;white-space:nowrap;flex:none}
.hdr-cta .s{display:none}
/* колонка тексту */
.col{max-width:780px;margin:0 auto;padding:36px 30px 72px}
.crumbs{font-size:13px;line-height:1.5;color:var(--muted);margin:0 0 22px}
.crumbs a{color:var(--muted);text-decoration:none}.crumbs a:hover{color:var(--gold)}
h1{font-size:44px;line-height:1.08;font-weight:700;letter-spacing:-1.2px;color:#fff;margin:0 0 18px}
.meta{font-size:14px;color:var(--muted);margin:0 0 34px}
.lead{font-size:19px;line-height:1.6;margin:0 0 34px}
.prose{font-size:18px;line-height:1.7;overflow-wrap:break-word}
.prose p{margin:0 0 1.1em}
.prose h2{font-size:30px;line-height:1.15;font-weight:700;letter-spacing:-.7px;color:#fff;margin:2.1em 0 .7em}
.prose h2::before{content:"";display:block;width:44px;height:2px;background:var(--gold);margin:0 0 18px}
.prose h3{font-size:21px;line-height:1.3;font-weight:700;color:var(--gold);margin:1.6em 0 .55em}
.prose h3.q{font-size:19px;color:#fff;margin:1.5em 0 .4em}
.prose strong{color:#fff;font-weight:600}
.prose a{color:var(--gold);text-decoration:underline;text-decoration-thickness:1px;text-underline-offset:3px}
.prose a:hover{color:#fff}
.prose ul,.prose ol{list-style:none;margin:0 0 1.2em;padding:0}
.prose li{position:relative;padding-left:32px;margin:0 0 .65em}
.prose ul>li::before{content:"";position:absolute;left:8px;top:.72em;width:7px;height:7px;border-radius:50%;background:var(--gold)}
.prose ol{counter-reset:n}
.prose ol>li{counter-increment:n}
.prose ol>li::before{content:counter(n);position:absolute;left:0;top:.26em;width:22px;height:22px;border-radius:50%;border:1px solid var(--gold);color:var(--gold);font-size:12px;font-weight:600;line-height:20px;text-align:center}
.prose hr{border:0;border-top:1px solid var(--line);margin:2.4em 0}
.prose blockquote{margin:0 0 1.2em;padding:4px 0 4px 20px;border-left:2px solid var(--gold)}
/* кнопка «таблетка + коло зі стрілкою» — як на головній */
.cta-box{margin:2.4em 0 0;padding:30px 24px;border:1px solid var(--line);border-radius:24px;text-align:center}
.cta{display:inline-flex;align-items:center;text-decoration:none;color:#000;cursor:pointer}
.cta-t{height:55px;display:flex;align-items:center;padding:0 20px;border-radius:30px;background:var(--gold);font-size:16px;font-weight:600;letter-spacing:-.6px;white-space:nowrap}
.cta-i{width:55px;height:55px;margin-left:-6px;border-radius:50%;background:var(--gold);display:grid;place-items:center;transition:transform .6s ease}
.cta:hover .cta-i{transform:rotate(-37deg)}
.prose .cta,.prose .cta:hover{color:#000;text-decoration:none}   /* інакше .prose a фарбує текст кнопки в золото */
.cta-alt,.prose .cta-alt{margin:16px 0 0;font-size:15px;line-height:1.5;color:var(--muted)}
.cta-alt a{color:var(--gold);text-underline-offset:3px}
/* список статей */
.posts{list-style:none;margin:0;padding:0;display:grid;gap:18px}
.post{border:1px solid var(--line);border-radius:24px;padding:28px}
.post h2{font-size:26px;line-height:1.2;font-weight:700;letter-spacing:-.6px;margin:0 0 10px}
.post h2 a{color:#fff;text-decoration:none}.post h2 a:hover{color:var(--gold)}
.post p{margin:0 0 14px;font-size:17px;line-height:1.6}
.post .meta{margin:0 0 12px}
.post .more{color:var(--gold);font-weight:600;font-size:15px;text-decoration:none}
/* підвал — як на головній */
.ft{padding:60px 0 30px;border-top:1px solid #111}
.ft-card{display:grid;grid-template-columns:1fr auto 1fr;align-items:start;gap:30px;padding:20px 46px 30px}
.ft h4{font-size:16px;font-weight:700;margin:0 0 14px;line-height:1.2;color:#fff}
.ft-nav a{display:block;font-size:13px;line-height:1.1;padding:4px 0;text-decoration:none;color:#fff}
.ft-nav a:hover,.ft-bottom a:hover{color:var(--gold)}
.ft-logo{width:300px;max-width:100%;margin-top:-6px}
.ft-c{justify-self:end;min-width:180px}
.ft-ic{display:flex;gap:8px;margin-bottom:16px}
.ft-ic a{width:36px;height:30px;border-radius:15px;border:1px solid var(--line);display:grid;place-items:center;color:var(--gold)}
.ft-c p{font-size:13px;line-height:1.5;margin:0;color:#fff}
.ft-bottom{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;margin:10px 46px 0;padding-top:24px;border-top:1px solid #2a2a2a;font-size:13px;color:#d2d2d2}
.ft-bottom a{text-decoration:none}
@media (max-width:1060px){.hdr-nav{display:none}}
@media (max-width:640px){.wrap{padding:0 16px}
.hdr-bar{height:58px;padding:0 6px 0 16px}.hdr-logo img{height:14px}
.hdr-cta{height:44px;padding:0 16px;font-size:14px}.hdr-cta .l{display:none}.hdr-cta .s{display:inline}
.col{padding:24px 16px 56px}
h1{font-size:30px;letter-spacing:-.8px;margin-bottom:14px}.meta{margin-bottom:26px}.lead{font-size:17px}
.prose{font-size:17px;line-height:1.65}.prose h2{font-size:24px;letter-spacing:-.5px}.prose h3{font-size:19px}.prose h3.q{font-size:18px}
.cta-box{padding:24px 14px}
.cta-t{height:46px;font-size:14px;padding:0 16px;letter-spacing:-.4px}.cta-i{width:46px;height:46px}.cta-i svg{width:22px;height:22px}
.post{padding:22px 18px}.post h2{font-size:22px}
.ft{padding:44px 0 24px}
.ft-card{grid-template-columns:1fr 1fr;padding:0;gap:26px 16px}
.ft-logo{grid-column:1/-1;order:-1;width:200px;justify-self:center}
.ft-c{justify-self:start;min-width:0}
.ft-bottom{margin:30px 0 0;flex-direction:column;gap:10px}}"""


# ---------- markdown -> HTML (мінімальний конвертер під наші статті) ----------

def typo(s):
    """Нерозривні пробіли: після однолітерних слів, перед тире, у числах «7 000 $», «1,9 млн»."""
    s = re.sub(r'(?<![\w\'-])([ІіЙйВвУуЗзАаОоЯяІі]) ', r'\1&nbsp;', s)
    s = s.replace(' — ', '&nbsp;— ')
    s = re.sub(r'(\d) (?=\d{3}\b)', r'\1&nbsp;', s)
    s = re.sub(r'(\d) (?=[€$%]|млн|тис|хв|роликів|сценаріїв|відео)', r'\1&nbsp;', s)
    return s


def inline(s):
    s = typo(html.escape(s, quote=False))
    s = re.sub(r'\[([^\]]+)\]\(([^)\s]+)\)', lambda m: f'<a href="{m.group(2)}">{m.group(1)}</a>', s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<![*\w])\*(?![\s*])(.+?)(?<![\s*])\*(?![*\w])', r'<em>\1</em>', s)
    # контакти в тексті — клікабельні
    s = re.sub(r'(?<![\w/.])@ksysha_bogdanets\b', f'<a href="{TG}" target="_blank" rel="noopener">@ksysha_bogdanets</a>', s)
    s = re.sub(r'(?<![\w/.])@ksysha\.bogdanets\b', f'<a href="{IG}" target="_blank" rel="noopener">@ksysha.bogdanets</a>', s)
    s = s.replace('через форму на сайті', f'через <a href="{FORM}">форму на сайті</a>')
    return s


def cta_box():
    return (f'<aside class="cta-box" aria-label="Запис на стратегічну сесію">'
            f'<a class="cta" href="{FORM}"><span class="cta-t">{CTA_TEXT}</span><span class="cta-i">{ARROW}</span></a>'
            f'<p class="cta-alt">або напишіть: <a href="{TG}" target="_blank" rel="noopener">Telegram</a> · '
            f'<a href="{IG}" target="_blank" rel="noopener">Instagram Direct</a></p></aside>')


def md_to_html(text):
    """Повертає (h1, html_тіла, є_кнопка). Підтримка: # ## ###, абзаци, - / 1. списки, ---, >, **, *, [](), кнопка."""
    out, para = [], []
    h1, has_cta = None, False

    def flush():
        if not para:
            return
        m = re.fullmatch(r'\*\*(.+)\*\*', para[0].strip())
        if m and len(para) > 1:          # «**Питання?**» + відповідь наступним рядком (FAQ)
            out.append(f'<h3 class="q">{inline(m.group(1))}</h3>')
            out.append(f'<p>{inline(" ".join(x.strip() for x in para[1:]))}</p>')
        else:
            out.append(f'<p>{inline(" ".join(x.strip() for x in para))}</p>')
        para.clear()

    lines = text.split('\n')
    i = 0
    while i < len(lines):
        ln = lines[i].rstrip()
        if not ln.strip():
            flush(); i += 1; continue
        if BUTTON_LINE.match(ln):
            flush(); out.append(cta_box()); has_cta = True; i += 1; continue
        m = re.match(r'^(#{1,3})\s+(.+)$', ln)
        if m:
            flush()
            level, title = len(m.group(1)), m.group(2).strip()
            if level == 1:
                if h1 is not None:
                    raise SystemExit('Більше одного H1')
                h1 = title
            else:
                out.append(f'<h{level}>{inline(title)}</h{level}>')
            i += 1; continue
        if ln.strip() == '---':
            flush(); out.append('<hr>'); i += 1; continue
        for tag, rx in (('ul', r'^[-*]\s+(.+)$'), ('ol', r'^\d+\.\s+(.+)$')):
            if re.match(rx, ln):
                flush()
                items = []
                while i < len(lines) and re.match(rx, lines[i].rstrip()):
                    items.append(re.match(rx, lines[i].rstrip()).group(1)); i += 1
                out.append(f'<{tag}>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + f'</{tag}>')
                break
        else:
            if ln.startswith('>'):
                flush()
                q = []
                while i < len(lines) and lines[i].startswith('>'):
                    q.append(lines[i][1:].strip()); i += 1
                out.append(f'<blockquote><p>{inline(" ".join(q))}</p></blockquote>')
                continue
            para.append(ln); i += 1
            continue
    flush()
    if h1 is None:
        raise SystemExit('Немає H1')
    return h1, '\n'.join(out), has_cta


# ---------- джерело ----------

def load(page):
    raw = (SRC / page['src']).read_text(encoding='utf-8')
    lines = raw.split('\n')
    start = next(i for i, l in enumerate(lines) if l.startswith('# '))
    meta = {}
    for l in lines[:start]:
        m = (re.match(r'^\*\*(Title|Description):\*\*\s*(.+?)\s*$', l)
             or re.match(r'^(title|description):\s*"?(.*?)"?\s*$', l))
        if m:
            meta[m.group(1).lower()] = m.group(2)
    end = next((i for i, l in enumerate(lines) if l.strip().startswith('## Нотатки для верстальника')), len(lines))
    body = [l for l in lines[start:end] if not QUESTION_LINE.match(l)]
    while body and body[-1].strip() in ('', '---'):
        body.pop()
    text = QUESTION_INLINE.sub('', '\n'.join(body))
    text = re.sub(r'\n{3,}', '\n\n', text)
    for k in ('title', 'description'):
        if not meta.get(k):
            raise SystemExit(f'{page["src"]}: немає {k}')
    return meta, text


# ---------- шаблон ----------

def human_date(iso):
    y, m, d = iso.split('-')
    return f'{int(d)} {MONTHS[int(m) - 1]} {y}'


def ld(obj):
    return ('<script type="application/ld+json">'
            + json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>')


def crumbs_ld(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': n + 1, 'name': name, 'item': SITE + path} for n, (name, path) in enumerate(items)]}


def header(current):
    nav = [('/', 'Головна'), ('/#cases', 'Кейси'), ('/reels-pid-klyuch-kyiv/', 'Reels під ключ'), ('/blog/', 'Блог')]
    cur = ' aria-current="page"'
    links = ''.join(f'<a href="{h}"{cur if h == current else ""}>{t}</a>' for h, t in nav)
    return (f'<header class="hdr"><div class="wrap"><div class="hdr-bar">'
            f'<a class="hdr-logo" href="/" aria-label="Оксана Богданець — на головну">'
            f'<img src="/cases/v2/wordmark-line-f211d95a.webp" alt="Оксана Богданець" width="180" height="18"></a>'
            f'<nav class="hdr-nav" aria-label="Меню">{links}</nav>'
            f'<a class="hdr-cta" href="{FORM}"><span class="l">{CTA_TEXT}</span><span class="s">Записатись</span></a>'
            f'</div></div></header>')


def footer():
    nav = [('/', 'Головна'), ('/#about', 'Про нас'), ('/#cases', 'Кейси'), ('/#services', 'Послуги'),
           ('/reels-pid-klyuch-kyiv/', 'Reels під ключ'), ('/blog/', 'Блог'), ('/#contacts', 'Контакти')]
    return ('<footer class="ft"><div class="wrap"><div class="ft-card">'
            '<div class="ft-nav"><h4>Навігація</h4>' + ''.join(f'<a href="{h}">{t}</a>' for h, t in nav) + '</div>'
            '<img class="ft-logo" src="/cases/v2/wordmark2-389b131e.webp" alt="Оксана Богданець" width="300" height="125" loading="lazy">'
            f'<div class="ft-c"><h4>Контакти</h4><div class="ft-ic">'
            f'<a href="{TG}" target="_blank" rel="noopener" aria-label="Telegram">{ICON_TG}</a>'
            f'<a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram Direct">{ICON_IG}</a></div>'
            '<p>ФОП Богданець Оксана<br>Київ, Україна</p></div></div>'
            '<div class="ft-bottom"><span>©2026 Усі права захищені</span>'
            '<a href="/privacy-policy.html">Політика конфіденційності</a></div></div></footer>')


def document(*, title, description, path, og_type, jsonld, crumbs, main, extra_head=''):
    url = SITE + path
    esc = lambda s: html.escape(s, quote=True)
    trail = ' / '.join([f'<a href="{p}">{html.escape(n)}</a>' for n, p in crumbs[:-1]]
                       + [f'<span aria-current="page">{html.escape(crumbs[-1][0])}</span>'])
    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:locale" content="uk_UA">
<meta property="og:site_name" content="Оксана Богданець">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{OG_IMAGE}">
<meta name="twitter:card" content="summary_large_image">
{extra_head}<link rel="icon" type="image/png" href="/cases/v2/favicon-c86237b7.png">
<link rel="preload" href="/cases/v2/inter-cyrillic-4e255302.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/cases/v2/inter-latin-65850a37.woff2" as="font" type="font/woff2" crossorigin>
{ld(jsonld)}
<style>{CSS}</style>
{PIXEL}
</head>
<body>
{PIXEL_NOSCRIPT}
<a class="skip" href="#main">До основного змісту</a>
{header(path)}
<main id="main"><div class="col">
<nav class="crumbs" aria-label="Ви тут">{trail}</nav>
{main}
</div></main>
{footer()}
{CONTACT_JS}
</body>
</html>
"""


def reading_minutes(text):
    return max(1, round(len(re.findall(r'\w+', text)) / 180))


def build_page(page):
    meta, text = load(page)
    h1, body, has_cta = md_to_html(text)
    if not has_cta:
        body += '\n' + cta_box()
    url = SITE + page['path']
    person = {'@type': 'Person', 'name': AUTHOR, 'url': SITE + '/'}
    if page['kind'] == 'article':
        crumbs = [('Головна', '/'), ('Блог', '/blog/'), (page['crumb'], page['path'])]
        node = {'@type': 'Article', 'headline': h1, 'description': meta['description'], 'url': url,
                'mainEntityOfPage': url, 'image': OG_IMAGE, 'inLanguage': 'uk',
                'datePublished': page['date'], 'dateModified': page['date'], 'author': person, 'publisher': person}
        info = (f'<p class="meta">{AUTHOR} · <time datetime="{page["date"]}">{human_date(page["date"])}</time>'
                f' · {reading_minutes(text)} хв читання</p>')
        og_type = 'article'
        extra = f'<meta property="article:published_time" content="{page["date"]}">\n'
    else:
        crumbs = [('Головна', '/'), (page['crumb'], page['path'])]
        node = {'@type': 'Service', 'name': page['name'], 'serviceType': 'Reels під ключ',
                'description': meta['description'], 'url': url, 'image': OG_IMAGE,
                'areaServed': {'@type': 'City', 'name': 'Київ'},
                'provider': {'@type': 'ProfessionalService', 'name': 'Оксана Богданець — Reels під ключ',
                             'url': SITE + '/', 'image': OG_IMAGE,
                             'address': {'@type': 'PostalAddress', 'addressLocality': 'Київ', 'addressCountry': 'UA'}}}
        info, og_type, extra = '', 'website', ''
    jsonld = {'@context': 'https://schema.org', '@graph': [node, crumbs_ld(crumbs)]}
    main = (f'<article><h1>{inline(h1)}</h1>\n{info}\n<div class="prose">\n{body}\n</div></article>')
    doc = document(title=meta['title'], description=meta['description'], path=page['path'], og_type=og_type,
                   jsonld=jsonld, crumbs=crumbs, main=main, extra_head=extra)
    return doc, dict(h1=h1, description=meta['description'], minutes=reading_minutes(text))


def build_blog_index(articles):
    person = {'@type': 'Person', 'name': AUTHOR, 'url': SITE + '/'}
    cards = ''.join(
        f'<li class="post"><h2><a href="{p["path"]}">{inline(info["h1"])}</a></h2>'
        f'<p class="meta"><time datetime="{p["date"]}">{human_date(p["date"])}</time> · {info["minutes"]} хв читання</p>'
        f'<p>{inline(info["description"])}</p><a class="more" href="{p["path"]}">Читати статтю →</a></li>'
        for p, info in articles)
    crumbs = [('Головна', '/'), ('Блог', '/blog/')]
    jsonld = {'@context': 'https://schema.org', '@graph': [
        {'@type': 'Blog', 'name': BLOG['h1'], 'url': SITE + BLOG['path'], 'inLanguage': 'uk',
         'description': BLOG['description'], 'author': person,
         'blogPost': [{'@type': 'BlogPosting', 'headline': info['h1'], 'url': SITE + p['path'],
                       'datePublished': p['date'], 'author': person} for p, info in articles]},
        crumbs_ld(crumbs)]}
    main = (f'<h1>{inline(BLOG["h1"])}</h1>\n<p class="lead">{inline(BLOG["lead"])}</p>\n'
            f'<ul class="posts">{cards}</ul>\n{cta_box()}')
    return document(title=BLOG['title'], description=BLOG['description'], path=BLOG['path'], og_type='website',
                    jsonld=jsonld, crumbs=crumbs, main=main)


# ---------- перевірки, sitemap ----------

def out_file(path):
    return ROOT / path.strip('/') / 'index.html'


def check(path, doc, built):
    errs = []
    for bad in FORBIDDEN:
        if bad in doc:
            errs.append(f'службовий текст «{bad}»')
    if doc.count('<h1') != 1:
        errs.append(f'H1: {doc.count("<h1")}')
    for need in ('<title>', 'name="description"', 'rel="canonical"', 'og:title', 'og:description', 'og:url',
                 'og:image', 'application/ld+json', "fbq('init','1478624944307903')", CTA_TEXT, 'href="/"'):
        if need not in doc:
            errs.append(f'немає {need}')
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        json.loads(m.group(1))
    for ref in set(re.findall(r'(?:href|src)="(/[^"#?]*)', doc)) | set(re.findall(r'url\((/[^)]+)\)', doc)):
        f = ROOT / ref.lstrip('/')
        if ref.endswith('/'):
            if ref not in built and not (f / 'index.html').exists():
                errs.append(f'бите посилання {ref}')
        elif ref != '/' and not f.exists():
            errs.append(f'немає файлу {ref}')
    if errs:
        raise SystemExit(f'{path}: ' + '; '.join(errs))


def update_sitemap(entries):
    p = ROOT / 'sitemap.xml'
    s = p.read_text(encoding='utf-8')
    add = ''.join(f'  <url><loc>{loc}</loc><lastmod>{mod}</lastmod><priority>{prio}</priority></url>\n'
                  for loc, mod, prio in entries if f'<loc>{loc}</loc>' not in s)
    if add:
        s = s.replace('</urlset>', add + '</urlset>')
        p.write_text(s, encoding='utf-8')
    return add


def main():
    dry = '--check' in sys.argv
    pages = [p for p in PAGES if p.get('ok')]
    for p in PAGES:
        if not p.get('ok'):
            print(f'пропущено (немає «ок» Оксани): {p["src"]}')
    built_paths = {p['path'] for p in pages} | {BLOG['path']}
    out, articles = {}, []
    for p in pages:
        doc, info = build_page(p)
        out[p['path']] = doc
        if p['kind'] == 'article':
            articles.append((p, info))
    articles.sort(key=lambda x: x[0]['date'], reverse=True)
    out[BLOG['path']] = build_blog_index(articles)
    for path, doc in out.items():
        check(path, doc, built_paths)
    if dry:
        print('перевірки пройдено:', ', '.join(out))
        return
    for path, doc in out.items():
        f = out_file(path)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(doc, encoding='utf-8')
        print('записано', f.relative_to(ROOT))
    entries = [(SITE + p['path'], p['date'], p['priority']) for p in pages]
    entries.append((SITE + BLOG['path'], max([BLOG['date']] + [p['date'] for p, _ in articles]), BLOG['priority']))
    added = update_sitemap(entries)
    print('sitemap.xml:', 'додано\n' + added if added else 'без змін')


if __name__ == '__main__':
    main()
