UV ?= uv
NPM ?= npm
BACKEND_DIR := backend
TGBOT_DIR := tgbot
FRONT_DIR := front
COMPOSE ?= docker compose
COMPOSE_FILE := deploy/local/docker-compose-full.yml
INFRA_SERVICES := backend-db zitadel zitadel-db redis nats

.DEFAULT_GOAL := help

.PHONY: help install test lint format format-check typecheck verify
.PHONY: install-backend run-backend test-backend lint-backend format-backend format-check-backend verify-backend
.PHONY: migrate-backend migration-backend migration-check-backend
.PHONY: install-tgbot run-tgbot-polling run-tgbot-webhook test-tgbot lint-tgbot format-tgbot
.PHONY: format-check-tgbot typecheck-tgbot verify-tgbot
.PHONY: install-front run-front lint-front typecheck-front build-front verify-front
.PHONY: infra-up infra-down infra-logs

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "; printf "Usage: make <target>\n\nTargets:\n"} /^[a-zA-Z0-9_-]+:.*## / {printf "  %-26s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: install-backend install-tgbot install-front ## Install all application dependencies

test: test-backend test-tgbot ## Run all available test suites

lint: lint-backend lint-tgbot lint-front ## Run all linters without modifying files

format: format-backend format-tgbot ## Format Python application code

format-check: format-check-backend format-check-tgbot ## Check formatting without modifying files

typecheck: typecheck-tgbot typecheck-front ## Run all configured type checkers

verify: verify-backend verify-tgbot verify-front ## Run all repository checks

install-backend: ## Install locked backend dependencies
	cd $(BACKEND_DIR) && $(UV) sync --dev --locked

run-backend: ## Run the FastAPI backend
	cd $(BACKEND_DIR) && $(UV) run python src/main.py

test-backend: ## Run backend tests
	cd $(BACKEND_DIR) && PYTHONPATH=.:src $(UV) run pytest

lint-backend: ## Run Ruff and WPS checks for the backend
	cd $(BACKEND_DIR) && $(UV) run ruff check --config ../ruff.toml .
	cd $(BACKEND_DIR) && $(UV) run flake8 --config ../.flake8 . --select=WPS

format-backend: ## Format backend code
	cd $(BACKEND_DIR) && $(UV) run ruff format --config ../ruff.toml .

format-check-backend: ## Check backend formatting without modifying files
	cd $(BACKEND_DIR) && $(UV) run ruff format --config ../ruff.toml --check .

verify-backend: lint-backend format-check-backend test-backend ## Run all configured backend checks

migrate-backend: ## Apply all backend database migrations
	cd $(BACKEND_DIR) && $(UV) run alembic upgrade head

migration-backend: ## Create a backend migration; pass message="description"
	@test -n "$(message)" || (echo 'Usage: make migration-backend message="migration description"' >&2; exit 2)
	cd $(BACKEND_DIR) && $(UV) run alembic revision --autogenerate -m "$(message)"

migration-check-backend: ## Check whether backend model changes need a migration
	cd $(BACKEND_DIR) && $(UV) run alembic check

install-tgbot: ## Install locked Telegram bot dependencies
	cd $(TGBOT_DIR) && $(UV) sync --dev --locked

run-tgbot-polling: ## Run the Telegram bot in polling mode
	cd $(TGBOT_DIR) && $(UV) run python src/run_polling.py

run-tgbot-webhook: ## Run the Telegram bot webhook application
	cd $(TGBOT_DIR) && $(UV) run python src/run_webhook.py

test-tgbot: ## Run Telegram bot tests
	cd $(TGBOT_DIR) && PYTHONPATH=src $(UV) run pytest

lint-tgbot: ## Run Ruff and WPS checks for the Telegram bot
	cd $(TGBOT_DIR) && $(UV) run ruff check --config ../ruff.toml .
	cd $(TGBOT_DIR) && $(UV) run flake8 --config ../.flake8 . --select=WPS

format-tgbot: ## Format Telegram bot code
	cd $(TGBOT_DIR) && $(UV) run ruff format --config ../ruff.toml .

format-check-tgbot: ## Check Telegram bot formatting without modifying files
	cd $(TGBOT_DIR) && $(UV) run ruff format --config ../ruff.toml --check .

typecheck-tgbot: ## Type-check the Telegram bot
	cd $(TGBOT_DIR) && MYPYPATH=src $(UV) run mypy --config-file ../mypy.ini --explicit-package-bases src

verify-tgbot: lint-tgbot format-check-tgbot typecheck-tgbot test-tgbot ## Run all Telegram bot checks

install-front: ## Install locked frontend dependencies
	$(NPM) --prefix $(FRONT_DIR) ci

run-front: ## Run the Vite frontend development server
	$(NPM) --prefix $(FRONT_DIR) run dev

lint-front: ## Run the frontend linter
	$(NPM) --prefix $(FRONT_DIR) run lint

typecheck-front: ## Type-check the frontend
	$(NPM) --prefix $(FRONT_DIR) run typecheck

build-front: ## Build the frontend production bundle
	$(NPM) --prefix $(FRONT_DIR) run build

verify-front: lint-front typecheck-front build-front ## Run all configured frontend checks

infra-up: ## Start local databases, identity provider, Redis, and NATS
	$(COMPOSE) -f $(COMPOSE_FILE) up -d $(INFRA_SERVICES)

infra-down: ## Stop the local Compose project without deleting volumes
	$(COMPOSE) -f $(COMPOSE_FILE) down

infra-logs: ## Follow local infrastructure logs
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f $(INFRA_SERVICES)
