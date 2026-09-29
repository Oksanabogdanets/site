"""Етапи роботи на телефоні (≤639px).

Мобільна копія Tilda-блоку етапів (rec1575166851) — 4 картки в один ряд із прокруткою вбік:
видно лише першу, а велика цифра налазила на слово «Етап» (Оксана 29.09: «Етап 1, Етап 2, Етап 3,
Етап 4 — все перемішалося»). На телефоні показуємо картки одна під одною; тексти беремо з десктопного
блоку (rec1558035631), щоб не дублювати. Заголовок «4 етапи роботи» (rec1575165041) лишається Tilda.
"""
import re

# (Етап N, назва, що робимо, результат) — id текстів у rec1558035631
STAGES = [('176314310323332090', '176314310325129970', '176314294687414690', '176314294688717070'),
          ('176314294689685120', '176314294690097560', '176314294692160210', '176314294693186340'),
          ('176314294694146400', '176314294694438690', '176314294697088490', '176314294698192400'),
          ('176314294699174820', '176314294699589770', '176314294702062550', '176314294703250180')]

CSS = """
#oks-st{display:none;background:linear-gradient(180deg,#222 0,#000 220px);padding:4px 16px 48px;font-family:'Inter',Arial,sans-serif}   /* продовжує сірий фон заголовка без стику */
@media screen and (max-width:639px){#oks-st{display:block}#rec1575166851.t-rec{display:none!important}}
#oks-st .st-card{border-radius:20px;border:1px solid #222;background:#000;padding:20px 18px 18px;margin-bottom:12px}
#oks-st .st-top{display:flex;align-items:baseline;justify-content:space-between;gap:12px;
  padding-bottom:12px;margin-bottom:16px;border-bottom:1px solid rgba(255,255,255,.12)}
#oks-st .st-n{color:#fff;font-size:30px;font-weight:700;line-height:1;letter-spacing:-.5px;white-space:nowrap}
#oks-st .st-t{color:#fff;font-size:14px;line-height:1.25;text-align:right}
#oks-st .st-h{color:#fff;font-size:13px;font-weight:700;text-transform:uppercase;margin-bottom:8px}
#oks-st .st-h::before{content:"✺";color:#f6d4aa;margin-right:8px}
#oks-st .st-d{color:#d2d2d2;font-size:14px;line-height:1.4;margin-bottom:16px}
#oks-st .st-r{background:#f6d4aa;border-radius:10px;padding:14px 16px}
#oks-st .st-rh{color:#6b5a45;font-size:12px;font-weight:800;text-transform:uppercase;margin-bottom:6px}
#oks-st .st-rt{color:#000;font-size:14px;font-weight:600;line-height:1.35}
"""


def _txt(s, eid, keep_br=False):
    a = s.find('<div id="rec1558035631"')
    m = re.search(r"field='tn_text_%s'>(.*?)</(?:div|h[1-6])>" % eid, s[a:], re.S)
    assert a > 0 and m, 'stages_m: нема тексту %s' % eid
    t = m.group(1)
    t = re.sub(r'<br\s*/?>', ' ', t)
    return re.sub(r'\s+', ' ', re.sub(r'<(?!/?(?:b|strong|em|i)\b)[^>]+>', '', t)).strip()


def html(s):
    cards = ''.join('<div class="st-card"><div class="st-top"><div class="st-n">%s</div><div class="st-t">%s</div></div>'
                    '<div class="st-h">Що робимо:</div><div class="st-d">%s</div>'
                    '<div class="st-r"><div class="st-rh">Результат:</div><div class="st-rt">%s</div></div></div>'
                    % tuple(_txt(s, e) for e in st) for st in STAGES)
    return '<div id="oks-st"><div class="oks-in">%s</div></div>' % cards
