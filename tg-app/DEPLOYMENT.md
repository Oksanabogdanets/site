# DEPLOYMENT.md — Як публікувати Telegram Mini App «Rilès»

## Поточна конфігурація (актуальна)
- **Фронтенд (Mini App):** Vercel-проєкт `tg-app` → **https://tg-app-azure-ten.vercel.app**
  - Root Directory = `tg-app`, авто-деплой з GitHub при кожному `push` у `main`
- **Бот:** `@oksana_bogdanets_bot` (Formula_reels) — Menu Button «Відкрити застосунок»
- **Репозиторій:** `git@github.com:Oksanabogdanets/site.git` (гілка `main`)
- **Бекенд:** поки немає (форма → буфер + личка). План — у `BACKEND-PLAN.md`.

---

## Крок 1 — Внести зміни локально
1. Відкрити файли в VS Code (папка `my-landing/tg-app/`)
2. Правки в `index.html` / `styles.css` / `app.js`
3. Переглянути: перетягнути `index.html` у браузер (F12 → режим телефону)

---

## Крок 2 — Зберегти і опублікувати
```bash
cd ~/Documents/projects/my-landing
git status                       # що змінилось
git add tg-app/                  # лише міні-апп (не зачіпаємо інше)
git commit -m "Опис що змінила"
git push origin main             # → Vercel сам задеплоїть за ~1 хв
```
**Vercel оновлює `tg-app-azure-ten.vercel.app` автоматично** після push.

---

## Крок 3 — Перевірити що працює
- [ ] Відкрити `https://tg-app-azure-ten.vercel.app` у браузері телефона
- [ ] Telegram → `@oksana_bogdanets_bot` → кнопка **«Відкрити застосунок»**
- [ ] Пройти флоу: Головна → Програма → Кейси → Записатись → відправити форму

---

## Крок 4 — Налаштування бота (через токен, робиться скриптом)
Скрипт `setup-bot.sh` читає `BOT_TOKEN` з `.env` і налаштовує Menu Button + опис + команди:
```bash
bash ~/Documents/projects/my-landing/tg-app/setup-bot.sh
```
Перевірити Menu Button:
```bash
# (токен бере з .env, не друкує)
cd ~/Documents/projects/my-landing/tg-app && set -a && source .env && set +a
curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getChatMenuButton"
```
Має повернути: `"type":"web_app", "text":"Відкрити застосунок", "url":"https://tg-app-azure-ten.vercel.app/"`

---

## Що НЕ комітимо (у `.gitignore`)
- `.env` — токен бота й майбутні ключі Supabase
- `.DS_Store`, `node_modules/`, `*.log`

---

## Майбутній бекенд (коли робитимемо — див. BACKEND-PLAN.md)
- Змінні `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `OKSANA_CHAT_ID` → **Vercel → Project → Settings → Environment Variables** (не в код!)
- Ендпоінт `tg-app/api/lead.js` (serverless на Vercel) — VPS не потрібен.

---

## Посилання для поширення
- **Бот / Mini App:** `https://t.me/oksana_bogdanets_bot`
- **Веб-версія (без Telegram):** `https://tg-app-azure-ten.vercel.app`
