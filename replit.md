# S-ARQ - Sistema de Gerenciamento de Arquivo

## Overview
S-ARQ is a Django-based document management system for Brazilian military/government organizations. It manages archive boxes, document codes, document lifecycles (phases, retention periods), and user logs.

## Tech Stack
- **Backend:** Django 5.1.3 (Python 3.12)
- **Database:** SQLite (`db.sqlite3`)
- **Frontend:** Django Templates + Bootstrap, Font Awesome, jQuery, Plotly
- **Charts:** Matplotlib, Seaborn, Plotly
- **Auth:** Django built-in (LDAP disabled in this environment)

## Project Structure
- `core/` — Django project config (settings, URLs, WSGI, roles)
- `app_arq/` — Main business logic app (models, views, templates, migrations)
- `login/` — Custom authentication app
- `static/` — Global static assets (CSS, JS, Images)
- `templates/` — Global HTML templates
- `fixtures/` — Initial data (JSON/Python)
- `db.sqlite3` — SQLite database

## Running the App
The app runs via Django's development server on port 5000:
```
python3 manage.py runserver 0.0.0.0:5000
```

## Key Configuration Notes
- **LDAP disabled**: The original project used LDAP/Active Directory for auth, but it's disabled in this environment. Django's built-in model backend is used instead.
- **ALLOWED_HOSTS**: Set to `['*']` for Replit proxy compatibility.
- **CSRF_TRUSTED_ORIGINS**: Configured to trust Replit domains.
- **Language**: Portuguese (pt-BR), Timezone: America/Sao_Paulo

## Deployment
- Target: autoscale
- Run command: `gunicorn --bind=0.0.0.0:5000 --reuse-port core.wsgi:application`

## Database
SQLite database is pre-populated. To apply new migrations:
```
python3 manage.py migrate
```

## System Dependencies
- `gcc-unwrapped` — Required for numpy/pandas C extensions (libstdc++)
