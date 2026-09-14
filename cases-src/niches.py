"""Рядок ніш під блоком цифр.

Перелік ніш не вміщався в підпис картки «15+» — текст ліз за її межі.
Тому в картці лишається короткий підпис, а ніші йдуть окремим рядком тегів.
"""

NICHES = ['Юристи', 'Медицина', "Б'юті", 'Психологія', 'Маркетинг',
          'SEO', 'Освіта', 'Рекрутинг', 'Нерухомість', 'Фото та відео']

CSS = """
#oks-niches{background:#000;padding:0 20px 70px;font-family:'Inter',Arial,sans-serif}
#oks-niches .nc-wrap{max-width:1000px;margin:0 auto;display:flex;flex-wrap:wrap;
  justify-content:center;gap:10px}
#oks-niches .nc-tag{border:1px solid rgba(246,212,170,.35);border-radius:40px;
  padding:9px 18px;color:#f6d4aa;font-size:14px;line-height:1;white-space:nowrap}
@media screen and (max-width:640px){#oks-niches{padding-bottom:46px}
  #oks-niches .nc-wrap{gap:8px}
  #oks-niches .nc-tag{padding:8px 14px;font-size:13px}}
"""


def html():
    tags = ''.join('<span class="nc-tag">%s</span>' % n for n in NICHES)
    return '<div id="oks-niches"><div class="nc-wrap">%s</div></div>' % tags
