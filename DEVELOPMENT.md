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

Both Python services require Python 3.13:

- `backend` requires Python `>=3.13`
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

Create the ignored local environment file before starting Compose:

```bash
cp deploy/local/.env.example deploy/local/.env
```

Fill every password field in `deploy/local/.env`. Generate a 32-character Zitadel master key with
`openssl rand -hex 16` and generate independent passwords rather than reusing one value across services.

The `infra-up` target selects infrastructure services from the full local Compose file:

- `backend-db` on `localhost:5432`
- `zitadel` on `localhost:8080`
- `zitadel-db` for Zitadel storage
- `redis` on `localhost:6379`
- `nats` on `localhost:4222`

Run:

```bash
make infra-up
```

Stop it with:

```bash
make infra-down
```

Local Zitadel credentials come from `deploy/local/.env`:

```text
URL: http://localhost:8080
Username: admin
Password: value of ZITADEL_ADMIN_PASSWORD
```

Local backend database defaults from `deploy/local/docker-compose-full.yml`:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=backend
POSTGRES_PASSWORD=
POSTGRES_DB=backend
```

## Backend

Create `backend/.env` with the variables used by the current backend config:

```dotenv
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=backend
POSTGRES_PASSWORD=
POSTGRES_DB=backend

ZITADEL_ISSUER=http://localhost:8080
ZITADEL_REDIRECT_URI=http://localhost:8000/api/v1/auth/callback
ZITADEL_CLIENT_ID=
ZITADEL_CLIENT_SECRET=
ZITADEL_AUDIENCE=

TELEGRAM_BOT_TOKEN=
TELEGRAM_AUTH_TTL_SECONDS=86400
```

Install dependencies and run from the repository root:

```bash
make install-backend
make run-backend
```

Open:

- API docs: http://localhost:8000/
- Healthcheck: http://localhost:8000/api/v1/healthcheck

### Backend Migrations

Migration files live in `backend/src/infra/migrations`.

Before relying on Alembic commands, verify that `backend/alembic.ini` points to the current migration path and database URL. The repository currently has infrastructure for Alembic, but the config may need syncing with the current module layout before `alembic upgrade head` is used in a fresh environment.

The local database URL is assembled from the `POSTGRES_*` values in `deploy/local/.env`.

```text
postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}
```

Migration commands are exposed through the root Makefile:

```bash
make migrate-backend
make migration-check-backend
make migration-backend message="add user status"
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
make install-tgbot
make run-tgbot-polling
```

Run webhook app:

```bash
make run-tgbot-webhook
```

The webhook app listens on `http://localhost:8000` by default, so do not run it on the same port as the backend unless you change one of the ports.

## Frontend

Install and run:

```bash
make install-front
make run-front
```

Open:

- http://localhost:5173/

Other commands:

```bash
make lint-front
make typecheck-front
make build-front
```

The frontend is currently a Vite/React shell. Treat it as the product UI surface, but expect application screens to be built out over time.

## Observability

Regular local development does not require the monitoring stack.

Start infrastructure plus observability:

The available local Compose file contains the full application and monitoring stack. Start it directly when all
services are required:

```bash
docker compose --env-file deploy/local/.env -f deploy/local/docker-compose-full.yml up -d
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
GRAFANA_ADMIN_PASSWORD=
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

Run all configured read-only checks:

```bash
make verify
```

Or run checks for one application area:

```bash
make verify-backend
make verify-tgbot
make verify-front
```

Formatting is intentionally separate because it changes files:

```bash
make format
make format-check
```

The frontend currently has no test script. The backend currently has no declared mypy dependency, so its verification
does not claim to run type checking. `make help` lists the complete supported command API.

GitHub Actions CI uses these same `make verify-*` targets and runs only the application areas affected by a change.
For branch protection, configure `CI success` as the single required check; it accepts application jobs that were
legitimately skipped by the path filters and fails when any job that did run was unsuccessful.

Repository hooks:

```bash
pre-commit install
pre-commit run --all-files
make verify-pre-commit
```

`make verify-pre-commit` uses the Telegram bot's locked `uv` environment for the pre-commit executable. GitHub Actions
installs the Telegram bot and frontend dependencies before running the same repository-wide target as a required CI
gate.

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
