// ═══════════════════════════════════════════════════
// Telegram Mini App — Наставництво по Reels (Оксана Богданець)
// Навигация, тема, анимации, форма, FAQ
// ═══════════════════════════════════════════════════

/* ─── 0. Единая точка контакта ─── */
// Личка эксперта. Изменить ник ТУТ — поменяется во всём приложении.
const CONTACT_USERNAME = 'ksysha_bogdanets';
const CONTACT_URL = 'https://t.me/' + CONTACT_USERNAME;
// Бот для лид-магнита (бесплатный разбор из оффер-модалки)
const OFFER_BOT_URL = 'https://t.me/oksana_bogdanets_bot?start=from_app';

/* ─── 1. Инициализация Telegram Web App ─── */
const tg = window.Telegram?.WebApp;

if (tg) {
  tg.expand();   // разворачиваем на весь экран
  tg.ready();    // сообщаем Telegram, что приложение готово

  applyTelegramTheme();                         // применяем тему Telegram
  tg.onEvent('themeChanged', applyTelegramTheme); // слушаем смену темы ОДИН раз

  // Чтобы вертикальный свайп при скролле не закрывал приложение случайно
  if (tg.isVersionAtLeast && tg.isVersionAtLeast('7.7') && tg.disableVerticalSwipes) {
    tg.disableVerticalSwipes();
  }

  // Кнопка «Назад» в шапке Telegram — возвращаем на главную
  tg.BackButton.onClick(() => {
    if (currentScreen !== 'home') {
      navigate('home', document.querySelector('.nav-item'));
    } else {
      tg.BackButton.hide();
    }
  });
}

/* ─── 2. Применение темы Telegram ─── */
function applyTelegramTheme() {
  if (!tg) return;

  const scheme = tg.colorScheme; // 'light' | 'dark'
  if (scheme === 'dark') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }

  // Переменные из Telegram — используем его цвета если есть
  const params = tg.themeParams;
  if (params) {
    const root = document.documentElement;
    if (params.bg_color)            root.style.setProperty('--bg',           params.bg_color);
    if (params.secondary_bg_color)  root.style.setProperty('--bg-secondary', params.secondary_bg_color);
    if (params.text_color)          root.style.setProperty('--text',         params.text_color);
    if (params.hint_color)          root.style.setProperty('--text-muted',   params.hint_color);
    if (params.section_bg_color)    root.style.setProperty('--bg-card',      params.section_bg_color);
  }
}

// Фолбэк: prefers-color-scheme (для просмотра в браузере без Telegram)
if (!tg) {
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  if (mq.matches) document.documentElement.classList.add('dark');
  mq.addEventListener('change', e => {
    document.documentElement.classList.toggle('dark', e.matches);
  });
}

/* ─── 3. Навигация между экранами ─── */
let currentScreen = 'home';
let isNavigating = false;

function navigate(screenId, btn) {
  if (isNavigating || currentScreen === screenId) return;
  isNavigating = true;

  // Уходящий и приходящий экраны
  const prevEl = document.getElementById('screen-' + currentScreen);
  const nextEl = document.getElementById('screen-' + screenId);

  prevEl.classList.add('exit-left');
  prevEl.classList.remove('active');

  // Небольшая задержка для плавности
  requestAnimationFrame(() => {
    nextEl.classList.add('active');
    // Скролл нового экрана — в начало
    const area = nextEl.querySelector('.scroll-area');
    if (area) area.scrollTop = 0;
  });

  // Навигация в нижней панели
  document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
  if (btn) btn.classList.add('active');

  // Кнопка «Назад» в Telegram
  if (tg) {
    screenId === 'home' ? tg.BackButton.hide() : tg.BackButton.show();
  }

  currentScreen = screenId;

  // Чистим exit-класс после анимации
  setTimeout(() => {
    prevEl.classList.remove('exit-left');
    isNavigating = false;
  }, 250);
}

/* ─── 4. FAQ аккордеон ─── */
function toggleFaq(btn) {
  const item = btn.closest('.faq-item');
  const isOpen = item.classList.contains('open');

  // Закрываем все открытые
  document.querySelectorAll('.faq-item.open').forEach(el => el.classList.remove('open'));

  // Открываем нажатый (если был закрыт)
  if (!isOpen) item.classList.add('open');

  // Хаптик-фидбек Telegram
  if (tg?.HapticFeedback) tg.HapticFeedback.selectionChanged();
}

/* ─── 5. Открыть форму заявки (с предвыбором тарифа) ─── */
function openApply(tier) {
  if (tg?.HapticFeedback) tg.HapticFeedback.impactOccurred('medium');

  const navBtn = document.querySelector('.nav-item:last-child');
  navigate('apply', navBtn);

  // Если пришли с кнопки тарифа — сразу выбираем его в форме
  if (tier) {
    const sel = document.getElementById('f-tier');
    if (sel) sel.value = tier;
  }

  setTimeout(() => {
    const form = document.getElementById('contact-form');
    if (form) form.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 300);
}

/* ─── 6. Открыть личку эксперта ─── */
// t.me-ссылки внутри Telegram открываем через openTelegramLink (не закрывает app)
function openContact() {
  if (tg?.openTelegramLink) tg.openTelegramLink(CONTACT_URL);
  else if (tg?.openLink)    tg.openLink(CONTACT_URL);
  else                      window.open(CONTACT_URL, '_blank');
}
function openTelegram(e) {
  if (e) e.preventDefault();
  openContact();
}

/* ─── 7. Кнопка оффер-модалки → бот (лид-магнит) ─── */
function openOfferBot(e) {
  if (e) e.preventDefault();
  if (tg?.openTelegramLink) tg.openTelegramLink(OFFER_BOT_URL);
  else                      window.open(OFFER_BOT_URL, '_blank');
  closeOffer();
}

/* ─── 8. Хелперы: нативный алерт и копирование ─── */
function notify(text) {
  if (tg?.showAlert) tg.showAlert(text);
  else alert(text);
}

function copyToClipboard(text) {
  if (navigator.clipboard?.writeText) {
    navigator.clipboard.writeText(text).catch(() => fallbackCopy(text));
  } else {
    fallbackCopy(text);
  }
}
function fallbackCopy(text) {
  const ta = document.createElement('textarea');
  ta.value = text;
  ta.style.position = 'fixed';
  ta.style.opacity = '0';
  document.body.appendChild(ta);
  ta.focus();
  ta.select();
  try { document.execCommand('copy'); } catch (_) {}
  document.body.removeChild(ta);
}

/* ─── 9. Отправка формы ─── */
// Без sendData (он закрывает app и работает только из keyboard-кнопки).
// Логика: собираем заявку → копируем готовый текст → лид открывает личку и вставляет.
function submitForm(e) {
  e.preventDefault();

  // Honeypot: если скрытое поле заполнено — это бот, тихо выходим
  const hp = document.querySelector('#contact-form [name="hp"]');
  if (hp && hp.value.trim() !== '') return;

  const name    = document.getElementById('f-name').value.trim();
  const contact = document.getElementById('f-contact').value.trim();
  const tierSel = document.getElementById('f-tier');
  const tierVal = tierSel ? tierSel.value : '';
  const tierTxt = tierSel && tierSel.selectedIndex >= 0 ? tierSel.options[tierSel.selectedIndex].text : '';
  const task    = document.getElementById('f-task').value.trim();

  // Валидация
  if (!name)               { notify('Вкажи, будь ласка, імʼя 🙏'); return; }
  if (contact.length < 2)  { notify('Залиш контакт — Telegram або Instagram @username'); return; }

  // Данные пользователя Telegram (если открыто внутри Telegram)
  const u = tg?.initDataUnsafe?.user;
  const fromTg = u
    ? `\n— від ${[u.first_name, u.last_name].filter(Boolean).join(' ')}${u.username ? ' @' + u.username : ''} (id ${u.id})`
    : '';

  // Готовый текст заявки для лички
  const msg =
    `🔥 Заявка на наставництво\n\n` +
    `Імʼя: ${name}\n` +
    `Контакт: ${contact}\n` +
    (tierVal ? `Тариф: ${tierTxt}\n` : '') +
    (task ? `Про себе: ${task}\n` : '') +
    fromTg;

  // Копируем — лид просто вставит и отправит
  copyToClipboard(msg);

  if (tg?.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');

  // Показываем экран успеха (app НЕ закрывается)
  document.getElementById('contact-form').classList.add('hidden');
  document.getElementById('form-success').classList.remove('hidden');
}

/* ─── 10. Экран-оффер (модалка) ─── */
function showOfferIfNeeded() {
  if (localStorage.getItem('offer_shown')) return;
  setTimeout(() => {
    document.getElementById('offer-modal').classList.remove('hidden');
  }, 800);
}

function closeOffer() {
  localStorage.setItem('offer_shown', '1');
  const modal = document.getElementById('offer-modal');
  modal.style.transition = 'opacity 200ms';
  modal.style.opacity = '0';
  setTimeout(() => modal.classList.add('hidden'), 200);
  if (tg?.HapticFeedback) tg.HapticFeedback.selectionChanged();
}

showOfferIfNeeded();

/* ─── 11. Тач-фидбек для всех кнопок (active-состояние на iOS) ─── */
document.querySelectorAll('button, a').forEach(el => {
  el.addEventListener('touchstart', () => {}, { passive: true });
});
