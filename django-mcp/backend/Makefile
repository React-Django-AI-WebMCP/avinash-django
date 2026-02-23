.PHONY: help install run migrate makemigrations shell test lint format check docker-up docker-down

PYTHON     = python
MANAGE     = $(PYTHON) manage.py
PIP        = pip
SETTINGS   = config.settings.local

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

# ── Setup ────────────────────────────────────────────────────────────────────
install: ## Install local dependencies
	$(PIP) install -r requirements/local.txt
	pre-commit install
	pre-commit install --hook-type commit-msg

# ── Django ───────────────────────────────────────────────────────────────────
run: ## Run local dev server
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) runserver

migrate: ## Apply migrations
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) migrate

makemigrations: ## Create new migrations
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) makemigrations

migrations-check: ## Check for missing migrations
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) migrate --check

shell: ## Open Django shell
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) shell_plus

collectstatic: ## Collect static files
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) collectstatic --noinput

check: ## Run Django system checks
	DJANGO_SETTINGS_MODULE=$(SETTINGS) $(MANAGE) check

# ── Testing ──────────────────────────────────────────────────────────────────
test: ## Run test suite with coverage
	DJANGO_SETTINGS_MODULE=$(SETTINGS) pytest

test-fast: ## Run tests without coverage
	DJANGO_SETTINGS_MODULE=$(SETTINGS) pytest --no-cov -x

# ── Code Quality ─────────────────────────────────────────────────────────────
lint: ## Run all linters (flake8 + pylint)
	flake8 . --max-line-length=120 --extend-ignore=E203,E266,E501,W503 --exclude=migrations,.venv
	pylint $$(git ls-files '*.py' | grep -v migrations)

format: ## Auto-format code (black + isort)
	black . --line-length=120
	isort . --profile=black --line-length=120

format-check: ## Check formatting without making changes
	black . --check --line-length=120
	isort . --check --profile=black --line-length=120

# ── Docker ───────────────────────────────────────────────────────────────────
docker-up: ## Start all services
	docker compose up --build -d

docker-down: ## Stop all services
	docker compose down

docker-logs: ## Tail logs
	docker compose logs -f

docker-shell: ## Shell into web container
	docker compose exec web bash

docker-manage: ## Run manage.py inside container (e.g. make docker-manage CMD="migrate")
	docker compose exec web python manage.py $(CMD)

# ── Helpers ──────────────────────────────────────────────────────────────────
new-app: ## Scaffold a new Django app (e.g. make new-app NAME=orders)
	$(MANAGE) startapp $(NAME)
	touch $(NAME)/services.py
	touch $(NAME)/urls.py
	@echo "App '$(NAME)' created. Add it to INSTALLED_APPS in config/settings/base.py"
