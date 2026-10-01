# Backend Agent Guide

## Scope

These instructions apply to everything under `backend/`. Markdown links resolve from this directory; commands below run
from the repository root.

Before changing behavior, read the files being changed, their tests, and one nearby implementation that solves a
similar problem. Use these documents only when the task needs them:

- `../ARCHITECTURE.md` for runtime relationships, module boundaries, persistence, authentication, and known gaps;
- `../DEVELOPMENT.md` for local setup and environment variables;
- `../arch/product/glossary.md` and the relevant product document when domain meaning changes;
- `../Makefile` for supported commands.

Executable code, `pyproject.toml`, `uv.lock`, migrations, and deployment configuration take precedence over stale prose.
If a backend change makes documentation inaccurate, update the owning document in the same change.

## Runtime and Layout

- Python 3.13 and the locked `uv` environment are required.
- `src/main.py` is the process entry point and application factory.
- `src/presentation/rest/` owns FastAPI routes, HTTP DTOs, middleware, and exception-to-response translation.
- `src/module/<name>/` owns product modules. Only `auth` currently contains implemented behavior; the other package
  names are placeholders, not approved interfaces or requirements.
- `src/infra/` owns cross-cutting adapters: database setup, Dishka composition, logging, and observability.
- `src/infra/db/migrations/` is the Alembic migration tree.
- `tests/` mirrors behavior by test level. Pytest loads `tests.fixtures.db` from `tests/conftest.py`.

Application imports assume `backend/src` is on `PYTHONPATH`. Follow the Makefile commands instead of changing imports or
test discovery to compensate for an incorrectly launched command.

## Architecture Boundaries

Keep the dependency direction:

```text
presentation -> application/domain interfaces <- infrastructure adapters
```

- Keep controllers thin: validate and translate HTTP data, call an application operation, and translate the result.
- Do not put SQLAlchemy queries, provider-specific token handling, or product decisions in controllers.
- Define request and response contracts in `presentation/rest/dto`; preserve existing public HTTP behavior unless the
  task explicitly changes the contract.
- Register dependencies through Dishka providers in `infra/ioc`; do not construct sessions, repositories, or external
  clients inside controllers.
- Keep async I/O async. Do not perform network, database, or environment-dependent work at import time.
- Translate expected domain/authentication failures in the presentation layer. Do not leak provider responses,
  credentials, SQL details, or stack traces to clients.
- The auth module is transitional: `AuthService` currently imports concrete infrastructure classes, and
  `AuthRepository` currently commits directly. Do not spread those dependencies to new modules. Introduce an
  application-owned interface when a real second adapter or focused test double requires it, and move transaction
  ownership to the application/unit-of-work seam before adding a multi-repository or multi-write operation.

## Database and Migrations

- Use async SQLAlchemy and the request-scoped `AsyncSession` provided by Dishka.
- Every schema change requires an Alembic migration. Never rely on model metadata alone to update a database.
- Inspect existing revisions before choosing a revision dependency, identifier, table name, constraint name, or data
  migration style.
- Keep migrations reviewable and deterministic. Do not read application secrets or call external services from a
  migration.
- Do not delete, reset, or recreate a developer database or volume unless the user explicitly requests it.

Run migration commands from the repository root:

```bash
make migration-check-backend
make migration-backend message="short description"
make migrate-backend
```

Migration creation and application require a configured database. If it is unavailable, report exactly which check was
not run; do not claim the migration was exercised.

## Tests and Checks

For a behavior change, add or update tests at the narrowest useful level. For a bug fix, reproduce the failure first
when practical. Do not make live Zitadel, Telegram, or other network calls in ordinary tests; use explicit fakes at the
external boundary.

Run from the repository root:

```bash
make test-backend
make lint-backend
make format-check-backend
make verify-backend
```

Use `make format-backend` only when formatting changes are intended. The backend has no configured type checker, so do
not borrow the Telegram environment or invent a backend type-check command. Run the smallest relevant test first, then
`make verify-backend` before handoff when the environment permits it.

## Configuration, Security, and Telemetry

- Keep real values in ignored `backend/.env` or `deploy/local/.env` files. Commit only placeholders and variable names.
- Validate all external input, but treat validation and authorization as separate concerns.
- Never log tokens, authorization headers, Telegram payload hashes, passwords, message text, or unnecessary personal
  data.
- Metric and log labels must be bounded. Do not use user IDs, identity subjects, request IDs, chat IDs, raw URLs with
  identifiers, exception messages, or other unbounded values as labels.
- Observability is optional locally. `/metrics` exists only when observability is enabled; the health endpoint is
  `/api/v1/healthcheck/`.
- Preserve structured logging and trace context when changing middleware. Keep health and metrics traffic excluded from
  high-volume tracing where configured.
