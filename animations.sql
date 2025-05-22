create table animations (
  id uuid primary key default gen_random_uuid(),
  prompt text not null,
  level text not null,
  email text,
  status text default 'pending',
  video_url text,
  error text,
  created_at timestamptz default now(),
  completed_at timestamptz
);
