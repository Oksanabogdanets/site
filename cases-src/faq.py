"""FAQ — власний акордеон замість Tilda-блоків (rec1558142251 … rec1576480751).

У Tilda кожне питання і відповідь — окремий zero-block, відповіді на телефоні
йшли шрифтом 9px і вилазили за картку (Оксана 23.09: «текст з'їхав у телефонному
режимі»). Питання «Які етапи роботи?» прибрано — етапи є окремим блоком.
Правити = міняти QA.
"""

QA = [
    ('Скільки часу до перших роликів?',
     'Місяць — від стратегічної сесії до готових відео. Перші два тижні команда готує '
     'стратегію і сценарії, далі зйомка і монтаж.'),
    ('А якщо я не в Києві?',
     'Наша команда працює по всій Україні: у нас є свої оператори в кожному місті. '
     'Але головний результат залежить від стратегії і сценаріїв, які повністю веде Оксана, '
     'і це не залежить від міста.'),
    ('Що, якщо я не вмію говорити на камеру?',
     'Майже всі клієнти, яких ви бачите на цій сторінці, починали з нами — це була їхня '
     'перша зйомка. Перед зйомкою ми проводимо достатньо часу, щоб у кадрі ви почувалися впевнено.'),
]

CSS = """
#oks-faq{background:#000;padding:90px 20px 90px;font-family:'Inter',Arial,sans-serif}
#oks-faq .fq-in{max-width:1000px;margin:0 auto}
#oks-faq .fq-head{text-align:center;margin-bottom:36px}
#oks-faq .fq-head .oks-tag{margin-bottom:18px}
#oks-faq h2{color:#fff;font-size:40px;font-weight:600;line-height:1.1;margin:0}
#oks-faq details{margin-bottom:14px}
#oks-faq summary{list-style:none;cursor:pointer;display:flex;align-items:center;justify-content:space-between;gap:16px;
  border-radius:40px;padding:18px 22px 18px 28px;color:#000;font-size:17px;font-weight:700;text-transform:uppercase;
  letter-spacing:.02em;background:linear-gradient(90deg,#f6d4aa 0%,#d9b98f 100%)}
#oks-faq summary::-webkit-details-marker{display:none}
#oks-faq summary .fq-ic{flex:0 0 36px;width:36px;height:36px;border-radius:50%;border:2px solid rgba(0,0,0,.35);
  display:flex;align-items:center;justify-content:center;font-size:24px;font-weight:400;line-height:1;transition:transform .2s ease}
#oks-faq details[open] summary .fq-ic{transform:rotate(45deg)}
#oks-faq .fq-a{margin:10px 0 0;border-radius:26px;padding:22px 28px;background:#0a0a0a;border:1px solid rgba(255,255,255,.1);
  color:#d2d2d2;font-size:16px;line-height:1.5}
@media screen and (max-width:640px){#oks-faq{padding:60px 16px 60px}#oks-faq h2{font-size:28px}
  #oks-faq summary{font-size:14px;padding:14px 16px 14px 20px}#oks-faq summary .fq-ic{flex-basis:30px;width:30px;height:30px;font-size:20px}
  #oks-faq .fq-a{padding:16px 18px;font-size:15px}}
"""


def html():
    items = ''.join('<details%s><summary>%s<span class="fq-ic">+</span></summary><div class="fq-a">%s</div></details>'
                    % (' open' if i == 0 else '', q, a) for i, (q, a) in enumerate(QA))
    return ('<div id="oks-faq"><div class="fq-in"><div class="fq-head"><span class="oks-tag">FAQ</span>'
            '<h2>Те, що ви точно хотіли спитати</h2></div>%s</div></div>' % items)
