#!/usr/bin/env python3
"""Анкета на навчання «SMM через Claude»: oksanabogdanets.com.ua/smm/anketa/ (Оксана 26.10.2026).

Посилання і QR — на останньому слайді PDF-презентації навчання. Відповіді летять через FormSubmit на той самий alias,
що й форма сайту (листи на Gmail Оксани). Після анкети Оксана пише людині сама. Сторінка закрита від пошуку (noindex).
Запуск: python3 cases-src/smm_anketa.py → smm/anketa/index.html
"""
import os
import re
import sys

S = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, S)
import site2  # noqa: E402
import kp  # noqa: E402
from form import ENDPOINT  # noqa: E402
from site2 import consent  # noqa: E402

OUT = os.path.join(os.path.dirname(S), 'smm', 'anketa', 'index.html')

CSS = """
.an{max-width:720px;margin:0 auto;padding:70px 20px 90px}
.an .tag{display:inline-block;border:1px solid rgba(246,212,170,.5);color:var(--gold);border-radius:40px;padding:8px 18px;font-size:14px;margin-bottom:22px}
.an h1{font-family:'Oswald','Inter',sans-serif;font-weight:600;font-size:54px;line-height:1.05;text-transform:uppercase}
.an .lead{color:#d2d2d2;font-size:17px;line-height:1.5;margin:16px 0 34px}
.an form{border-radius:28px;padding:34px;background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);border:1px solid rgba(246,212,170,.35)}
.an label.q{display:block;color:#fff;font-size:16px;font-weight:600;margin:0 0 10px}
.an .f{margin-bottom:24px}
.an input[type=text],.an textarea{width:100%;box-sizing:border-box;background:#0a0a0a;border:1px solid rgba(255,255,255,.14);border-radius:14px;
  color:#fff;font-size:16px;padding:14px 16px;outline:none;font-family:inherit}
.an textarea{min-height:110px;resize:vertical}
.an input:focus,.an textarea:focus{border-color:var(--gold)}
.an .opts{display:flex;flex-wrap:wrap;gap:10px}
.an .opts label{cursor:pointer}
.an .opts input{position:absolute;opacity:0}
.an .opts span{display:inline-block;border:1px solid rgba(255,255,255,.25);border-radius:40px;padding:10px 18px;font-size:15px;color:#e6e6e6}
.an .opts input:checked+span{background:var(--gold);border-color:var(--gold);color:#000;font-weight:600}
.an button{width:100%;border:0;cursor:pointer;background:var(--gold);color:#000;font-size:17px;font-weight:600;border-radius:40px;padding:18px 22px;font-family:inherit;margin-top:6px}
.an .note{color:#8a8a8a;font-size:13px;line-height:1.4;margin-top:14px;text-align:center}
.an .ok{display:none;text-align:center;border-radius:28px;padding:44px 30px;border:1px solid rgba(246,212,170,.5);background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%)}
.an .ok h2{font-family:'Oswald','Inter',sans-serif;font-weight:600;font-size:40px;text-transform:uppercase;color:var(--gold)}
.an .ok p{color:#e6e6e6;font-size:17px;line-height:1.5;margin-top:14px}
@media (max-width:640px){.an h1{font-size:38px}.an form{padding:22px}}
"""

Q = [  # (name, питання, варіанти або None для тексту, обов'язкове)
    ('name', "Ваше ім'я", None, True),
    ('instagram', 'Нік в Instagram', None, True),
    ('contact', 'Telegram або телефон для зв\'язку', None, True),
    ('niche', 'Ваша ніша', ['SMM-спеціаліст', 'Таргетолог', 'Контент-мейкер', 'Веду свій блог', 'Інше'], True),
    ('years', 'Скільки років у професії', ['до 1 року', '1–2 роки', '3–5 років', '5+ років'], True),
    ('clients', 'Скільки клієнтів ведете зараз', ['0', '1–2', '3–5', '6+'], True),
    ('income', 'Дохід з професії або блогу на місяць', ['до 15 тис. грн', '15–30 тис.', '30–60 тис.', '60 тис.+'], True),
    ('ai', 'Чи користуєтесь Claude або ChatGPT', ['ні', 'пробую', 'щодня'], True),
    ('problem', 'Що зараз не виходить або забирає найбільше часу', 'textarea', True),
]


def field(name, q, opts, req):
    r = ' required' if req else ''
    if opts is None:
        inp = '<input type="text" name="%s"%s>' % (name, r)
    elif opts == 'textarea':
        inp = '<textarea name="%s"%s></textarea>' % (name, r)
    else:
        inp = '<div class="opts">%s</div>' % ''.join(
            '<label><input type="radio" name="%s" value="%s"%s><span>%s</span></label>' % (name, o, r if i == 0 else '', o)
            for i, o in enumerate(opts))
    return '<div class="f"><label class="q">%s</label>%s</div>' % (q, inp)


BODY = ('<section class="an"><span class="tag">Навчання «SMM через Claude»</span><h1>Анкета <span class="gold">учасника</span></h1>'
        '<p class="lead">Займе хвилину. Я перегляну відповіді й напишу вам особисто — розповім, як навчання допоможе саме вам, '
        'і забронюю місце. У групі лише 10 місць.</p>'
        '<form id="an-form">%s<input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off">'
        '<button type="submit">Надіслати анкету</button>'
        '<p class="note">Надсилаючи анкету, ви погоджуєтесь з <a href="/privacy-policy.html" style="color:#f6d4aa">політикою конфіденційності</a></p></form>'
        '<div class="ok" id="an-ok"><h2>Дякую!</h2><p>Анкету отримала. Напишу вам протягом дня в Instagram або Telegram.</p></div>'
        '</section>') % ''.join(field(*q) for q in Q)

JS = """
(function(){
  var f=document.getElementById('an-form');
  f.addEventListener('submit', async function(e){
    e.preventDefault();
    var b=f.querySelector('button'); b.disabled=true; b.textContent='Надсилаю…';
    var fd=new FormData(f), data={};
    fd.forEach(function(v,k){ data[k]=v; });
    data._subject='Анкета на навчання SMM через Claude: '+(data.name||'')+' ('+(data.instagram||'')+')';
    data._template='table'; data._captcha='false'; data.page=location.href;
    try{
      var r=await fetch('%s',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)});
      if(!r.ok) throw new Error(r.status);
      f.style.display='none'; document.getElementById('an-ok').style.display='block';
      if(window.fbq) fbq('track','Lead');
    }catch(err){ b.disabled=false; b.textContent='Спробувати ще раз'; }
  });
})();
""" % ENDPOINT

HEAD = (kp.HEAD.replace('Комерційна пропозиція · Оксана Богданець', 'Анкета · навчання SMM через Claude')
        .replace('Reels і TikTok під ключ: кейси, приклади відео, етапи роботи і вартість.',
                 'Анкета учасника навчання «SMM через Claude» для SMM-спеціалістів.'))


def build():
    fcss, fpre = site2.fonts()
    css = fcss + re.sub(r'\n\s*', '\n', ''.join(site2.CSS_PARTS) + CSS).strip()
    page = (HEAD % {'favicon': site2.favicon(), 'css': css, 'fontpre': fpre, 'pixel': consent.HEAD}
            + '<main id="main">' + BODY + '</main>\n<script>' + JS + '</script>\n' + consent.BANNER + '\n</body>\n</html>\n')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(page)
    print('smm/anketa/index.html: %d КБ' % (len(page.encode()) // 1024))


if __name__ == '__main__':
    build()
