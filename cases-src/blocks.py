"""Три невеликі власні блоки (за аналізом конкурента, 14.09):

- essence()  — абзац суті одразу під hero: «послугу надає команда» + вимірюваний обсяг
- results()  — «Що ви отримуєте»: результати окремо від процесу (продає саме це)
- about()    — «Хто веде проєкт»: регалії Оксани замість цифр клієнтів
"""

ESSENCE = ('Послугу надає команда <b>Oksana Bogdanets Production</b>. Робимо під ключ '
           '<b>15 або 30 вертикальних відео на місяць</b>: стратегія, сценарії, зйомка за один день, '
           'монтаж і публікація. Можливий формат без зйомки — знімаєте самі за нашими сценаріями.')

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
#oks-ess,#oks-res,#oks-about{background:#000;font-family:'Inter',Arial,sans-serif}
#oks-ess{padding:0 20px 70px}
#oks-ess p{max-width:860px;margin:0 auto;text-align:center;color:#d2d2d2;font-size:19px;line-height:1.45}
#oks-ess b{color:#f6d4aa;font-weight:600}
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
  .oks-h2{font-size:32px}#oks-about .ab{grid-template-columns:220px 1fr;gap:28px}}
@media screen and (max-width:640px){#oks-ess{padding-bottom:46px}#oks-ess p{font-size:16px}
  #oks-res,#oks-about{padding-bottom:60px}.oks-h2{font-size:26px;margin-bottom:24px}
  #oks-res .rs-grid{grid-template-columns:1fr;gap:14px}
  #oks-about .ab{grid-template-columns:1fr;padding:22px;gap:22px}
  #oks-about .ab-ph{max-width:220px}#oks-about .ab-grid{grid-template-columns:repeat(2,1fr)}}
"""


def essence():
    return '<div id="oks-ess"><p>%s</p></div>' % ESSENCE


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
