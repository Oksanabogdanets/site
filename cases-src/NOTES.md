# Сайт кейсів — як з ним працювати (для агента без доступу до Mac)

Власниця — Оксана Богданець (Reels-продакшн). Звертатись на «ти», відповідати українською;
Оксана часто диктує російською — це нормально. Спочатку короткий план, потім дії.
Скріни від Оксани іноді не доходять — просити описати словами.

## Що де
- `cases/` — зібраний сайт (GitHub Pages: https://oksanabogdanets.github.io/site/cases/).
  `cases/latest.html` — лінк в обхід кешу, давати Оксані саме його.
- `cases-src/build.py` — збирає `cases/index.html` з `ra.html` (клон Tilda-сторінки конкурента
  reels-agency.ru): список замін тексту `T`, мапа картинок `rep` (індекс ra-img → файл в `assets/`),
  список відео `VIDEOS`, власні блоки. Запуск: `cd cases-src && python3 build.py`
  (потрібні Python 3 + `pip install pillow numpy`).
- Модулі власних блоків: `packages.py` (4 пакети), `niches.py` (ряд ніш), `team.py` (команда),
  `blocks.py` (суть, «Що ви отримуєте», «Хто веде проєкт»), `form.py` (форма → FormSubmit),
  `extra_cards.py` (додаткові картки відео у стрічці), `cases_tall.py` (кейси 03/04 + сітка 2×2),
  `make_reviews.py` (колаж відгуків), `reviews.py` (текстові відгуки, поки не підключено).
- `assets/` — картинки сайту (`_asset_url()` копіює їх у `cases/img/` з md5-суфіксом).
- `canva/pNN.png` — сторінки презентації Оксани (джерело скрінів кейсів), `crop_canva.py` — вирізки.
- `reviews-src/` — скріни чатів для відгуків (Telegram у ТЕМНІЙ темі, без шпалер).
- `cases/video/vN.mp4` + `assets/vcoverN.jpg` — ролики стрічки «Приклади відео».

## Деплой
```
cd cases-src && python3 build.py
cd .. && git add cases && git commit -m "[agent] fix(cases): …" && git push origin main
```
Перевірка, що GitHub Pages оновився (1–2 хв):
`curl -s "https://oksanabogdanets.github.io/site/cases/?n=1" | md5sum` == md5 локального `cases/index.html`.

## Типові задачі
- **Нове відео у стрічку**: `ffmpeg -nostdin -i IN.mov -vf scale=720:1280 -r 30 -c:v libx264 -preset slow -crf 26
  -profile:v high -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 96k cases/video/vN.mp4`,
  кадр-обкладинка → `assets/vcoverN.jpg` (720×1280), номер у список `VIDEOS` у build.py (порядок = порядок на сайті).
- **Відгуки**: скріни чатів у темній темі → `reviews-src/` → `python3 make_reviews.py reviews-src/a.png reviews-src/b.png …`
  → `assets/chats.jpg` → build. Зараз там один відгук (Ольга, khobzei.clinic), треба ще два.
- **Фото команди**: 888×888 у `assets/`, ім'я файла у `team.py` PEOPLE (Олександр, Анастасія, Данило, Валерія — фото ще нема).
- **Тексти**: правити у списку `T` в build.py або у відповідному модулі; після зміни — build і перевірка
  `russian leftovers: 0` у виводі.

## Правила, здобуті болем
- Секція Tilda = кілька `rec` поспіль (hero = rec1558021021 + мозаїка rec1570791861). Вставляти власний блок
  лише між незалежними секціями, дивитись сусідні rec.
- Блок кейсів (rec1558030471) переведено зі стрічки з прихованою прокруткою у сітку 2×2 / стовпчик (`cases_tall.regrid`).
- Кейс 04 = Muza Body (клініка естетичної медицини): тексти з комерційної пропозиції (КП): ребрендинг,
  сторінка з 0 за 30 днів, заявки через 2 тижні, органіка.
- Етапи роботи й години клієнта — з КП Оксани, не вигадувати.
- Ніколи не пушити, не перевіривши результат; «нічого не змінилось» від Оксани = зазвичай кеш браузера → latest.html.
- Коміти: `[agent] type(cases): опис` + трейлер `Co-Authored-By: Claude …`.
