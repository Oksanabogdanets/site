"""Три невеликі власні блоки (за аналізом конкурента, 14.09):

- mission()  — «Наша місія» одразу під hero: теза + три пункти + фінальна фраза (редакція Оксани з КП, 16.09;
               замінив абзац «Послугу надає команда…», який Оксана попросила прибрати)
- results()  — «Що ви отримуєте»: результати окремо від процесу (продає саме це)
- about()    — «Хто веде проєкт»: регалії Оксани замість цифр клієнтів
"""

MISSION = 'Ми масштабуємо <b>таланти, бізнеси та професіоналів</b>'
MISSION_POINTS = [
    ('Розуміємо болі вашої аудиторії',
     'Глибоко розуміємо, що болить вашій аудиторії, і транслюємо рішення через контент — '
     'завдяки цьому ви отримуєте цільові заявки'),
    ('Розвиваємо бренди',
     'Через творчий, сучасний і стратегічний контент'),
    ('Створюємо якісні та продаючі Reels',
     'Вони працюють на особистий бренд і збільшують потік клієнтів'),
]
MISSION_FINAL = 'Ми не закриваємо контент-план — <b>ми закриваємо ваші цілі</b>.'

RESULTS = [
    ('Системний потік заявок', 'Reels ведуть у Direct і на сайт, а не просто збирають перегляди'),
    ('Зростання підписників', 'Цільова аудиторія, яка приходить із роликів і лишається'),
    ('Впізнаваність і особистий бренд', 'Вас починають упізнавати в ніші і радити'),
    ('Зростання продажів', 'Більше брендових запитів — клієнти приходять уже теплими'),
]

REGALIA = [
    ('3 роки', 'у Reels-продакшні'),
    ('15+', 'ніш у роботі'),
    ('10+', 'роликів із 100 тис.+ переглядів'),
    ('4', 'ролики-мільйонники'),
]
ABOUT_TEXT = ('Продюсерка. Веде кожен проєкт особисто — від стратегічної сесії до фінального монтажу. '
              'Стратегію і сценарії не делегує: це те, що вирішує результат.')

CSS = """
#oks-mission,#oks-res,#oks-about{background:#000;font-family:'Inter',Arial,sans-serif}
#oks-mission{padding:10px 20px 90px}
#oks-mission .oks-h2{max-width:820px}
#oks-mission .ms-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
#oks-mission .ms-card{border-radius:24px;padding:26px 24px 28px;
  background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);border:1px solid rgba(246,212,170,.18)}
#oks-mission .ms-n{color:#f6d4aa;font-size:13px;letter-spacing:.08em;margin-bottom:14px}
#oks-mission .ms-t{color:#fff;font-size:20px;font-weight:600;line-height:1.2;margin-bottom:10px}
#oks-mission .ms-d{color:#9b9b9b;font-size:15px;line-height:1.4}
#oks-mission .ms-final{margin:34px auto 0;max-width:720px;text-align:center;color:#d2d2d2;
  font-size:21px;line-height:1.35;padding:22px 26px;border-radius:18px;
  border:1px solid rgba(246,212,170,.3);background:rgba(246,212,170,.05)}
#oks-mission .ms-final b{color:#f6d4aa;font-weight:600}
#oks-res{padding:0 20px 90px}
.oks-in{max-width:1180px;margin:0 auto}
.oks-tag{display:inline-block;border:1px solid rgba(246,212,170,.4);border-radius:40px;
  padding:7px 16px;color:#f6d4aa;font-size:13px;margin-bottom:22px}
.oks-h2{color:#fff;font-size:40px;font-weight:600;line-height:1.1;margin:0 0 36px;max-width:720px}
.oks-h2 b{color:#f6d4aa;font-weight:600}
#oks-res .rs-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
#oks-res .rs-card{border-radius:24px;padding:26px 24px 28px;
  background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);border:1px solid rgba(246,212,170,.18)}
#oks-res .rs-n{color:#f6d4aa;font-size:13px;letter-spacing:.08em;margin-bottom:14px}
#oks-res .rs-t{color:#fff;font-size:20px;font-weight:600;line-height:1.2;margin-bottom:10px}
#oks-res .rs-d{color:#9b9b9b;font-size:14px;line-height:1.4}
#oks-about{padding:0 20px 90px}
#oks-about .ab{display:grid;grid-template-columns:300px 1fr;gap:40px;align-items:center;
  border-radius:28px;padding:34px;background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);
  border:1px solid rgba(246,212,170,.25)}
#oks-about .ab-ph{width:100%;aspect-ratio:1/1;border-radius:22px;overflow:hidden}
#oks-about .ab-ph img{width:100%;height:100%;object-fit:cover;display:block}
#oks-about .ab-name{color:#fff;font-size:30px;font-weight:600;margin:0 0 6px}
#oks-about .ab-role{color:#f6d4aa;font-size:14px;margin-bottom:16px}
#oks-about .ab-text{color:#d2d2d2;font-size:16px;line-height:1.45;margin-bottom:24px;max-width:600px}
#oks-about .ab-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
#oks-about .ab-num{color:#f6d4aa;font-size:30px;font-weight:600;line-height:1}
#oks-about .ab-lbl{color:#9b9b9b;font-size:13px;line-height:1.3;margin-top:6px}
@media screen and (max-width:1000px){#oks-res .rs-grid{grid-template-columns:repeat(2,1fr)}
  .oks-h2{font-size:32px}#oks-about .ab{grid-template-columns:220px 1fr;gap:28px}
  #oks-mission .ms-grid{grid-template-columns:1fr;gap:14px}}
@media screen and (max-width:640px){#oks-mission{padding-bottom:60px}
  #oks-mission .ms-final{font-size:17px;padding:18px 20px;margin-top:24px}
  #oks-res,#oks-about{padding-bottom:60px}.oks-h2{font-size:26px;margin-bottom:24px}
  #oks-res .rs-grid{grid-template-columns:1fr;gap:14px}
  #oks-about .ab{grid-template-columns:1fr;padding:22px;gap:22px}
  #oks-about .ab-ph{max-width:220px}#oks-about .ab-grid{grid-template-columns:repeat(2,1fr)}}
"""


def mission():
    cards = ''.join('<div class="ms-card"><div class="ms-n">0%d</div><div class="ms-t">%s</div>'
                    '<div class="ms-d">%s</div></div>' % (i, t, d) for i, (t, d) in enumerate(MISSION_POINTS, 1))
    return ('<div id="oks-mission"><div class="oks-in"><span class="oks-tag">Наша місія</span>'
            '<h2 class="oks-h2">%s</h2><div class="ms-grid">%s</div><p class="ms-final">%s</p></div></div>'
            % (MISSION, cards, MISSION_FINAL))


def results():
    cards = ''.join('<div class="rs-card"><div class="rs-n">0%d</div><div class="rs-t">%s</div>'
                    '<div class="rs-d">%s</div></div>' % (i, t, d) for i, (t, d) in enumerate(RESULTS, 1))
    return ('<div id="oks-res"><div class="oks-in"><span class="oks-tag">Результати</span>'
            '<h2 class="oks-h2">Що ви <b>отримуєте</b></h2><div class="rs-grid">%s</div></div></div>' % cards)


def about(photo_url):
    stats = ''.join('<div><div class="ab-num">%s</div><div class="ab-lbl">%s</div></div>' % (n, l)
                    for n, l in REGALIA)
    return ('<div id="oks-about"><div class="oks-in"><span class="oks-tag">Хто веде проєкт</span>'
            '<div class="ab"><div class="ab-ph"><img src="%s" alt="Оксана Богданець"></div>'
            '<div><h3 class="ab-name">Оксана Богданець</h3><div class="ab-role">Засновниця, продюсерка</div>'
            '<p class="ab-text">%s</p><div class="ab-grid">%s</div></div></div></div></div>'
            % (photo_url, ABOUT_TEXT, stats))
