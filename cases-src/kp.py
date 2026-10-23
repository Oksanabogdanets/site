#!/usr/bin/env python3
"""Комерційна пропозиція у вигляді сайту: oksanabogdanets.com.ua/kp/ (Оксана 23.10.2026).

Структура — як PDF «КомерційнаПропозиція-2пакети» (Desktop/продажи рілс під ключ): обкладинка, «ми — креативне
агентство», клієнти, місія, що вміємо, кейси, приклади відео (клікабельні), що входить і хто працює, старт, етапи,
вартість, контакти. Стиль і блоки — з головної (site2.py). Ціни тільки тут, сторінка закрита від пошуку (noindex).
Ціни (Оксана 23.10): під ключ 15 відео $1100 / 30 відео $2100; зйомка і монтаж (без стратегії й сценаріїв) 15 відео $700.
Запуск: python3 cases-src/kp.py → kp/index.html
"""
import os
import re
import sys

S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import site2  # noqa: E402
from site2 import img, blocks, consent, TG, DIRECT, ARROW  # noqa: E402

OUT = os.path.join(os.path.dirname(S), 'kp', 'index.html')

KP_CSS = """
.kp-cover{position:relative;min-height:640px;display:grid;grid-template-columns:1.05fr .95fr;align-items:center;overflow:hidden}
.kp-cover .ph{position:absolute;right:0;top:0;bottom:0;width:58%}
.kp-cover .ph img{width:100%;height:100%;object-fit:cover;object-position:50% 20%}
.kp-cover .ph::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,#000 0%,rgba(0,0,0,.55) 30%,rgba(0,0,0,0) 62%)}
.kp-cover .tx{position:relative;z-index:1;padding:90px 0}
.kp-cover h1{font-family:'Oswald','Inter',sans-serif;font-weight:600;font-size:76px;line-height:1.04;text-transform:uppercase;letter-spacing:.5px}
.kp-cover .ig{display:inline-flex;align-items:center;gap:10px;margin-top:30px;padding:12px 22px;border-radius:40px;background:#fff;color:#000;
  font-weight:600;text-decoration:none;font-size:18px}
.kp-sec{padding:80px 0}
.kp-lead{max-width:900px;margin:0 auto;text-align:center}
.kp-lead p.big{font-family:'Oswald','Inter',sans-serif;font-size:34px;line-height:1.25;text-transform:uppercase;font-weight:500}
.pills{display:flex;flex-wrap:wrap;justify-content:center;gap:14px;margin-top:34px}
.pill-p{background:var(--gold);color:#000;border-radius:18px;padding:16px 22px;font-weight:600;font-size:16px;line-height:1.25;max-width:260px}
.kp-clients{display:flex;flex-wrap:wrap;justify-content:center;gap:22px;margin-top:40px}
.kp-clients figure{margin:0;display:flex;flex-direction:column;align-items:center;gap:10px;width:150px;text-align:center}
.kp-clients img{width:110px;height:110px;border-radius:24px;object-fit:cover;border:1px solid var(--line);background:#fff}
.kp-clients figcaption{font-size:13px;color:#bdbdbd;line-height:1.3}
.kp-skills{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:40px}
.kp-card{border:1px solid rgba(246,212,170,.3);border-radius:22px;padding:26px;background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%)}
.kp-card h3{font-family:'Oswald','Inter',sans-serif;font-weight:600;font-size:24px;text-transform:uppercase;color:var(--gold);margin-bottom:12px}
.kp-card p{color:#d2d2d2;font-size:15px;line-height:1.45}
.kp-two{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:40px}
.kp-two ul{margin:0;padding:0;list-style:none;columns:2;column-gap:20px}
.kp-two li{padding:7px 0 7px 22px;position:relative;color:#e6e6e6;font-size:15px;break-inside:avoid}
.kp-two li::before{content:"✦";position:absolute;left:0;color:var(--gold);font-size:12px;top:9px}
.kp-steps{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:40px;counter-reset:s}
.kp-step{border:1px solid var(--line);border-radius:22px;padding:26px;text-align:center}
.kp-step b{display:block;font-family:'Oswald','Inter',sans-serif;font-size:44px;color:var(--gold);line-height:1;margin-bottom:10px}
.kp-step span{font-size:17px;font-weight:600}
.kp-price{display:grid;grid-template-columns:repeat(2,1fr);gap:18px;margin-top:40px;max-width:900px;margin-left:auto;margin-right:auto}
.pr{border:1px solid rgba(246,212,170,.3);border-radius:24px;padding:28px 26px;display:flex;flex-direction:column;
  background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%)}
.pr.main{border-color:rgba(246,212,170,.75);box-shadow:0 18px 50px rgba(246,212,170,.10)}
.pr h3{font-family:'Oswald','Inter',sans-serif;font-weight:600;font-size:24px;text-transform:uppercase;color:var(--gold);line-height:1.15}
.pr .sub{color:#9b9b9b;font-size:14px;line-height:1.4;margin:10px 0 18px;min-height:3.9em}
.pr .row{display:flex;justify-content:space-between;align-items:baseline;gap:12px;padding:14px 0;border-top:1px solid rgba(255,255,255,.08)}
.pr .row span{font-size:16px;color:#e6e6e6}
.pr .row b{font-family:'Oswald','Inter',sans-serif;font-size:34px;font-weight:600;font-variant-numeric:tabular-nums}
.pr .inc{margin:14px 0 22px;padding:0;list-style:none;flex:1}
.pr .inc li{font-size:14px;color:#cfcfcf;padding:5px 0 5px 22px;position:relative;line-height:1.35}
.pr .inc li::before{content:"✓";position:absolute;left:0;color:var(--gold)}
.pr .inc li.no{color:#6a6a6a;text-decoration:line-through}.pr .inc li.no::before{content:"✕";color:#6a6a6a}
.pr .btn{display:block;text-align:center;background:var(--gold);color:#000;border-radius:40px;padding:15px 18px;font-weight:600;text-decoration:none}
.kp-end{text-align:center;padding:90px 0 40px}
.kp-end h2{font-family:'Oswald','Inter',sans-serif;font-weight:600;font-size:64px;text-transform:uppercase;line-height:1.05}
.kp-end .btns{display:flex;justify-content:center;gap:14px;flex-wrap:wrap;margin-top:34px}
.kp-end .btns a{border:1px solid var(--gold);color:var(--gold);border-radius:40px;padding:15px 26px;font-weight:600;text-decoration:none}
.kp-end .btns a.f{background:var(--gold);color:#000}
@media (max-width:900px){.kp-cover{grid-template-columns:1fr;min-height:0}
  .kp-cover .ph{position:relative;width:100%;height:440px;order:-1}
  .kp-cover .ph::after{background:linear-gradient(0deg,#000 0%,rgba(0,0,0,0) 45%)}
  .kp-cover .tx{padding:0 0 40px;margin-top:-90px}
  .kp-cover h1{font-size:48px}
  .kp-skills,.kp-steps,.kp-price,.kp-two{grid-template-columns:1fr}
  .kp-lead p.big{font-size:24px}.kp-end h2{font-size:42px}.kp-two ul{columns:1}}
"""

CLIENTS = [('ava_zv1.png', 'Юридична компанія «Звільнимо»'), ('ava_mbody.png', 'Клініка естетичної медицини'),
           ('ava_nina.png', 'Психолог Ніна Демиденко'), ('ava_julia.png', "Кар'єрний консультант"),
           ('ilona_case.jpg', 'Освіта в ЄС')]

INCLUDED = ['діагностика', 'стратегічна сесія', 'аналіз ринку і конкурентів', 'аналіз цільової аудиторії', 'аналіз продукту',
            'контент-стратегія', 'сценарії', 'репетиція сценаріїв у Zoom', 'підбір образу і локації', 'зйомка', 'монтаж',
            'обкладинки на відео']
TEAM = ['продюсер', 'маркетолог', 'таргетолог', 'project manager', 'менеджер зйомки', 'сценарист', 'оператор',
        'монтажер', 'SMM-спеціаліст']

# (назва, для кого, [(обсяг, ціна)], що входить: (пункт, так/ні), головний)
# 23.10 Оксана: лише 2 пакети; під ключ 15 = $1100, 30 = 2×1100 − 100 = $2100; щотижневу аналітику прибрати;
# «без зйомки» прибрати; зйомка і монтаж без стратегії й сценаріїв — $700; обкладинки входять в обидва
PRICES = [
    ('Reels під ключ', 'Повний цикл: стратегія, сценарії, зйомка і монтаж. Від вас — лише Zoom на репетицію сценаріїв '
     'і 5 годин на зйомці.',
     [('15 відео', '$1100'), ('30 відео', '$2100')],
     [('Аналіз ринку, конкурентів, цільової аудиторії і продукту', 1), ('Стратегія просування', 1),
      ('Сценарії з хуками', 1), ('Репетиція сценаріїв у Zoom', 1), ('Підбір образу, локації і реквізиту', 1),
      ('Зйомка з оператором і постановка подачі', 1), ('Монтаж', 1), ('Обкладинки на відео', 1)], True),
    ('Зйомка і монтаж', 'Стратегія, сценарії й ідеї — ваші. Ми знімаємо, монтуємо і робимо обкладинки.',
     [('15 відео', '$700')],
     [('Аналіз ринку, конкурентів, цільової аудиторії і продукту', 0), ('Стратегія просування', 0),
      ('Сценарії з хуками', 0), ('Зйомка з оператором', 1), ('Монтаж', 1), ('Обкладинки на відео', 1)], False),
]


def cover():
    return ('<section class="kp-cover" id="top"><div class="ph"><img src="%s" alt="Оксана Богданець" width="800" height="1000"></div>'
            '<div class="wrap"><div class="tx"><h1>Комерційна<br><span class="gold">пропозиція</span></h1>'
            '<a class="ig" href="https://www.instagram.com/ksysha.bogdanets/" target="_blank" rel="noopener">ksysha.bogdanets ↗</a>'
            '</div></div></section>') % img('oksana_about_suit.jpg', w=1100)


def agency():
    pills = ''.join('<div class="pill-p">%s</div>' % t for t in
                    ('Перетворюємо продукт — в стиль', 'Статистику — в можливості', 'Стратегію просування — в гармонію'))
    return ('<section class="kp-sec"><div class="wrap kp-lead"><p class="big"><span class="gold">Ми — креативне агентство</span> '
            'і знаємо, як зробити так, щоб ваші відео працювали на охоплення, продажі та побудову особистого бренду</p>'
            '<div class="pills">%s</div></div></section>') % pills


def clients():
    items = ''.join('<figure><img src="%s" alt="" width="110" height="110" loading="lazy"><figcaption>%s</figcaption></figure>'
                    % (img(f, w=240), t) for f, t in CLIENTS)
    return ('<section class="kp-sec"><div class="wrap"><div class="sh-c"><span class="tag">Наші клієнти</span>'
            '<h2 class="h2">З ким ми працюємо</h2></div><div class="kp-clients">%s</div></div></section>') % items


def skills():
    cards = [('Reels-просування', 'Просування під ключ експертів, підприємців і компаній через вертикальні ролики Reels.'),
             ('TikTok-просування', 'Відео в TikTok, які набирають 100 000+ переглядів і працюють на впізнаваність бренду.'),
             ('Просування + воронки', 'Монетизація контенту і залучення клієнтів через структурно побудовані воронки продажів.')]
    html = ''.join('<div class="kp-card"><h3>%s</h3><p>%s</p></div>' % c for c in cards)
    return ('<section class="kp-sec"><div class="wrap"><div class="sh-c"><span class="tag">Що ми вміємо</span>'
            '<h2 class="h2">Наші напрямки</h2></div><div class="kp-skills">%s</div></div></section>') % html


def included():
    li = lambda xs: ''.join('<li>%s</li>' % x for x in xs)
    return ('<section class="kp-sec"><div class="wrap"><div class="sh-c"><span class="tag">Ведення Reels / TikTok під ключ</span>'
            '<h2 class="h2">Що входить і хто працює над проєктом</h2></div><div class="kp-two">'
            '<div class="kp-card"><h3>Сюди входить</h3><ul>%s</ul></div>'
            '<div class="kp-card"><h3>Над проєктом працює</h3><ul>%s</ul></div></div></div></section>') % (li(INCLUDED), li(TEAM))


def start():
    steps = ''.join('<div class="kp-step"><b>%d</b><span>%s</span></div>' % (i + 1, t) for i, t in
                    enumerate(('Робимо Zoom-зустріч', 'Заповнюємо бриф', 'Підписуємо договір')))
    return ('<section class="kp-sec"><div class="wrap"><div class="sh-c"><span class="tag">Старт</span>'
            '<h2 class="h2">Що потрібно для старту</h2></div><div class="kp-steps">%s</div></div></section>') % steps


def prices():
    cards = ''
    for name, sub, rows, inc, main in PRICES:
        r = ''.join('<div class="row"><span>%s</span><b>%s</b></div>' % x for x in rows)
        i = ''.join('<li%s>%s</li>' % ('' if ok else ' class="no"', t) for t, ok in inc)
        cards += ('<div class="pr%s"><h3>%s</h3><p class="sub">%s</p>%s<ul class="inc">%s</ul>'
                  '<a class="btn" href="%s" target="_blank" rel="noopener">Обговорити пакет →</a></div>'
                  % (' main' if main else '', name, sub, r, i, TG))
    return ('<section class="kp-sec" id="prices"><div class="wrap"><div class="sh-c"><span class="tag">Вартість</span>'
            '<h2 class="h2">Вартість <span class="gold">наших послуг</span></h2></div><div class="kp-price">%s</div></div></section>') % cards


def contacts():
    return ('<section class="kp-end"><div class="wrap"><h2>Бажаєте<br><span class="gold">співпрацювати?</span></h2>'
            '<div class="btns"><a class="f" href="%s" target="_blank" rel="noopener">Написати в Telegram</a>'
            '<a href="%s" target="_blank" rel="noopener">Написати в Instagram Direct</a></div></div></section>') % (TG, DIRECT)


SECTIONS = [cover, agency, clients, blocks.mission, skills, site2.cases, site2.videos, included, start, site2.stages,
            prices, contacts, site2.footer]

HEAD = """<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="robots" content="noindex, nofollow">
<title>Комерційна пропозиція · Оксана Богданець</title>
<meta name="description" content="Reels і TikTok під ключ: кейси, приклади відео, етапи роботи і вартість.">
<meta property="og:title" content="Комерційна пропозиція · Оксана Богданець">
<meta property="og:description" content="Reels і TikTok під ключ: кейси, приклади відео, етапи роботи і вартість.">
<meta property="og:image" content="https://oksanabogdanets.com.ua/cases/og-cases.jpg?v=2">
<link rel="icon" type="image/png" href="%(favicon)s">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600&display=swap">
%(fontpre)s
<style>%(css)s</style>
%(pixel)s
</head>
<body>
"""


# на сторінці КП немає мобільного меню головної — без цієї перевірки скрипт падав і відео не запускались
JS = site2.JS.replace("var m=document.getElementById('mnav');", "var m=document.getElementById('mnav'); if(!m) return;", 1)


def build():
    body = ''.join(f() for f in SECTIONS)
    fcss, fpre = site2.fonts()
    css = fcss + re.sub(r'\n\s*', '\n', ''.join(site2.CSS_PARTS) + KP_CSS).strip()
    page = (HEAD % {'favicon': site2.favicon(), 'css': css, 'fontpre': fpre, 'pixel': consent.HEAD}
            + '<main id="main">' + body + '</main>\n<script>' + JS + '</script>\n' + consent.BANNER + '\n</body>\n</html>\n')
    page = page.replace('href="#top"', 'href="/"')                         # «Головна» у підвалі — на сайт
    page = re.sub(r'href="#(about|cases|services|contacts)"', r'href="/#\1"', page)
    page = re.sub(r'(?<![/\w.-])(v2/|video/)', r'/cases/\1', page)       # ресурси головної лежать у /cases/
    page = page.replace('href="../privacy-policy.html"', 'href="/privacy-policy.html"')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(page)
    print('kp/index.html: %d КБ' % (len(page.encode()) // 1024))


if __name__ == '__main__':
    build()
