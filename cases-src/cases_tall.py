"""Кейси 03 і 04 — високі картки з «до/після», як 01 і 02 (rec1558030471).

У клоні reels-agency.ru картки 03 і 04 короткі (один скрін, без «до/після»),
через що ряд виглядав криво, а довгі бейджі не влазили в пілюлі. Для кожної
короткої картки клонуємо всі 16 елементів колонки кейса 02, зсуваємо їх у свою
колонку (DOM-атрибути left за res + CSS `left:calc(50% - Npx + Xpx)`),
підставляємо тексти, скріни й ширини, а стару картку прибираємо з DOM.
Кейс 03 — Юлія, кар'єрна консультантка (скріни з Canva, стор. 5–6).
Кейс 04 — Muza Body, клініка естетичної медицини (КП стор. 7, Canva стор. 14).

TikTok у кейсах 01 і 02 (tiktok()): під скріном «після» — стрічка з трьох роликів із цифрами
(Canva стор. 13 і 10), зібрана в один композит (assets/*_after_tt.jpg); картки стають на 239px
вищими (210 на телефоні), ряд 2 сітки і артборд зсуваються на стільки ж.
"""
import re
from extra_cards import _css_rules

REC = 'rec1558030471'
BAR = '1763463084063'          # смужка справа — останній елемент, перед нею вставляємо клони

# елементи кейса 02 у порядку DOM
SRC = ['1763049596437',                                # фон картки 400x535
       '1763049596545', '1763049596546',               # пілюля + текст «КЕЙС 02»
       '1763049596547', '1763049596548',               # пілюля + текст назви
       '1763049596550', '1763049596551',               # пілюля + текст бейджа
       '176311494518411670', '1763115034639',          # пілюля + текст «ДО»
       '1763049596557',                                # скрін ДО 358x141
       '176311536977549140', '176311536976010280',     # пілюля + текст «ПІСЛЯ»
       '1763049596562',                                # скрін ПІСЛЯ 358x156
       '1763049596563', '1763049596565', '1763049596567']   # фон + заголовок + текст результату
T_NUM, T_TITLE, T_BADGE, T_RES, T_TEXT = '1763049596546', '1763049596548', '1763049596551', '1763049596565', '1763049596567'
P_TITLE, P_BADGE = '1763049596547', '1763049596550'
IMG_BEFORE, IMG_AFTER = '1763049596557', '1763049596562'

TARGETS = [
    dict(prefix='8',                                   # кейс 03: колонка 850 (на 360px — 705)
         shift={'': 410, '480': 410, '640': 410, '360': 345},
         old=['1763049596573', '1763049596575', '1763049596576', '1763049596577', '1763049596578',
              '1763049596580', '1763049596581', '1763049596583', '1763049596584', '1763049596586', '1763049596588'],
         text={T_NUM: 'КЕЙС 03', T_TITLE: "КАР'ЄРНИЙ КОНСУЛЬТАНТ", T_BADGE: '+700 ЦІЛЬОВИХ ПІДПИСНИКІВ',
               T_RES: 'РЕЗУЛЬТАТ: +700 ЦІЛЬОВИХ З 10 REELS',
               T_TEXT: 'Набирає групу на менторство. Аудиторія зросла <em>у 7 разів</em>'},
         widen={P_TITLE: {183: 205, 169: 190}, T_TITLE: {198: 205, 154: 180},
                P_BADGE: {187: 240, 166: 215}, T_BADGE: {181: 215}},
         img={IMG_BEFORE: 'julia_before.jpg', IMG_AFTER: 'julia_after.jpg'}),
    dict(prefix='9',                                   # кейс 04: колонка 1260 (на 360px — 1050)
         shift={'': 820, '480': 820, '640': 820, '360': 690},
         old=['176345641403933930', '176345671309114360', '176345671310542740', '176345681060954820',
              '176345681062842360', '1763456356523', '176345643527384350', '176345643529596620',
              '176345657280266780', '176345669173990020', '176345669176222330'],
         text={T_NUM: 'КЕЙС 04', T_TITLE: 'КЛІНІКА ЕСТЕТИЧНОЇ МЕДИЦИНИ', T_BADGE: 'ЗАЯВКИ ЗА 2 ТИЖНІ',
               T_RES: 'РЕЗУЛЬТАТ: СТОРІНКА З 0 ЗА 30 ДНІВ',
               T_TEXT: 'З порожньої сторінки — до перших заявок <strong>через 2 тижні</strong>. '
                       '<em>100% органіка</em>, без витрат на таргет'},
         widen={P_TITLE: {183: 250, 169: 220}, T_TITLE: {198: 230, 154: 200}},
         img={IMG_BEFORE: 'mbody_before.jpg', IMG_AFTER: 'mbody_after.jpg'}),
]
# половина контейнера в CSS calc(50% - Npx + Xpx) -> який res
CSS_RES = {'640': '', '320': '640', '240': '480', '180': '360'}


def _frag(rec, eid):
    a = rec.index("tn-elem__1558030471%s'" % eid)
    a = rec.rfind("<div class='t396__elem", 0, a)
    return a, rec.find("<div class='t396__elem", a + 10)


def _shift_dom(frag, shift):
    def rep(m):
        res = (m.group(1) or '').replace('-res-', '')
        return 'data-field-left%s-value="%d"' % (m.group(1) or '', int(m.group(2)) + shift[res])
    return re.sub(r'data-field-left(-res-\d+)?-value="(-?\d+)"', rep, frag)


def _shift_css(rule, shift):
    def rep(m):
        return 'left:calc(50%% - %spx + %dpx)' % (m.group(1), int(m.group(2)) + shift[CSS_RES[m.group(1)]])
    return re.sub(r'left:calc\(50% - (\d+)px \+ (-?\d+)px\)', rep, rule)


def _widen(txt, widths):
    for old, new in widths.items():
        txt = re.sub(r'(data-field-width(?:-res-\d+)?-value=")%d"' % old, r'\g<1>%d"' % new, txt)
        txt = txt.replace('width:%dpx' % old, 'width:%dpx' % new)
    return txt


def _clone(rec, css, t, asset_url):
    dom, css_add = '', ''
    for eid in SRC:
        nid = t['prefix'] + eid[1:]
        a, b = _frag(rec, eid)
        f = _shift_dom(rec[a:b], t['shift'])
        f = f.replace("tn-elem__1558030471%s'" % eid, "tn-elem__1558030471%s'" % nid)
        f = f.replace("data-elem-id='%s'" % eid, "data-elem-id='%s'" % nid)
        f = f.replace("tn_text_%s'" % eid, "tn_text_%s'" % nid)
        if eid in t['text']:
            f = re.sub(r"(field='tn_text_%s'>).*?(</div>)" % nid,
                       lambda m: m.group(1) + t['text'][eid] + m.group(2), f, count=1, flags=re.S)
        if eid in t['img']:
            f = re.sub(r'data-original="[^"]+"', 'data-original="%s"' % asset_url(t['img'][eid]), f, count=1)
        if eid in t['widen']:
            f = _widen(f, t['widen'][eid])
        dom += f
        for media, rule in _css_rules(css, eid):
            r = _shift_css(rule.replace('data-elem-id="%s"' % eid, 'data-elem-id="%s"' % nid), t['shift'])
            if eid in t['widen']:
                r = _widen(r, t['widen'][eid])
            css_add += (media + r + '}' * media.count('@media')) if media else r
    return dom, css_add


def apply(s, asset_url):
    """asset_url(filename) -> шлях картинки у зібраному сайті (img/...)."""
    rec_a = s.index('<div id="%s"' % REC)
    rec_b = s.find('<div id="rec', rec_a + 10)
    rec = s[rec_a:rec_b]
    st = rec.index('<style>') + 7
    css = rec[st:rec.index('</style>', st)]

    dom_all, css_all = '', ''
    for t in TARGETS:
        dom, css_add = _clone(rec, css, t, asset_url)
        dom_all += dom; css_all += css_add
        for eid in t['old']:                       # прибираємо стару коротку картку
            a, b = _frag(rec, eid)
            rec = rec[:a] + rec[b:]
    a, _ = _frag(rec, BAR)
    rec = rec[:a] + dom_all + rec[a:]
    rec, tt_css = tiktok(rec, asset_url)
    css_all += tt_css
    rec, grid_css = regrid(rec)
    css_all += grid_css

    s = s[:rec_a] + rec + s[rec_b:]
    return s.replace('</head>', '<style>' + css_all + '</style>\n</head>', 1)


# ---------- TikTok-стрічка під «ПІСЛЯ» у кейсах 01 і 02 ----------
TT = [dict(after='1763049596500', bg='176313527876574120',                       # кейс 01, Звільнимо (Canva 13)
           below=['1763049596528', '1763049596531', '1763049596532'], img='zvilnymo_after_tt.jpg',
           url='https://www.tiktok.com/@zvilnymo'),
      dict(after='1763049596562', bg='1763049596437',                              # кейс 02, Ніна (Canva 10)
           below=['1763049596563', '1763049596565', '1763049596567'], img='nina_after_tt.jpg',
           url='https://www.tiktok.com/@nina_demydenko')]
# посилання поверх TikTok-стрічки (нижні 60% картинки «після»): Оксана — «має бути клікабельним»
TT_LINK = ('<a href="%s" target="_blank" rel="noopener" aria-label="TikTok" '
           'style="position:absolute;left:0;right:0;top:40%%;bottom:0;z-index:5;display:block;cursor:pointer"></a>')
TT_H = {'': 395, '360': 328}    # висота скріна «після» з стрічкою (було 156 / 118)
TT_D = {'': 239, '360': 210}    # на стільки нижче все під ним і вища картка


def _tag(frag):
    """Відкривальний тег без '>' (щоб _set міг дописати атрибут) і решта фрагмента."""
    i = frag.index('>')
    return frag[:i], frag[i:]


def _bump(tag, key, res, d):
    a = 'data-field-%s%s-value' % (key, '-res-%s' % res if res else '')
    m = re.search(a + r'="(-?[\d.]+)"', tag)
    return re.sub(a + r'="[^"]*"', '%s="%d"' % (a, int(float(m.group(1))) + d), tag) if m else tag


def tiktok(rec, asset_url):
    css = ''
    for t in TT:
        a, b = _frag(rec, t['after'])
        tag, rest = _tag(rec[a:b])
        rest = re.sub(r'data-original="[^"]+"', 'data-original="%s"' % asset_url(t['img']), rest, count=1)
        j = rest.rfind('</div>'); rest = rest[:j] + TT_LINK % t['url'] + rest[j:]   # перед закриттям .tn-elem
        for res in RES:
            h = TT_H['360'] if res == '360' else TT_H['']
            tag = _set(tag, 'height', res, h)
            r = '#rec1558030471 .tn-elem[data-elem-id="%s"]{height:%dpx!important}' % (t['after'], h)
            css += (MEDIA[res] + '{' + r + '}') if MEDIA[res] else r
        rec = rec[:a] + tag + rest + rec[b:]
        a, b = _frag(rec, t['bg'])
        tag, rest = _tag(rec[a:b])
        for res in RES:
            d = TT_D['360'] if res == '360' else TT_D['']
            tag = _bump(tag, 'height', res, d)
            m = re.search(r'data-field-height%s-value="(\d+)"' % ('-res-%s' % res if res else ''), tag)
            if m:
                r = '#rec1558030471 .tn-elem[data-elem-id="%s"]{height:%spx!important}' % (t['bg'], m.group(1))
                css += (MEDIA[res] + '{' + r + '}') if MEDIA[res] else r
        rec = rec[:a] + tag + rest + rec[b:]
        for eid in t['below']:
            a, b = _frag(rec, eid)
            tag, rest = _tag(rec[a:b])
            for res in RES:
                tag = _bump(tag, 'top', res, TT_D['360'] if res == '360' else TT_D[''])
            rec = rec[:a] + tag + rest + rec[b:]
    return rec, css


# ---------- сітка замість горизонтальної стрічки ----------
# У конкурента 4 картки стоять у ряд із прихованою прокруткою — картки 2–4 видно лише
# якщо тягнути вбік, і Оксана бачила тільки першу. Тому: на десктопі 2×2 по центру,
# на планшеті й телефоні — в один стовпчик. Позиції правимо і в data-атрибутах
# (для JS Tilda), і CSS-перекриттям з !important.
HIDE = ['1763692875647',          # лінія-трек стрічки
        '1763463084063',          # смужка-затемнення справа
        '1763049596554',          # дублікат пілюлі «ДО» кейса 02 (на мобільному стоїть збоку)
        '1763691776527']          # прозора плашка 430x100 кейса 02
HIDE_MOBILE = ['1763049596501']   # плашка під текстом кейса 01 — на 360 стоїть збоку

RES = ['', '640', '480', '360']
HALF = {'': 640, '640': 320, '480': 240, '360': 180}
MEDIA = {'': '', '640': '@media screen and (max-width:959px)',
         '480': '@media screen and (max-width:639px)', '360': '@media screen and (max-width:479px)'}
CUR_LEFT = {'': [30, 440, 850, 1260], '640': [30, 440, 850, 1260], '480': [30, 440, 850, 1260], '360': [15, 360, 705, 1050]}
NEW_LEFT = {'': [235, 645, 235, 645], '640': [120] * 4, '480': [40] * 4, '360': [15] * 4}
# кейси 01 і 02 вищі на TT_D (TikTok-стрічка) — усе, що нижче них, зсунуто на стільки ж
ROW_TOP = {'': [0, 0, 939, 939], '640': [0, 939, 1878, 2578], '480': [0, 939, 1878, 2578], '360': [0, 780, 1560, 2130]}
ART_H = {'': 1639, '640': 3278, '480': 3278, '360': 2720}
CHAIN = {'': [''], '640': ['640', ''], '480': ['480', '640', ''], '360': ['360', '480', '640', '']}
# скріни кейса 01 (build.py ZV_SHOTS робить їх 358px на всіх екранах) — на 360 як у кейса 02
OVERRIDE = {'1763049596474': {'360': (31, 130, 295, 116)},   # ДО: left, top, width, height
            '1763049596500': {'360': (31, 294, 297, 328)}}   # ПІСЛЯ + TikTok-стрічка (TT_H)


def _col(left):
    return 0 if left < 420 else 1 if left < 840 else 2 if left < 1250 else 3


def _val(attrs, key, res):
    """Значення атрибута для res з успадкуванням від більшого екрана (як у Tilda)."""
    for r in CHAIN[res]:
        m = re.search(r'data-field-%s%s-value="(-?[\d.]+)"' % (key, '-res-%s' % r if r else ''), attrs)
        if m:
            return int(float(m.group(1)))
    return 0


def _set(attrs, key, res, v):
    a = 'data-field-%s%s-value' % (key, '-res-%s' % res if res else '')
    if re.search(a + '="', attrs):
        return re.sub(a + r'="[^"]*"', '%s="%d"' % (a, v), attrs)
    return attrs + ' %s="%d"' % (a, v)


def regrid(rec):
    edits, css = [], ''
    for m in re.finditer(r"<div class='t396__elem tn-elem tn-elem__1558030471(\d+)'([^>]*)>", rec):
        eid, attrs = m.group(1), m.group(2)
        if eid in HIDE:
            continue
        col = _col(_val(attrs, 'left', ''))
        new = attrs
        for res in RES:
            l = _val(attrs, 'left', res) - CUR_LEFT[res][col] + NEW_LEFT[res][col]
            t = _val(attrs, 'top', res) + ROW_TOP[res][col]
            size = ''
            if eid in OVERRIDE and res in OVERRIDE[eid]:
                l, t, w, h = OVERRIDE[eid][res]
                new = _set(_set(new, 'width', res, w), 'height', res, h)
                size = 'width:%dpx!important;height:%dpx!important;' % (w, h)
            new = _set(_set(new, 'left', res, l), 'top', res, t)
            r = ('#rec1558030471 .tn-elem[data-elem-id="%s"]{top:%dpx!important;'
                 'left:calc(50%% - %dpx + %dpx)!important;%s}' % (eid, t, HALF[res], l, size))
            css += (MEDIA[res] + '{' + r + '}') if MEDIA[res] else r
        edits.append((m.start(2), m.end(2), new))
    for a, b, new in reversed(edits):
        rec = rec[:a] + new + rec[b:]
    # висота артборда
    rec = re.sub(r'data-artboard-height="\d+"', 'data-artboard-height="%d"' % ART_H[''], rec, 1)
    rec = re.sub(r'data-artboard-height-res-480="\d+"',
                 'data-artboard-height-res-640="%d" data-artboard-height-res-480="%d"' % (ART_H['640'], ART_H['480']), rec, 1)
    rec = re.sub(r'data-artboard-height-res-360="\d+"', 'data-artboard-height-res-360="%d"' % ART_H['360'], rec, 1)
    for res in RES:
        r = ('#rec1558030471 .t396__artboard,#rec1558030471 .t396__filter,#rec1558030471 .t396__carrier'
             '{height:%dpx!important}' % ART_H[res])
        css += (MEDIA[res] + '{' + r + '}') if MEDIA[res] else r
    css += ','.join('#rec1558030471 .tn-elem[data-elem-id="%s"]' % e for e in HIDE) + '{display:none!important}'
    css += MEDIA['360'] + '{' + ','.join('#rec1558030471 .tn-elem[data-elem-id="%s"]' % e for e in HIDE_MOBILE) + '{display:none!important}}'
    return rec, css
