"""Відгук на телефоні (≤639px).

Колаж assets/chats.jpg (1680×461) у Tilda-елементі стоїть 587px завширшки на 360px екрані —
аватар-кружечок і половина тексту за краєм (Оксана 26.09: «некоректно взятий кружечок»),
а вписаний у 330px він нечитабельний. Тому на телефоні Tilda-блок rec1558070821 (мобільна копія — rec1575196761) ховаємо
і показуємо ті самі повідомлення як бульбашки Telegram (темна тема) + аватар зі скріна.
На десктопі лишається скрін. Правити = міняти REVIEWS.
"""

REVIEWS = [dict(name='Olha Bodrova', ava='ava_olha.png',
                msgs=[('Вітаю.', '14:36'),
                      ('Дуже мені подобається. ❤️<br><br>Є пару питань по помилках в титрах. Розпишу. '
                       'А так дуже кльово і жваво', '14:37')])]

CSS = """
#oks-rvm{display:none;background:#000;padding:12px 16px 60px;font-family:'Inter',Arial,sans-serif}
@media screen and (max-width:639px){#oks-rvm{display:block}#rec1558070821.t-rec,#rec1575196761.t-rec{display:none!important}}
#oks-rvm .rvm-chat{position:relative;background:#0e1621;border-radius:22px;padding:16px 14px 16px 56px;
  border:1px solid rgba(255,255,255,.08)}
#oks-rvm .rvm-ava{position:absolute;left:12px;bottom:16px;width:34px;height:34px;border-radius:50%}
#oks-rvm .rvm-b{position:relative;background:#182533;color:#fff;font-size:15px;line-height:1.35;
  border-radius:16px 16px 16px 4px;padding:8px 54px 8px 12px;margin-bottom:6px}
#oks-rvm .rvm-b:last-child{margin-bottom:0}
#oks-rvm .rvm-n{color:#5eb5f7;font-weight:600;font-size:14px;margin-bottom:2px}
#oks-rvm .rvm-t{position:absolute;right:11px;bottom:6px;color:#7d8b99;font-size:11px}
#oks-rvm .rvm-re{display:inline-block;margin-top:8px;background:#233446;border-radius:14px;padding:3px 9px;font-size:13px}
"""


def html(asset_url):
    out = ''
    for r in REVIEWS:
        bubbles = ''
        for i, (t, tm) in enumerate(r['msgs']):
            name = '<div class="rvm-n">%s</div>' % r['name'] if i == 0 else ''
            re_ = '<div><span class="rvm-re">❤️</span></div>' if i == len(r['msgs']) - 1 else ''
            bubbles += '<div class="rvm-b">%s%s%s<span class="rvm-t">%s</span></div>' % (name, t, re_, tm)
        out += '<div class="rvm-chat"><img class="rvm-ava" src="%s" alt="">%s</div>' % (asset_url(r['ava']), bubbles)
    return '<div id="oks-rvm"><div class="oks-in">%s</div></div>' % out
