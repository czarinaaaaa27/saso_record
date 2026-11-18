# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Stack

| Layer    | Technology                                     |
|----------|------------------------------------------------|
| Backend  | Django 6.x + Django REST Framework, Python 3.12 |
| Database | SQLite (`db.sqlite3` at project root)          |
| Frontend | React 19 + Vite (in `frontend/`)               |
| Styling  | Tailwind CSS v4 via `@tailwindcss/vite`        |

## Commands

### Backend
```bash
# Activate virtualenv (required before any Python command)
source venv/Scripts/activate

# Run dev server (port 8000)
python manage.py runserver

# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Create a new Django app
python manage.py startapp <name> apps/<name>
```

### Frontend
```bash
cd frontend

npm run dev      # Vite dev server on port 5173
npm run build    # Production build to frontend/dist/
npm run preview  # Preview production build
```

### Slash commands (Codex)
- `/new-app <name>` — scaffold a new Django app in `apps/` and wire it in
- `/migrate` — run `makemigrations` + `migrate`

## Architecture

### Backend layout
```
manage.py                  # Django entry point
backend/                   # Django project module (settings, urls, wsgi)
apps/
  accounts/                # Custom User model (roles: admin, director, assistant)
  students/                # Student, ClearanceRequirement, CounselingRecord models
  discipline/              # DisciplinaryCase model (minor/moderate/major)
  activities/              # Activity + ActivityParticipation models
  dashboard/               # Read-only stats API (no model, aggregates other apps)
  urls.py                  # Top-level API router
  seed.py                  # Run: python manage.py shell < apps/seed.py
```

`AUTH_USER_MODEL = "accounts.User"` — always use `get_user_model()` not `auth.User`.

When adding a new app: fix `apps.py` `name` to `"apps.<appname>"` (startapp sets it wrong).

API base: `/api/` → `apps/urls.py` → per-app routers.

### Frontend layout
```
frontend/
  src/
    App.jsx
    index.css          # Tailwind entry: @import "tailwindcss"
    components/        # Reusable UI components
    pages/             # Page-level components
    hooks/             # Custom React hooks
    api/               # fetch wrappers for backend calls
  vite.config.js       # Tailwind plugin + /api proxy to :8000
```

Vite proxies all `/api/*` requests to `http://localhost:8000`, so frontend code calls `fetch('/api/...')` without worrying about ports.

### CORS & Auth
- CORS is handled by `django-cors-headers`; React dev origin (`http://localhost:5173`) is allowed via `.env`
- DRF defaults to `SessionAuthentication`. For POST/PUT/DELETE from React, send `X-CSRFToken` header (read from the `csrftoken` cookie).

## Environment
Copy `.env.example` to `.env`. The `.env` file is loaded by `python-dotenv` in `backend/settings.py`. Never commit `.env`.

## Agents
Three Codex sub-agents are configured in `.Codex/agents/`:
- **backend-dev** — Django models, serializers, views, migrations
- **frontend-dev** — React components, Tailwind styling, Vite config
- **fullstack** — features spanning both sides
