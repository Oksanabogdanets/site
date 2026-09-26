"""«Для кого» на телефоні (≤639px).

Tilda-блок rec1556224301 (і його мобільні копії rec1571157661 — заголовок, rec1571158361 — картки) на 360/480 показує лише першу
картку: решта три стоять за межами артборду (left 399/823/1255), а горизонтальної прокрутки
в артборда нема (Оксана 26.09: «щоб у мобільній версії був структурований сайт»).
Тому на телефоні Tilda-блок ховаємо і показуємо цей: заголовок + фото + 4 картки у стовпчик.
На десктопі лишається Tilda. Тексти й іконки беремо з самого Tilda-блоку (html(s)), щоб не дублювати.
"""
import re

# (іконка, заголовок, підзаголовок, підпис) — id елементів Tilda-блоку rec1556224301
CARDS = [('1763111044188', '1763047549768', '1763047549771', '1763047549777'),
         ('1763111250511', '1763047549795', '1763047549796', '1763047549803'),
         ('1763111144115', '1763047549830', '1763047549833', '1763047549839'),
         ('176312696550625290', '176312696551532080', '176312696553695930', '176312696555815890')]
PHOTO = '1763373226918'

CSS = """
#oks-fw{display:none;background:#000;padding:56px 16px 40px;font-family:'Inter',Arial,sans-serif}
@media screen and (max-width:639px){#oks-fw{display:block}#rec1556224301.t-rec,#rec1571157661.t-rec,#rec1571158361.t-rec{display:none!important}}
#oks-fw .fw-head{text-align:center;margin-bottom:22px}
#oks-fw .fw-head .oks-tag{margin-bottom:16px}
#oks-fw h2{color:#fff;font-size:28px;font-weight:700;line-height:1.1;margin:0;letter-spacing:-.5px}
#oks-fw h2 b{color:#f6d4aa;font-weight:700}
#oks-fw .fw-ph{border-radius:20px;overflow:hidden;margin:0 0 14px;aspect-ratio:4/3;background:#111}
#oks-fw .fw-ph img{width:100%;height:100%;object-fit:cover;object-position:76% 50%;display:block}
#oks-fw .fw-card{border-radius:22px;padding:22px 18px 18px;margin-bottom:12px;background:#000;
  border:1px solid rgba(255,255,255,.14);text-align:center}
#oks-fw .fw-ic{width:40px;height:40px;margin:0 auto 12px;display:block}
#oks-fw .fw-t{color:#fff;font-size:19px;font-weight:600;line-height:1.2;margin-bottom:8px}
#oks-fw .fw-d{color:#9b9b9b;font-size:14px;line-height:1.4;padding-bottom:12px;margin-bottom:12px;
  border-bottom:1px solid rgba(246,212,170,.35)}
#oks-fw .fw-c{color:#fff;font-size:11px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;line-height:1.35}
#oks-fw .fw-c::before{content:"✦";display:block;color:#f6d4aa;font-size:14px;margin-bottom:6px}
"""


def _txt(s, eid):
    m = re.search(r"field='tn_text_%s'>(.*?)</(?:div|h[1-6])>" % eid, s, re.S)
    assert m, 'forwhom: нема тексту %s' % eid
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', m.group(1))).strip()


def _img(s, eid):
    i = s.find("data-elem-id='%s'" % eid)
    m = re.search(r"(img/[\w-]+\.(?:svg|png|jpg))", s[i:i + 2500])
    assert i > 0 and m, 'forwhom: нема картинки %s' % eid
    return m.group(1)


def html(s):
    cards = ''.join('<div class="fw-card"><img class="fw-ic" src="%s" alt=""><div class="fw-t">%s</div>'
                    '<div class="fw-d">%s</div><div class="fw-c">%s</div></div>'
                    % (_img(s, ic), _txt(s, t), _txt(s, d), _txt(s, c)) for ic, t, d, c in CARDS)
    return ('<div id="oks-fw"><div class="oks-in"><div class="fw-head"><span class="oks-tag">Для кого</span>'
            '<h2>Вам потрібен <b>Reels Producer</b>, якщо</h2></div>'
            '<div class="fw-ph"><img src="%s" alt="Оксана Богданець" loading="lazy"></div>%s</div></div>'
            % (_img(s, PHOTO), cards))
