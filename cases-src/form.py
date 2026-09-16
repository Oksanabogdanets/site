"""Форма «Записатися»: ім'я, нік в Instagram, телефон.

Летить через FormSubmit AJAX на той самий alias, що й квіз (листи на Gmail Оксани).
Нік в Instagram потрібен, щоб подивитись профіль до дзвінка.
"""

ENDPOINT = 'https://formsubmit.co/ajax/5c554157cf1eeb4492b86d791350d154'

CSS = """
#oks-form{background:#000;padding:0 20px 90px;font-family:'Inter',Arial,sans-serif}
#oks-form .fm{max-width:1180px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:40px;
  align-items:center;border-radius:28px;padding:40px;
  background:linear-gradient(160deg,#241a12 0%,#0d0a08 55%,#000 100%);border:1px solid rgba(246,212,170,.35)}
#oks-form h2{color:#fff;font-size:36px;font-weight:600;line-height:1.1;margin:0 0 14px}
#oks-form h2 b{color:#f6d4aa;font-weight:600}
#oks-form .fm-sub{color:#9b9b9b;font-size:15px;line-height:1.45;max-width:440px}
#oks-form label{display:block;color:#9b9b9b;font-size:12px;letter-spacing:.04em;margin:0 0 6px}
#oks-form input{width:100%;box-sizing:border-box;background:#0a0a0a;border:1px solid rgba(255,255,255,.14);
  border-radius:14px;color:#fff;font-size:16px;padding:14px 16px;margin-bottom:14px;outline:none;font-family:inherit}
#oks-form input:focus{border-color:#f6d4aa}
#oks-form button{width:100%;box-sizing:border-box;border:0;cursor:pointer;background:#f6d4aa;color:#000;font-size:16px;font-weight:600;
  border-radius:40px;padding:16px 22px;font-family:inherit;transition:transform .15s ease}
#oks-form button:hover{transform:translateY(-2px)}
#oks-form button[disabled]{opacity:.6;cursor:default;transform:none}
#oks-form .fm-note{color:#6a6a6a;font-size:12px;line-height:1.35;margin-top:10px}
#oks-form .fm-ok{display:none;color:#f6d4aa;font-size:18px;line-height:1.4;padding:22px 0}
#oks-form .fm-hp{position:absolute;left:-9999px;opacity:0}
@media screen and (max-width:900px){#oks-form .fm{grid-template-columns:1fr;gap:26px;padding:26px}
  #oks-form h2{font-size:28px}}
@media screen and (max-width:640px){#oks-form{padding-bottom:60px}}
"""

JS = """
(function(){
  var f=document.getElementById('oks-form-el'); if(!f) return;
  f.addEventListener('submit', async function(e){
    e.preventDefault();
    var b=f.querySelector('button'); b.disabled=true; b.textContent='Надсилаю…';
    var v=function(n){return (f.querySelector('[name='+n+']')||{}).value||'';};
    var data={ name:v('name'), instagram:v('instagram'), phone:v('phone'), page:location.href,
      _subject:'Заявка з сайту кейсів: '+v('name')+' ('+v('instagram')+')', _template:'table', _captcha:'false', _honey:v('_honey') };
    try{
      var r=await fetch('%s',{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)});
      if(!r.ok) throw new Error(r.status);
      f.style.display='none'; document.getElementById('oks-form-ok').style.display='block';
    }catch(err){ b.disabled=false; b.textContent='Спробувати ще раз'; }
  });
})();
""" % ENDPOINT


def html():
    return ('<div id="oks-form"><div class="fm"><div><h2>Записатися на <b>розбір</b></h2>'
            '<p class="fm-sub">Подивимось ваш профіль і нішу до дзвінка, щоб на розборі говорити '
            'предметно: формат, обсяг, з чого починати. 20 хвилин у Zoom, безкоштовно.</p></div>'
            '<div><form id="oks-form-el" autocomplete="on">'
            '<label>Ім’я</label><input name="name" type="text" required maxlength="80">'
            '<label>Нік в Instagram</label><input name="instagram" type="text" required maxlength="80" placeholder="@">'
            '<label>Телефон</label><input name="phone" type="tel" required maxlength="40" placeholder="+380">'
            '<input class="fm-hp" name="_honey" tabindex="-1" autocomplete="off">'
            '<button type="submit">Записатися</button>'
            '<div class="fm-note">Натискаючи кнопку, ви погоджуєтесь на обробку персональних даних.</div>'
            '</form><div id="oks-form-ok" class="fm-ok">Дякую! Заявка вже в Оксани — напише вам протягом дня.</div></div>'
            '</div></div><script>%s</script>' % JS)
