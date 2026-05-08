# CLAUDE.md — Telegram Mini App «Цифровой мастер»

## Что это
Telegram Mini App — портфолио цифрового специалиста (сайты, приложения, ИИ-агенты).
Открывается прямо внутри Telegram через кнопку бота.
Стек: чистый HTML + CSS + JS. Никаких фреймворков.

---

## Структура файлов

```
tg-app/
├── index.html    — точка входа, всё HTML (4 экрана + навигация)
├── styles.css    — все стили: тема, компоненты, анимации
├── app.js        — логика: навигация, FAQ, форма, Telegram SDK
└── CLAUDE.md     — этот файл
```

---

## Навигация между экранами

4 экрана переключаются через нижнюю панель (`bottom-nav`).
Анимация: slide + fade за 220ms (`--transition` в CSS).

| ID экрана       | Вкладка    | Что внутри                              |
|----------------|------------|------------------------------------------|
| `screen-home`  | Главная    | Hero, статистика, боли, метод, CTA       |
| `screen-services` | Услуги  | 4 карточки услуг с ценами               |
| `screen-cases` | Кейсы      | 3 кейса с результатами в цифрах         |
| `screen-contact` | Контакт  | Процесс работы, FAQ, форма заявки       |

Функция переключения: `navigate(screenId, navBtn)` в `app.js`.

---

## Где менять данные

### Контакт / Telegram
- В `index.html` → кнопка «Написать в Telegram»: замени `href="https://t.me/your_username"`
- В `app.js` → функция `openTelegram()`: замени `const url = 'https://t.me/your_username'`

### Цены на услуги
- `index.html` → блок `#screen-services` → `.service-price` в каждой карточке

### Кейсы (результаты)
- `index.html` → блок `#screen-cases` → каждый `.case-card`
- Поля: `.case-niche`, `.case-title`, `.case-big-num`, `.case-result-label`, `.case-row`

### Статистика (числа в шапке)
- `index.html` → `.stats-grid` → `.stat-card`
- Для анимированного счётчика: добавь `data-target="40"` на `.stat-num`

### FAQ — добавить вопрос
```html
<div class="faq-item">
  <button class="faq-q" onclick="toggleFaq(this)">
    Твой вопрос здесь?
    <span class="faq-arrow">›</span>
  </button>
  <div class="faq-a">
    Ответ на вопрос.
  </div>
</div>
```

---

## Telegram SDK

Подключён через CDN: `https://telegram.org/js/telegram-web-app.js`

Что использует приложение:
- `tg.expand()` — раскрытие на весь экран
- `tg.colorScheme` — тёмная / светлая тема
- `tg.themeParams` — цвета из Telegram
- `tg.BackButton` — системная кнопка «Назад»
- `tg.HapticFeedback` — вибрация при нажатиях
- `tg.sendData(json)` — отправка заявки боту
- `tg.openLink(url)` — открыть ссылку через Telegram

Все вызовы SDK обёрнуты в `if (tg)` — приложение корректно работает и в обычном браузере.

---

## Тёмная / светлая тема

Применяется автоматически из Telegram через `tg.colorScheme`.
В браузере — через `prefers-color-scheme`.
Переменные CSS: `:root` (светлая) и `.dark` (тёмная) в `styles.css`.

Чтобы сменить акцентный цвет — измени `--accent: #2AABEE` в `:root`.

---

## Отправка заявки

Сейчас: `tg.sendData(JSON.stringify({name, contact, task}))` — данные идут в Telegram-бота.

Чтобы отправлять на свой сервер — замени в `app.js` функцию `submitForm`:
```js
await fetch('/api/contact', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name, contact, task })
});
```

---

## Как запустить

### Локально (для просмотра)
Открыть `index.html` в браузере. Тема — из `prefers-color-scheme`.

### В Telegram
1. Создать бота через @BotFather
2. Включить Menu Button → указать URL опубликованного `index.html`
3. Или использовать Inline Button с `web_app: { url: "..." }`
4. Опубликовать файлы на любой хостинг (GitHub Pages, Vercel, Netlify — всё подходит)

---

## Мобильная адаптация

- Диапазон: 320px–430px (iPhone SE → iPhone 15 Plus)
- Все кнопки: `min-height: 44px` (Apple HIG)
- Шрифт: минимум 13px (body 15px)
- Нет горизонтальной прокрутки
- Safe area для iPhone с «чёлкой»: `padding-bottom: env(safe-area-inset-bottom)`
- Touch: `:active` работает на iOS через пустой `touchstart` listener
