# Development

This guide describes how to run the current DatingBot / Make Dating Free Again repository locally.

The project is in transition from an older Telegram-only dating bot into a multi-surface product with backend, Telegram bot, frontend and observability services. Prefer the commands in this document over older Django-era instructions.

## Prerequisites

Install:

- Docker with Docker Compose
- Python runtime managed by `uv`
- Node.js and npm for the frontend
- Git
- A Telegram bot token if you run `tgbot`

Python versions currently differ by service:

- `backend` requires Python `>=3.11`
- `tgbot` requires Python `>=3.13,<4.0`

## Repository Layout

```text
backend/      FastAPI API, auth, database access and migrations
tgbot/        Telegram bot and webhook service
front/        React + Vite frontend
monitoring/   Grafana, Prometheus, Loki, Tempo, OpenTelemetry Collector
arch/         Product and architecture notes
```

## Start Local Infrastructure

The development compose file starts infrastructure only:

- `backend-db` on `localhost:5432`
- `zitadel` on `localhost:8080`
- `zitadel-db` for Zitadel storage

Run:

```bash
docker compose -f compose-dev.yml up -d
```

Stop it with:

```bash
docker compose -f compose-dev.yml down
```

Local Zitadel defaults from `compose-dev.yml`:

```text
URL: http://localhost:8080
Username: admin
Password: Admin123!
```

Local backend database defaults from `compose-dev.yml`:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=backend
POSTGRES_PASSWORD=backend
POSTGRES_DB=backend
```

## Backend

Create `backend/.env` with the variables used by the current backend config:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=backend
POSTGRES_PASSWORD=backend
POSTGRES_DB=backend

ZITADEL_ISSUER=http://localhost:8080
ZITADEL_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback
ZITADEL_CLIENT_ID=
ZITADEL_CLIENT_SECRET=
ZITADEL_AUDIENCE=

TELEGRAM_BOT_TOKEN=
TELEGRAM_AUTH_TTL_SECONDS=86400
```

Install dependencies and run:

```bash
cd backend
uv sync --dev
uv run python src/main.py
```

Open:

- API docs: http://localhost:8000/
- Healthcheck: http://localhost:8000/api/v1/healthcheck

### Backend Migrations

Migration files live in `backend/src/infra/migrations`.

Before relying on Alembic commands, verify that `backend/alembic.ini` points to the current migration path and database URL. The repository currently has infrastructure for Alembic, but the config may need syncing with the current module layout before `alembic upgrade head` is used in a fresh environment.

Expected database URL for the local compose database:

```text
postgresql+asyncpg://backend:backend@localhost:5432/backend
```

## Telegram Bot

Create `tgbot/.env`:

```dotenv
BOT_TOKEN=
ADMINS=
USE_REDIS=false
```

The legacy example also contains variables for database, Redis, maps and payments. The current `load_config()` path used by polling reads only bot token, admins and Redis usage; add the other variables only when working on features that require them.

Run polling mode:

```bash
cd tgbot
uv sync --dev
uv run python src/run_polling.py
```

Run webhook app:

```bash
cd tgbot
uv sync --dev
uv run python src/run_webhook.py
```

The webhook app listens on `http://localhost:8000` by default, so do not run it on the same port as the backend unless you change one of the ports.

## Frontend

Install and run:

```bash
cd front
npm install
npm run dev
```

Open:

- http://localhost:5173/

Other commands:

```bash
npm run lint
npm run build
npm run preview
```

The frontend is currently a Vite/React shell. Treat it as the product UI surface, but expect application screens to be built out over time.

## Observability

Regular local development does not require the monitoring stack.

Start infrastructure plus observability:

```bash
docker compose -f compose-dev.yml -f compose-monitoring.yml up -d
```

Open:

- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- Tempo: http://localhost:3200
- Loki: http://localhost:3100
- OpenTelemetry Collector gRPC: http://localhost:4317
- OpenTelemetry Collector HTTP: http://localhost:4318
- cAdvisor: http://localhost:8081

Grafana defaults:

```dotenv
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=admin
```

Enable app instrumentation with:

```dotenv
OBSERVABILITY_ENABLED=true
APP_ENV=dev
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_METRICS_EXPORTER=otlp
OTEL_TRACES_EXPORTER=otlp
OTEL_LOGS_EXPORTER=none
OTEL_PROPAGATORS=tracecontext,baggage
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=dev
OTEL_PYTHON_LOG_CORRELATION=true
OTEL_PYTHON_EXCLUDED_URLS=/health,/metrics,/api/v1/healthcheck
```

More details are in [monitoring/README.md](monitoring/README.md).

## Tests And Checks

Backend:

```bash
cd backend
uv run pytest
uv run ruff format .
uv run ruff check .
uv run mypy .
```

Telegram bot:

```bash
cd tgbot
uv run pytest
uv run ruff format .
uv run ruff check .
uv run mypy .
```

Frontend:

```bash
cd front
npm run lint
npm run build
```

Repository hooks:

```bash
pre-commit install
pre-commit run --all-files
```

Note: the current pre-commit config still references `frontend/` in a few frontend hooks, while the actual directory is `front/`. Update those hooks before depending on frontend pre-commit checks.

## Localization

Telegram bot translations live in `tgbot/locales`.

Extract and update messages:

```bash
cd tgbot
uv run pybabel extract -F babel.cfg -o locales/dating.pot .
uv run pybabel update -d locales -D dating -i locales/dating.pot
```

Compile translations:

```bash
cd tgbot
uv run pybabel compile -d locales -D dating
```
