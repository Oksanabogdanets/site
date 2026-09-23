"""Блок «Команда» — п'ять людей замість чотирьох Tilda-карток (rec1558093791).

Фото — файли в assets/ (888x888, як ava_oksana.jpg). Поки фото немає —
на місці стоїть коло з ініціалом. Правити = міняти PEOPLE.
"""

# (ім'я, роль, файл фото в assets або None)
PEOPLE = [
    ('Оксана', 'Засновниця, продюсерка', 'ava_oksana.jpg'),
    ('Олександра', 'Операторка і монтажерка', None),
    ('Анастасія', 'Операторка', None),
    ('Данило', 'Оператор', None),
    ('Валерія', 'SMM-спеціалістка', None),
    ('Анастасія', 'Методологиня', None),
    ('Анастасія', 'Таргетологиня', None),
]

LEAD = 'Кожен проєкт — від стратегії до фінального монтажу — ведеться під керівництвом Оксани.'

CSS = """
#oks-team{background:#000;padding:0 20px 90px;font-family:'Inter',Arial,sans-serif}
#oks-team .tm-in{max-width:1180px;margin:0 auto}
#oks-team .tm-tag{display:inline-block;border:1px solid rgba(246,212,170,.4);border-radius:40px;
  padding:7px 16px;color:#f6d4aa;font-size:13px;margin-bottom:22px}
#oks-team h2{color:#fff;font-size:40px;font-weight:600;line-height:1.1;margin:0 0 40px;max-width:640px}
#oks-team h2 b{color:#f6d4aa;font-weight:600}
#oks-team .tm-grid{display:grid;grid-template-columns:repeat(7,1fr);gap:18px}
#oks-team .tm-card{text-align:center}
#oks-team .tm-ph{width:100%;aspect-ratio:1/1;border-radius:24px;overflow:hidden;
  background:linear-gradient(160deg,#241a12,#0d0a08);border:1px solid rgba(246,212,170,.18);
  display:flex;align-items:center;justify-content:center}
#oks-team .tm-ph img{width:100%;height:100%;object-fit:cover;display:block}
#oks-team .tm-ph span{color:#f6d4aa;font-size:56px;font-weight:600}
#oks-team .tm-name{color:#fff;font-size:18px;font-weight:600;margin:16px 0 4px}
#oks-team .tm-role{color:#9b9b9b;font-size:13px;line-height:1.35}
#oks-team .tm-lead{margin:40px auto 0;max-width:720px;text-align:center;color:#d2d2d2;
  font-size:17px;line-height:1.4;padding:22px 26px;border-radius:18px;
  border:1px solid rgba(246,212,170,.3);background:rgba(246,212,170,.05)}
#oks-team .tm-lead b{color:#f6d4aa;font-weight:600}
@media screen and (max-width:1000px){#oks-team .tm-grid{grid-template-columns:repeat(4,1fr)}
  #oks-team h2{font-size:32px}}
@media screen and (max-width:640px){#oks-team{padding-bottom:60px}
  #oks-team .tm-grid{grid-template-columns:repeat(2,1fr);gap:14px}
  #oks-team h2{font-size:26px;margin-bottom:26px}
  #oks-team .tm-ph span{font-size:40px}
  #oks-team .tm-lead{font-size:15px;padding:18px}}
"""


def html(photo_url):
    """photo_url(filename) -> шлях картинки у зібраному сайті (img/...)."""
    cards = []
    for name, role, photo in PEOPLE:
        inner = ('<img src="%s" alt="%s">' % (photo_url(photo), name) if photo
                 else '<span>%s</span>' % name[0])
        cards.append('<div class="tm-card"><div class="tm-ph">%s</div>'
                     '<div class="tm-name">%s</div><div class="tm-role">%s</div></div>'
                     % (inner, name, role))
    lead = LEAD.replace('під керівництвом Оксани', '<b>під керівництвом Оксани</b>')
    return ('<div id="oks-team"><div class="tm-in"><span class="tm-tag">Команда</span>'
            '<h2>Команда з досвідом роботи в <b>20+ нішах</b></h2>'
            '<div class="tm-grid">%s</div><div class="tm-lead">%s</div></div></div>'
            % (''.join(cards), lead))
