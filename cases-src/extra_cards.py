"""Додає нові картки у стрічку «Приклади відео» (Tilda zero-block rec1558059361).

В оригіналі reels-agency.ru картки стоять в один ряд з горизонтальною прокруткою:
ширина 337px, крок 367px, під ними лінія-трек. Нові картки просто продовжують ряд —
клонуємо пару елементів слоту 5 (shape-приймач + preview-обкладинка), її CSS-правила
разом з медіа-контекстом, і ANNEXX-віджет, що чіпляє відео до shape.
"""
import re

REC = 'rec1558059361'
SH_CLS, SH_ID = '1558059361176346352572069110', '176346352572069110'   # shape слоту 5
PV_CLS, PV_ID = '15580593611763704917239000005', '1763704917239000005'  # preview слоту 5
SPACER_ID = '176346356351337360'          # порожній елемент справа, задає ширину прокрутки
STEP = {'': 367, '360': 330, '480': 357, '640': 367}
BASE = {'': 1498, '360': 1335, '480': 1443, '640': 1498}   # позиції слоту 5


def _dom_frag(s, cls):
    """DOM-елемент за класом: він іде останнім входженням (перед ним — конфіги ANNEXX)."""
    i = s.rindex("tn-elem__" + cls)
    a = s.rfind("<div class='t396__elem", 0, i)
    b = s.find("<div class='t396__elem", i)
    return a, b, s[a:b]


def _shift(frag, n, old_id, new_id, old_cls, new_cls):
    """Копія DOM-елемента: новий id/клас і зсув по left на n кроків."""
    frag = frag.replace(old_cls, new_cls).replace("'" + old_id + "'", "'" + new_id + "'")
    for res, step in STEP.items():
        attr = 'data-field-left-value' if not res else 'data-field-left-res-%s-value' % res
        frag = frag.replace('%s="%d"' % (attr, BASE[res]), '%s="%d"' % (attr, BASE[res] + step * n))
    return frag


def _css_rules(css, elem_id):
    """Всі правила для elem_id разом з @media-преамбулою, в якій вони лежать."""
    out, stack, i, n = [], [], 0, len(css)
    while i < n:
        b, e = css.find('{', i), css.find('}', i)
        if b < 0 and e < 0:
            break
        if e >= 0 and (b < 0 or e < b):        # закрилась @media-обгортка
            if stack:
                stack.pop()
            i = e + 1
            continue
        sel = css[i:b].strip()
        if sel.startswith('@media'):
            stack.append(sel + '{')
            i = b + 1
            continue
        e = css.find('}', b)
        if e < 0:
            break
        if 'data-elem-id="%s"' % elem_id in sel:
            out.append((''.join(stack), sel + css[b:e + 1]))
        i = e + 1
    return out


def _css_for(css, elem_id, new_id, n):
    """CSS нових елементів: той самий набір правил зі зсунутим left."""
    chunks = []
    for media, rule in _css_rules(css, elem_id):
        r = rule.replace('data-elem-id="%s"' % elem_id, 'data-elem-id="%s"' % new_id)
        for res, step in STEP.items():
            r = r.replace('+ %dpx)' % BASE[res], '+ %dpx)' % (BASE[res] + step * n))
        chunks.append((media + r + ('}' * media.count('@media')) if media else r))
    return ''.join(chunks)


def add(s, videos, donor_url, css_hook='</head>'):
    """videos — список (номер слоту, шлях_до_mp4, шлях_до_обкладинки) для карток 7, 8, …

    donor_url — адреса ролика, що вже стоїть у слоті 5: за нею знаходимо
    ANNEXX-віджет-донор. Передається ззовні, бо номер файла в слоті може мінятись.
    """
    sh_a, sh_b, sh_frag = _dom_frag(s, SH_CLS)
    pv_a, pv_b, pv_frag = _dom_frag(s, PV_CLS)
    cover5 = re.search(r'img/[^"\']+\.(?:jpg|png)', pv_frag).group(0)

    # ANNEXX-віджет слоту 5 — цілий rec-блок
    i = s.index(donor_url)
    w_a = s.rfind('<div id="rec', 0, i)
    w_b = s.find('<div id="rec', i)
    widget = s[w_a:w_b]

    # CSS артборда
    rec_i = s.index('<div id="%s"' % REC)
    st = s.index('<style>', rec_i) + len('<style>')
    en = s.index('</style>', st)
    css = s[st:en]

    dom_add, widget_add, css_add, play = '', '', '', []
    for num, _mp4, cover in videos:
        k = num - 5                      # зсув у кроках відносно слоту 5, який клонуємо
        new_sh_id, new_pv_id = SH_ID[:-2] + '%02d' % (10 + num), PV_ID[:-2] + '%02d' % num
        new_sh_cls, new_pv_cls = '1558059361' + new_sh_id, '1558059361' + new_pv_id
        dom_add += _shift(sh_frag, k, SH_ID, new_sh_id, SH_CLS, new_sh_cls)
        dom_add += _shift(pv_frag, k, PV_ID, new_pv_id, PV_CLS, new_pv_cls).replace(cover5, cover)
        widget_add += (widget.replace(SH_CLS, new_sh_cls).replace(PV_CLS, new_pv_cls)
                             .replace(donor_url, _mp4)
                             .replace('id="rec1590968851"', 'id="rec159096885%d"' % (1 + k)))
        css_add += _css_for(css, SH_ID, new_sh_id, k) + _css_for(css, PV_ID, new_pv_id, k)
        play.append(new_pv_cls)

    # зсуваємо правий обмежувач прокрутки за останню картку
    n = len(videos)
    for res, step in STEP.items():
        attr = 'data-field-left-value' if not res else 'data-field-left-res-%s-value' % res
        old = {'': 2202, '360': 1985, '480': 2137, '640': 2202}[res]
        s = s.replace('%s="%d"' % (attr, old), '%s="%d"' % (attr, old + step * n))
    for old, new in ((2202, 2202 + STEP[''] * n),):
        s = s.replace('data-elem-id="%s"]{z-index:3;top:6px;;left:calc(50%% - 640px + %dpx)' % (SPACER_ID, old),
                      'data-elem-id="%s"]{z-index:3;top:6px;;left:calc(50%% - 640px + %dpx)' % (SPACER_ID, new))

    s = s[:pv_b] + dom_add + s[pv_b:]
    w_b2 = s.index('<div id="rec', s.index(donor_url))
    s = s[:w_b2] + widget_add + s[w_b2:]
    s = s.replace(css_hook, '<style>' + css_add + '</style>\n' + css_hook, 1)
    return s, play
