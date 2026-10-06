"""Банер cookie і Meta Pixel лише за згодою (Оксана 06.10.2026, після юр-аналізу).

Pixel не завантажується, доки людина не натисне «Прийняти»; вибір зберігається в localStorage
(«oks_cookie» = yes / no). «Налаштування cookie» — будь-яке посилання з атрибутом data-cookie-settings.
Використовують site2.py (головна) і blog.py (блог, сторінка послуги, юридичні сторінки).
"""

PIXEL_ID = '1478624944307903'

# у <head>: oksPixel() вмикає Pixel; одразу — тільки якщо раніше натиснули «Прийняти»
HEAD = ("<!-- Meta Pixel (набір «Оксана Богданець | Особистий бренд») — лише після «Прийняти» в банері cookie -->\n"
        "<script>window.oksPixel=function(){if(window.fbq)return;!function(f,b,e,v,n,t,s){if(f.fbq)return;"
        "n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;"
        "n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;"
        "s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script',"
        "'https://connect.facebook.net/en_US/fbevents.js');fbq('init','" + PIXEL_ID + "');fbq('track','PageView')};"
        "try{if(localStorage.getItem('oks_cookie')==='yes')oksPixel()}catch(e){}</script>")

CSS = (".ck{position:fixed;left:16px;right:16px;bottom:16px;z-index:55;max-width:560px;margin:0 auto;background:#111;"
       "border:1px solid rgba(246,212,170,.35);border-radius:18px;padding:16px 18px;color:#d2d2d2;"
       "font:14px/1.45 'Inter',Arial,sans-serif;box-shadow:0 10px 40px rgba(0,0,0,.6)}"
       ".ck[hidden]{display:none}.ck p{margin:0}.ck a{color:#f6d4aa}"
       ".ck-b{display:flex;gap:10px;margin-top:12px;justify-content:flex-end;flex-wrap:wrap}"
       ".ck-b button{flex:0 1 150px;border-radius:30px;padding:11px 18px;font:600 14px 'Inter',Arial,sans-serif;cursor:pointer;"
       "border:1px solid #f6d4aa;background:none;color:#f6d4aa}"
       ".ck-b button[data-ck=yes]{background:#f6d4aa;color:#000}")

# перед </body>
BANNER = ('<div class="ck" id="ck" role="dialog" aria-label="Cookie" hidden>'
          '<p>Ми використовуємо cookie і Meta Pixel, щоб оцінювати роботу сайту й реклами. Без вашої згоди вони не вмикаються. '
          '<a href="/privacy-policy.html">Політика конфіденційності</a></p>'
          '<div class="ck-b"><button type="button" data-ck="no">Відхилити</button>'
          '<button type="button" data-ck="yes">Прийняти</button></div></div>'
          '<style>' + CSS + '</style>'
          "<script>(function(){var b=document.getElementById('ck');if(!b)return;"
          "function get(){try{return localStorage.getItem('oks_cookie')}catch(e){return null}}"
          "function set(v){try{localStorage.setItem('oks_cookie',v)}catch(e){}}"
          "if(!get())b.hidden=false;"
          "b.addEventListener('click',function(e){var v=e.target.getAttribute&&e.target.getAttribute('data-ck');if(!v)return;"
          "var was=get();set(v);b.hidden=true;if(v==='yes'&&window.oksPixel)oksPixel();else if(v==='no'&&was==='yes')location.reload()});"
          "document.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('[data-cookie-settings]');"
          "if(!a)return;e.preventDefault();b.hidden=false})})();</script>")

SETTINGS_LINK = '<a href="#" data-cookie-settings>Налаштування cookie</a>'
