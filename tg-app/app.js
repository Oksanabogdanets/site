// ═══════════════════════════════════════════════════
// Telegram Mini App — Цифровой мастер
// Навигация, тема, анимации, форма, FAQ
// ═══════════════════════════════════════════════════

/* ─── 1. Инициализация Telegram Web App ─── */
const tg = window.Telegram?.WebApp;

if (tg) {
  // Разворачиваем на весь экран
  tg.expand();
  // Готовность приложения
  tg.ready();

  // Применяем тему Telegram (light / dark)
  applyTelegramTheme();

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
    if (params.bg_color)         root.style.setProperty('--bg',         params.bg_color);
    if (params.secondary_bg_color) root.style.setProperty('--bg-secondary', params.secondary_bg_color);
    if (params.text_color)       root.style.setProperty('--text',        params.text_color);
    if (params.hint_color)       root.style.setProperty('--text-muted',  params.hint_color);
    if (params.section_bg_color) root.style.setProperty('--bg-card',     params.section_bg_color);
  }

  // Слушаем смену темы во время работы приложения
  tg.onEvent('themeChanged', applyTelegramTheme);
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

  // Уходящий экран
  const prevEl = document.getElementById('screen-' + currentScreen);
  const nextEl = document.getElementById('screen-' + screenId);

  prevEl.classList.add('exit-left');
  prevEl.classList.remove('active');

  // Небольшая задержка для плавности
  requestAnimationFrame(() => {
    nextEl.classList.add('active');
    // Скролл нового экрана — в начало
    nextEl.querySelector('.scroll-area').scrollTop = 0;
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

/* ─── 5. Анимация счётчика числа ─── */
function animateCounter(el, target, duration = 1000) {
  const start = performance.now();
  const update = (now) => {
    const elapsed = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - elapsed, 3); // ease-out-cubic
    el.textContent = Math.round(ease * target);
    if (elapsed < 1) requestAnimationFrame(update);
  };
  requestAnimationFrame(update);
}

// Запускаем счётчики когда элемент попал в видимость
const counterObs = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const el = entry.target;
    const target = parseInt(el.dataset.target);
    if (!isNaN(target)) animateCounter(el, target);
    counterObs.unobserve(el);
  });
}, { threshold: 0.5 });

document.querySelectorAll('[data-target]').forEach(el => counterObs.observe(el));

/* ─── 6. Открыть консультацию ─── */
function openApply() {
  if (tg?.HapticFeedback) tg.HapticFeedback.impactOccurred('medium');

  const navBtn = document.querySelector('.nav-item:last-child');
  navigate('apply', navBtn);

  setTimeout(() => {
    const form = document.getElementById('contact-form');
    if (form) form.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 300);
}

/* ─── 7. Открыть Telegram напрямую ─── */
function openTelegram(e) {
  e.preventDefault();
  const url = 'https://t.me/ksysha_bogdanets';
  if (tg) {
    tg.openLink(url);
  } else {
    window.open(url, '_blank');
  }
}

/* ─── 8. Отправка формы ─── */
function submitForm(e) {
  e.preventDefault();

  const name    = document.getElementById('f-name').value.trim();
  const contact = document.getElementById('f-contact').value.trim();
  const task    = document.getElementById('f-task').value.trim();

  if (!name || !contact) return;

  // Хаптик
  if (tg?.HapticFeedback) tg.HapticFeedback.notificationOccurred('success');

  // Отправка через Telegram.sendData — данные попадут к боту
  if (tg?.sendData) {
    const payload = JSON.stringify({ name, contact, task });
    tg.sendData(payload);
  } else {
    // В браузере без Telegram — просто логируем (замени на fetch к своему API)
    console.log('Заявка:', { name, contact, task });
  }

  // Показываем успех, скрываем форму
  document.getElementById('contact-form').classList.add('hidden');
  document.getElementById('form-success').classList.remove('hidden');
}

/* ─── 9. Тач-фидбек для всех кнопок ─── */
document.querySelectorAll('button, a').forEach(el => {
  el.addEventListener('touchstart', () => {}, { passive: true }); // разблокирует :active на iOS
});
