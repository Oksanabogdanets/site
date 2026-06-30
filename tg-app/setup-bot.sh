#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# Налаштування Telegram-бота через Bot API.
# Токен читається з .env (поряд зі скриптом) і НЕ друкується ніде.
# Налаштовує: Menu Button (кнопка-застосунок), опис, короткий опис, команди.
# ─────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")"

# 1. Беремо токен з .env (без виводу значення)
if [ ! -f .env ]; then echo "❌ Поряд немає .env"; exit 1; fi
set -a; source .env; set +a
: "${BOT_TOKEN:?❌ У .env немає рядка BOT_TOKEN=...}"

API="https://api.telegram.org/bot${BOT_TOKEN}"
APP_URL="https://tg-app-azure-ten.vercel.app"

# Хелпер: викликає метод, показує лише ok/опис помилки (без токена)
call() { # $1=method  $2=json
  local r
  r=$(curl -s "${API}/$1" -H 'Content-Type: application/json' -d "$2")
  if echo "$r" | grep -q '"ok":true'; then
    echo "  ✅ $1"
  else
    echo "  ⚠️ $1 → $(echo "$r" | sed -E 's/.*"description":"([^"]*)".*/\1/')"
  fi
}

echo "→ Menu Button (кнопка-застосунок знизу)…"
call setChatMenuButton "{\"menu_button\":{\"type\":\"web_app\",\"text\":\"Відкрити застосунок\",\"web_app\":{\"url\":\"${APP_URL}\"}}}"

echo "→ Опис бота…"
call setMyDescription "{\"description\":\"Наставництво з Reels від Оксани Богданець. Навчаю експертів продавати свої послуги через Reels — системно, без бюджету на рекламу. Тисни кнопку нижче, щоб відкрити застосунок 👇\"}"

echo "→ Короткий опис…"
call setMyShortDescription "{\"short_description\":\"Reels-наставництво: заявки з контенту без реклами. Відкрий застосунок 👇\"}"

echo "→ Команди (/start, /help)…"
call setMyCommands "{\"commands\":[{\"command\":\"start\",\"description\":\"Відкрити застосунок і почати\"},{\"command\":\"help\",\"description\":\"Як це працює та звʼязок з Оксаною\"}]}"

echo ""
echo "✅ Готово. Відкрий @oksana_bogdanets_bot — знизу буде кнопка «Відкрити застосунок»."
