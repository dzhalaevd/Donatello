# syntax=docker/dockerfile:1

FROM ghcr.io/astral-sh/uv:0.6.14 AS uv

FROM python:3.13-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv

WORKDIR /app

COPY --from=uv /uv /uvx /bin/
COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project


FROM python:3.13-slim AS runtime

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/app/src" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 10001 app

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY --chown=app:app alembic.ini ./
COPY --chown=app:app src ./src

USER app

EXPOSE 8000

CMD ["uvicorn", "main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000"]
