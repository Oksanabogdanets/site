"""Блок форматів роботи — чотири пакети з наростанням.

Замінює дві Tilda-копії блоку (rec1558101811 і rec1575209271): у них було три картки
по 376px, четверта в ряд не влазила, а пункт «Підбір локації…» дублювався.
Тут один список пунктів на всі картки: що входить — золота галочка, що ні —
закреслено червоним. Правити = міняти ITEMS і PACKAGES.
"""

# Порядок пунктів однаковий у всіх картках — так видно, що саме додається у старшому пакеті.
ITEMS = [
    'Індивідуальна стратегія: аналіз конкурентів, ЦА і ринку',
    'Сценарії з хуками, воронками й описами',
    'Супровід по зйомці: образи, стилістика, кадр',
    'Монтаж роликів',
    'Публікація з описом, хештегами й обкладинкою',
    'Підбір локації, організація і курування зйомки',
    'Зйомка з оператором: профкамера, світло, звук',
    'Розбір статистики і супровід',
    'Щотижневі рекомендації за цифрами',
]

# (назва, підзаголовок, скільки перших пунктів входить, обсяг на місяць)
PACKAGES = [
    ('Сценарії', 'Стратегія і сценарії — знімаєте та монтуєте самі', 2, '15 або 30 сценаріїв на місяць'),
    ('Сценарії + супровід + монтаж', 'Пишемо сценарії, ведемо вас на зйомці й монтуємо', 4, '15 або 30 відео на місяць'),
    ('Reels без зйомки', 'Знімаєте самі — монтаж і публікація на нас', 5, '15 або 30 відео на місяць'),
    ('Reels під ключ зі зйомкою', 'Повний цикл: студія, оператор, монтаж, публікація', 9, '15 або 30 відео на місяць'),
]

CSS = """
#oks-pk{background:#000;padding:0 20px 90px;font-family:'Inter',Arial,sans-serif}
#oks-pk .pk-grid{max-width:1280px;margin:0 auto;display:grid;gap:20px;
  grid-template-columns:repeat(4,1fr)}
#oks-pk .pk-card{display:flex;flex-direction:column;border-radius:24px;padding:28px 24px 24px;
  background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);
  border:1px solid rgba(246,212,170,.18)}
#oks-pk .pk-card.is-full{border-color:rgba(246,212,170,.55);
  box-shadow:0 18px 50px rgba(246,212,170,.10)}
/* min-height на шапці — щоб списки в усіх картках починались на одному рівні */
#oks-pk .pk-title{color:#f6d4aa;font-size:19px;font-weight:700;line-height:1.15;
  letter-spacing:.04em;text-transform:uppercase;margin:0;min-height:2.3em}
#oks-pk .pk-sub{color:#9b9b9b;font-size:13px;line-height:1.35;margin:10px 0 14px;
  min-height:2.7em}
#oks-pk .pk-vol{display:inline-block;border:1px solid rgba(246,212,170,.35);border-radius:40px;
  padding:6px 12px;color:#f6d4aa;font-size:12px;margin-bottom:20px}
#oks-pk .pk-list{list-style:none;margin:0 0 24px;padding:0;flex:1}
#oks-pk .pk-list li{position:relative;padding:0 0 14px 26px;margin-bottom:14px;
  border-bottom:1px solid rgba(255,255,255,.07);color:#d2d2d2;font-size:15px;line-height:1.3}
#oks-pk .pk-list li:last-child{border-bottom:0;margin-bottom:0}
#oks-pk .pk-list li::before{position:absolute;left:0;top:0;font-size:15px;line-height:1.3}
#oks-pk .pk-list li.yes::before{content:"✓";color:#f6d4aa}
#oks-pk .pk-list li.no{color:#6a6a6a;text-decoration:line-through;
  text-decoration-color:#e04b4b;text-decoration-thickness:2px}
#oks-pk .pk-list li.no::before{content:"✕";color:#e04b4b;text-decoration:none}
#oks-pk .pk-btn{display:inline-flex;align-items:center;justify-content:center;gap:10px;
  background:#f6d4aa;color:#000;font-size:15px;font-weight:600;text-decoration:none;
  border-radius:40px;padding:14px 22px;transition:transform .15s ease}
#oks-pk .pk-btn:hover{transform:translateY(-2px)}
@media screen and (max-width:1100px){#oks-pk .pk-grid{grid-template-columns:repeat(2,1fr)}}
@media screen and (max-width:640px){#oks-pk{padding-bottom:60px}
  #oks-pk .pk-grid{grid-template-columns:1fr;gap:16px}
  #oks-pk .pk-card{padding:24px 20px 20px}}
"""


def html(link):
    cards = []
    for i, (name, sub, n, vol) in enumerate(PACKAGES):
        lis = ''.join('<li class="%s">%s</li>' % ('yes' if k < n else 'no', t)
                      for k, t in enumerate(ITEMS))
        cards.append(
            '<div class="pk-card%s"><h3 class="pk-title">%s</h3><p class="pk-sub">%s</p>'
            '<span class="pk-vol">%s</span>'
            '<ul class="pk-list">%s</ul><a class="pk-btn" href="%s" target="_blank" '
            'rel="noopener">Обговорити проєкт →</a></div>'
            % (' is-full' if i == len(PACKAGES) - 1 else '', name, sub, vol, lis, link))
    return ('<div id="oks-pk"><div class="pk-grid">%s</div></div>'
            % ''.join(cards))
