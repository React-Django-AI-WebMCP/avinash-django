# Backend — Django REST API

Production-ready Django 5 + DRF backend with PostgreSQL, Redis, Celery, JWT auth, and Docker.

## Stack

| Layer | Technology |
|---|---|
| Framework | Django 5, Django REST Framework |
| Auth | SimpleJWT |
| Database | PostgreSQL 16 |
| Cache / Broker | Redis 7 |
| Async tasks | Celery |
| Server | Gunicorn (gthread) |
| Storage | AWS S3 (production) |
| Monitoring | Sentry |
| CI | GitHub Actions |

## Quick Start

```bash
# 1. Create virtualenv
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
make install

# 3. Copy and fill in env vars
cp .env.example .env

# 4. Run migrations
make migrate

# 5. Start dev server
make run
```

## Docker

```bash
make docker-up      # start all services (web + db + redis + celery)
make docker-down    # stop
make docker-logs    # tail logs
make docker-shell   # exec bash in web container
```

## Common Commands

```bash
make test           # pytest + coverage
make lint           # flake8 + pylint
make format         # black + isort
make check          # django system check
make makemigrations # create new migrations
make new-app NAME=orders  # scaffold a new app
```

## Project Structure

```
backend/
├── config/               # Project package (settings, urls, wsgi, asgi)
│   └── settings/
│       ├── base.py       # Shared settings
│       ├── local.py      # Dev overrides
│       └── production.py # Prod overrides
├── core/                 # Shared app (models, middleware, exceptions, etc.)
├── requirements/
│   ├── base.txt
│   ├── local.txt
│   └── production.txt
├── logs/
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── manage.py
```

## API Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health/` | Liveness probe |
| GET | `/ready/` | Readiness probe (DB + cache) |

## Environment Variables

See `.env.example` for the full list with descriptions.

## Adding a New App

```bash
make new-app NAME=orders
# Then add "orders" to INSTALLED_APPS in config/settings/base.py
```
