"""Блок «Команда» — п'ять людей замість чотирьох Tilda-карток (rec1558093791).

Фото — файли в assets/ (888x888, як ava_oksana.jpg). Поки фото немає —
на місці стоїть коло з ініціалом. Правити = міняти PEOPLE.
"""

# (ім'я, роль, файл фото в assets або None, опис або None)
# 29.09 Оксана: фото й описи з профілів, АЛЕ без прізвищ, ніків, посилань і будь-яких зачіпок —
# клієнти не мають знати, хто знімає, і писати операторам напряму. Опис — лише що людина робить.
PEOPLE = [
    ('Оксана', 'Засновниця, продюсерка', 'oksana_team.jpg', 'Стратегія і сценарії кожного проєкту'),   # нове фото 29.09
    ('Олександра', 'Відеографка, режисерка монтажу', 'tm_oleksandra.jpg', 'Знімає Reels для експертів і брендів, веде монтаж'),
    ('Анастасія', 'Відеографка, фотографка', 'tm_anastasia.jpg', 'Контент для бізнесу, експертів і особистих брендів'),
    ('Данило', 'Кінорежисер, оператор', 'tm_danylo.jpg', 'Знімає, пише й монтує: кіно, репортажі, кліпи'),
    ('Валерія', 'SMM-спеціалістка', None, None),
]

# Партнери — окремий розділ (Оксана 03.10: методологиня «не хоче бути просто в команді»). Instagram НЕ показуємо.
PARTNERS = [
    ('Анастасія', 'Методологиня, таргетологиня', None, 'Методологиня експертних курсів, 2500+ учнів. Налаштовує таргетовану рекламу'),   # 03.10: «таргетолог вона ще»
]

LEAD = 'Кожен проєкт — від стратегії до фінального монтажу — ведеться під керівництвом Оксани.'

CSS = """
#oks-team{background:#000;padding:0 20px 90px;font-family:'Inter',Arial,sans-serif}
#oks-team .tm-in{max-width:1180px;margin:0 auto}
#oks-team .tm-tag{display:inline-block;border:1px solid rgba(246,212,170,.4);border-radius:40px;
  padding:7px 16px;color:#f6d4aa;font-size:13px;margin-bottom:22px}
#oks-team h2{color:#fff;font-size:40px;font-weight:600;line-height:1.1;margin:0 0 40px;max-width:640px}
#oks-team h2 b{color:#f6d4aa;font-weight:600}
#oks-team .tm-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:18px}
#oks-team .tm-card{text-align:center}
#oks-team .tm-ph{width:100%;aspect-ratio:1/1;border-radius:24px;overflow:hidden;
  background:linear-gradient(160deg,#241a12,#0d0a08);border:1px solid rgba(246,212,170,.18);
  display:flex;align-items:center;justify-content:center}
#oks-team .tm-ph img{width:100%;height:100%;object-fit:cover;display:block}
#oks-team .tm-ph span{color:#f6d4aa;font-size:56px;font-weight:600}
#oks-team .tm-name{color:#fff;font-size:18px;font-weight:600;margin:16px 0 4px}
#oks-team .tm-role{color:#f6d4aa;font-size:12.5px;line-height:1.3}
#oks-team .tm-desc{color:#9b9b9b;font-size:12.5px;line-height:1.35;margin-top:6px}
#oks-team .tm-lead{margin:40px auto 0;max-width:720px;text-align:center;color:#d2d2d2;
  font-size:17px;line-height:1.4;padding:22px 26px;border-radius:18px;
  border:1px solid rgba(246,212,170,.3);background:rgba(246,212,170,.05)}
#oks-team .tm-lead b{color:#f6d4aa;font-weight:600}
@media screen and (max-width:1000px){#oks-team .tm-grid{display:flex;gap:14px;overflow-x:auto;scroll-snap-type:x mandatory;
    -webkit-overflow-scrolling:touch;scrollbar-width:none;margin:0 -20px;padding:0 20px 6px;scroll-padding:0 20px}
  #oks-team .tm-grid::-webkit-scrollbar{display:none}
  #oks-team .tm-card{flex:0 0 26%;scroll-snap-align:start}
  #oks-team h2{font-size:32px}}
@media screen and (max-width:640px){#oks-team{padding-bottom:60px}
  #oks-team .tm-grid{margin:0 -20px;padding:0 20px 6px;scroll-padding:0 20px}
  #oks-team .tm-card{flex:0 0 42%}
  #oks-team h2{font-size:26px;margin-bottom:26px}
  #oks-team .tm-ph span{font-size:40px}
  #oks-team .tm-lead{font-size:15px;padding:18px}}
#oks-partners{background:#000;padding:0 20px 90px;font-family:'Inter',Arial,sans-serif}
#oks-partners .pt-in{max-width:1180px;margin:0 auto}
#oks-partners .pt-tag{display:inline-block;border:1px solid rgba(246,212,170,.4);border-radius:40px;
  padding:7px 16px;color:#f6d4aa;font-size:13px;margin-bottom:22px}
#oks-partners h2{color:#fff;font-size:40px;font-weight:600;line-height:1.1;margin:0 0 40px}
#oks-partners h2 b{color:#f6d4aa;font-weight:600}
#oks-partners .pt-grid{display:flex;flex-wrap:wrap;gap:18px}
#oks-partners .pt-card{display:flex;align-items:center;gap:22px;flex:0 1 520px;padding:22px;border-radius:24px;
  background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);border:1px solid rgba(246,212,170,.3)}
#oks-partners .pt-ph{flex:0 0 120px;height:120px;border-radius:20px;overflow:hidden;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(160deg,#241a12,#0d0a08);border:1px solid rgba(246,212,170,.18)}
#oks-partners .pt-ph img{width:100%;height:100%;object-fit:cover;display:block}
#oks-partners .pt-ph span{color:#f6d4aa;font-size:48px;font-weight:600}
#oks-partners .pt-name{color:#fff;font-size:22px;font-weight:600}
#oks-partners .pt-role{color:#f6d4aa;font-size:14px;margin-top:4px}
#oks-partners .pt-desc{color:#b5b5b5;font-size:15px;line-height:1.4;margin-top:10px}
@media screen and (max-width:640px){#oks-partners{padding-bottom:60px}#oks-partners h2{font-size:26px;margin-bottom:26px}
  #oks-partners .pt-card{gap:16px;padding:16px}#oks-partners .pt-ph{flex-basis:88px;height:88px}#oks-partners .pt-ph span{font-size:36px}
  #oks-partners .pt-name{font-size:19px}#oks-partners .pt-desc{font-size:14px}}
"""


def html(photo_url):
    """photo_url(filename) -> шлях картинки у зібраному сайті (img/...)."""
    cards = []
    for name, role, photo, desc in PEOPLE:
        inner = ('<img src="%s" alt="%s">' % (photo_url(photo), name) if photo
                 else '<span>%s</span>' % name[0])
        cards.append('<div class="tm-card"><div class="tm-ph">%s</div>'
                     '<div class="tm-name">%s</div><div class="tm-role">%s</div>%s</div>'
                     % (inner, name, role, '<div class="tm-desc">%s</div>' % desc if desc else ''))
    lead = LEAD.replace('під керівництвом Оксани', '<b>під керівництвом Оксани</b>')
    return ('<div id="oks-team"><div class="tm-in"><span class="tm-tag">Команда</span>'
            '<h2>Команда з досвідом роботи в <b>20+ нішах</b></h2>'
            '<div class="tm-grid">%s</div><div class="tm-lead">%s</div></div></div>'
            % (''.join(cards), lead))


def partners_html(photo_url):
    """Розділ «Партнери» (id="partners" — пункт меню)."""
    cards = []
    for name, role, photo, desc in PARTNERS:
        inner = ('<img src="%s" alt="%s" loading="lazy">' % (photo_url(photo), name) if photo
                 else '<span>%s</span>' % name[0])
        cards.append('<div class="pt-card"><div class="pt-ph">%s</div><div><div class="pt-name">%s</div>'
                     '<div class="pt-role">%s</div>%s</div></div>'
                     % (inner, name, role, '<div class="pt-desc">%s</div>' % desc if desc else ''))
    return ('<section id="partners"><div id="oks-partners"><div class="pt-in"><span class="pt-tag">Партнери</span>'
            '<h2>Наші <b>партнери</b></h2><div class="pt-grid">%s</div></div></div></section>' % ''.join(cards))
