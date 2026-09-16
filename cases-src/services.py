"""Три блоки перед пакетами (за КП Оксани, 16.09):

- skills()  — «Що ми вміємо?»: Reels під ключ / TikTok / просування + воронки
- process() — «Ведення Reels і TikTok під ключ»: десять етапів + хто працює над проєктом
- start()   — «Що потрібно для старту?»: Zoom-зустріч → бриф → договір

Оксана: спочатку розписати, що вміємо і як ведемо проєкт, і лише потім — які є пакети.
Правити = міняти SKILLS / STEPS / ROLES / START.
"""

SKILLS = [
    ('Reels-просування під ключ', 'Для експертів, підприємців і компаній'),
    ('TikTok-просування', 'Відео, які набирають від 100 тис. переглядів, працюють на впізнаваність бренду '
                          'та збільшення клієнтів'),
    ('Просування + воронки', 'Монетизація контенту, залученість клієнтів, структурно побудовані воронки продажів'),
]

STEPS = ['Діагностика', 'Стратегічна сесія', 'Аналіз конкурентів', 'Аналіз ринку', 'Аналіз продукту',
         'Контент-стратегія', 'Сценарії', 'Зйомка', 'Монтаж', 'Щотижнева аналітика']

ROLES = ['продюсер', 'маркетолог', 'сценарист', 'оператор', 'монтажер', 'SMM-спеціаліст']

START = [
    ('Zoom-зустріч', 'Знайомимось, розбираємо вашу нішу і формат — 20 хвилин'),
    ('Бриф', 'Заповнюєте бриф — ми готуємо діагностику і стратегічну сесію'),
    ('Договір', 'Підписуємо договір — і команда стартує'),
]

CSS = """
#oks-skills,#oks-process,#oks-start{background:#000;padding:0 20px 90px;font-family:'Inter',Arial,sans-serif}
#oks-skills .sk-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
#oks-skills .sk-card{border-radius:24px;padding:28px 24px 30px;
  background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);border:1px solid rgba(246,212,170,.18)}
#oks-skills .sk-n{color:#f6d4aa;font-size:13px;letter-spacing:.08em;margin-bottom:14px}
#oks-skills .sk-t{color:#fff;font-size:22px;font-weight:600;line-height:1.15;margin-bottom:10px}
#oks-skills .sk-d{color:#9b9b9b;font-size:15px;line-height:1.4}
#oks-process .pr-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:14px}
#oks-process .pr-step{position:relative;border-radius:18px;padding:18px 16px 18px;
  background:#0a0a0a;border:1px solid rgba(255,255,255,.08)}
#oks-process .pr-n{color:#f6d4aa;font-size:12px;letter-spacing:.08em;margin-bottom:8px}
#oks-process .pr-t{color:#fff;font-size:16px;font-weight:600;line-height:1.2}
#oks-process .pr-roles{margin:28px 0 0;color:#d2d2d2;font-size:17px;line-height:1.45;padding:20px 24px;
  border-radius:18px;border:1px solid rgba(246,212,170,.3);background:rgba(246,212,170,.05)}
#oks-process .pr-roles b{color:#f6d4aa;font-weight:600}
#oks-start .st-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
#oks-start .st-card{display:flex;gap:18px;align-items:flex-start;border-radius:24px;padding:26px 24px;
  background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);border:1px solid rgba(246,212,170,.18)}
#oks-start .st-num{flex:none;width:44px;height:44px;border-radius:50%;background:#f6d4aa;color:#000;
  font-size:18px;font-weight:700;display:flex;align-items:center;justify-content:center}
#oks-start .st-t{color:#fff;font-size:20px;font-weight:600;line-height:1.2;margin-bottom:8px}
#oks-start .st-d{color:#9b9b9b;font-size:14px;line-height:1.4}
@media screen and (max-width:1000px){#oks-skills .sk-grid,#oks-start .st-grid{grid-template-columns:1fr;gap:14px}
  #oks-process .pr-grid{grid-template-columns:repeat(2,1fr);gap:10px}}
@media screen and (max-width:640px){#oks-skills,#oks-process,#oks-start{padding-bottom:60px}
  #oks-skills .sk-card{padding:22px 20px 24px}#oks-skills .sk-t{font-size:19px}
  #oks-process .pr-step{padding:14px 14px}#oks-process .pr-t{font-size:14px}
  #oks-process .pr-roles{font-size:15px;padding:16px 18px;margin-top:20px}
  #oks-start .st-card{padding:20px 18px;gap:14px}#oks-start .st-t{font-size:18px}}
"""


def skills():
    cards = ''.join('<div class="sk-card"><div class="sk-n">0%d</div><div class="sk-t">%s</div>'
                    '<div class="sk-d">%s</div></div>' % (i, t, d) for i, (t, d) in enumerate(SKILLS, 1))
    return ('<div id="oks-skills"><div class="oks-in"><span class="oks-tag">Послуги</span>'
            '<h2 class="oks-h2">Що ми <b>вміємо</b>?</h2><div class="sk-grid">%s</div></div></div>' % cards)


def process():
    steps = ''.join('<div class="pr-step"><div class="pr-n">%02d</div><div class="pr-t">%s</div></div>'
                    % (i, t) for i, t in enumerate(STEPS, 1))
    roles = ', '.join(ROLES)
    return ('<div id="oks-process"><div class="oks-in"><span class="oks-tag">Як працюємо</span>'
            '<h2 class="oks-h2">Ведення Reels і TikTok <b>під ключ</b></h2><div class="pr-grid">%s</div>'
            '<p class="pr-roles">Над проєктом працює команда: <b>%s</b>. '
            'Стратегію і сценарії курує Оксана особисто.</p></div></div>' % (steps, roles))


def start():
    cards = ''.join('<div class="st-card"><div class="st-num">%d</div><div><div class="st-t">%s</div>'
                    '<div class="st-d">%s</div></div></div>' % (i, t, d) for i, (t, d) in enumerate(START, 1))
    return ('<div id="oks-start"><div class="oks-in"><span class="oks-tag">Старт</span>'
            '<h2 class="oks-h2">Що потрібно <b>для старту</b>?</h2><div class="st-grid">%s</div></div></div>' % cards)
