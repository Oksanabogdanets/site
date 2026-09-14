"""Відгуки як оформлені цитати — без скріншотів чатів.

Скріни з Canva мали лише ~370px завширшки: і шпалери Telegram видно,
і після вирізання бульбашок виходило рвано. Тому — текст у картках.
Правити = міняти REVIEWS: (ім'я, хто це, текст).
"""

# заповнюється з оригінальних скрінів / OCR — поки порожньо, блок не рендериться
REVIEWS = []

CSS = """
#oks-rev{background:#000;padding:0 20px 90px;font-family:'Inter',Arial,sans-serif}
#oks-rev .rv-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
#oks-rev .rv-card{position:relative;border-radius:24px;padding:34px 26px 26px;
  background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);border:1px solid rgba(246,212,170,.18)}
#oks-rev .rv-q{position:absolute;top:14px;left:22px;color:#f6d4aa;font-size:54px;line-height:1;opacity:.55;font-family:Georgia,serif}
#oks-rev .rv-t{color:#d2d2d2;font-size:16px;line-height:1.5;margin:14px 0 22px}
#oks-rev .rv-n{color:#fff;font-size:15px;font-weight:600}
#oks-rev .rv-r{color:#9b9b9b;font-size:13px;margin-top:3px}
@media screen and (max-width:1000px){#oks-rev .rv-grid{grid-template-columns:repeat(2,1fr)}}
@media screen and (max-width:640px){#oks-rev{padding-bottom:60px}#oks-rev .rv-grid{grid-template-columns:1fr;gap:14px}
  #oks-rev .rv-card{padding:30px 20px 22px}}
"""


def html():
    if not REVIEWS:
        return ''
    cards = ''.join('<div class="rv-card"><div class="rv-q">“</div><p class="rv-t">%s</p>'
                    '<div class="rv-n">%s</div><div class="rv-r">%s</div></div>' % (t, n, r)
                    for n, r, t in REVIEWS)
    return ('<div id="oks-rev"><div class="oks-in"><span class="oks-tag">Відгуки</span>'
            '<h2 class="oks-h2">Нам довіряють — <b>і повертаються</b></h2>'
            '<div class="rv-grid">%s</div></div></div>' % cards)
