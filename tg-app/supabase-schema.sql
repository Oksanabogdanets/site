-- ─────────────────────────────────────────────────────────────
-- Supabase schema для заявок Mini App «Rilès» (наставництво з Reels)
-- Як застосувати: Supabase → SQL Editor → New query → вставити → Run
-- ─────────────────────────────────────────────────────────────

-- Таблиця заявок з форми «Записатись»
create table if not exists public.leads (
  id          uuid primary key default gen_random_uuid(),
  created_at  timestamptz not null default now(),
  name        text not null,
  contact     text not null,
  tier        text,
  message     text,
  tg_user_id  bigint,
  tg_username text,
  source      text default 'mini_app'
);

-- Row Level Security: вмикаємо захист.
-- Жодних публічних політик не додаємо → читати/писати може ТІЛЬКИ сервер
-- через service_role-ключ (він обходить RLS). Клієнт у базу не лізе.
alter table public.leads enable row level security;

-- Індекс, щоб свіжі заявки були зверху
create index if not exists leads_created_at_idx
  on public.leads (created_at desc);
