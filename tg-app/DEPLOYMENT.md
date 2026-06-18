# DEPLOYMENT.md — Чеклист публікації Telegram Mini App

## Поточна конфігурація
- **Фронтенд (Mini App):** GitHub Pages → `https://oksanabogdanets.github.io/site/tg-app/`
- **Бот:** `@oksana_bogdanets_bot` (Formula_reels)
- **Репозиторій:** `git@github.com:Oksanabogdanets/site.git` (гілка `main`)

---

## Крок 1 — Внести зміни локально

1. Відкрити файли в VSCode (папка `my-landing/tg-app/`)
2. Внести правки в `index.html`, `styles.css` або `app.js`
3. Переглянути результат: відкрити `index.html` в браузері

---

## Крок 2 — Зберегти і опублікувати

```bash
cd Documents/projects/my-landing

# Подивитись які файли змінились
git status

# Додати зміни
git add tg-app/

# Зберегти з описом
git commit -m "Опис що змінила"

# Відправити на GitHub
git push origin main
```

**GitHub Pages оновлюється автоматично** через ~1-2 хвилини після push.

---

## Крок 3 — Перевірити що все працює

- [ ] Відкрити `https://oksanabogdanets.github.io/site/tg-app/` в браузері
- [ ] Перевірити мобільний вигляд (DevTools → Toggle device toolbar)
- [ ] Відкрити Telegram → `@oksana_bogdanets_bot` → кнопка "Відкрити"
- [ ] Пройти весь флоу: Головна → Програма → Кейси → Записатись → відправити форму

---

## Крок 4 — Налаштування бота (робиться один раз)

Menu Button вже налаштовано! Перевірити:
```bash
curl -s "https://api.telegram.org/bot<TOKEN>/getChatMenuButton"
```
Має повернути: `{"type": "web_app", "text": "Відкрити", ...}`

---

## Що НЕ потрібно комітити

- `.env` — токен бота (він в `.gitignore`)
- `node_modules/` — якщо з'явиться
- `.DS_Store`

---

## Швидкий деплой (одна команда)

```bash
cd ~/Documents/projects/my-landing && git add tg-app/ && git commit -m "Update mini app" && git push
```

---

## Посилання для поширення

- **Пряме посилання** на Mini App через бота: `https://t.me/oksana_bogdanets_bot`
- **Web-версія** (без Telegram): `https://oksanabogdanets.github.io/site/tg-app/`
