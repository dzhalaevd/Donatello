# Local Monitoring

This directory contains the local/dev observability stack for DatingBot.

## Stack

- Grafana for dashboards
- Prometheus for metrics
- OpenTelemetry Collector for OTLP metrics and traces
- Tempo for distributed traces
- Loki for logs
- Promtail for Docker log collection
- cAdvisor for container CPU, memory and network metrics

## Run

Regular local development does not require this stack. Run the default
infrastructure only with:

```bash
docker compose -f compose-dev.yml up -d
```

Start observability only when you need metrics, traces, dashboards or log search:

```bash
docker compose -f compose-dev.yml -f compose-monitoring.yml up -d
```

Then open:

- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- OpenTelemetry Collector OTLP gRPC: http://localhost:4317
- OpenTelemetry Collector OTLP HTTP: http://localhost:4318
- OpenTelemetry Collector Prometheus export: http://localhost:9464/metrics
- Tempo: http://localhost:3200
- cAdvisor: http://localhost:8081

Grafana uses these default local credentials unless overridden:

```dotenv
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=
```

## Application Metrics

Prometheus scrapes:

- `otel-collector:9464/metrics`
- `backend:8000/metrics`
- `tgbot:8000/metrics`
- `cadvisor:8080/metrics`

The current `compose-dev.yml` defines infrastructure services only. If backend,
tgbot or frontend are run outside Docker, adjust `monitoring/prometheus/prometheus.yml`
or add application services with the same Docker service names.

Backend endpoints:

- `GET /health`
- `GET /metrics`

Telegram bot webhook endpoints:

- `GET /health`
- `GET /metrics`

## OpenTelemetry Auto-Instrumentation

Backend and Telegram bot include OpenTelemetry packages so they can be started
with zero-code instrumentation.

Observability is disabled by default for local development. It is enabled when:

- `OBSERVABILITY_ENABLED=true`, or
- `APP_ENV` / `ENVIRONMENT` is `prod`, `production` or `staging`.

Set `OBSERVABILITY_ENABLED=false` to force-disable it in any environment.

Inside Docker Compose, use the collector endpoint:

```dotenv
OBSERVABILITY_ENABLED=true
APP_ENV=dev
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_METRICS_EXPORTER=otlp
OTEL_TRACES_EXPORTER=otlp
OTEL_LOGS_EXPORTER=none
OTEL_PROPAGATORS=tracecontext,baggage
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=dev
OTEL_PYTHON_LOG_CORRELATION=true
OTEL_PYTHON_EXCLUDED_URLS=/health,/metrics
```

Backend example:

```bash
cd backend
OBSERVABILITY_ENABLED=true OTEL_SERVICE_NAME=backend opentelemetry-instrument python src/main.py
```

Telegram webhook example:

```bash
cd tgbot
OBSERVABILITY_ENABLED=true OTEL_SERVICE_NAME=tgbot opentelemetry-instrument python src/run_webhook.py
```

For local runs outside Docker, point the exporter at localhost:

```dotenv
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

The direct `/metrics` endpoints remain available for simple Prometheus scraping,
while OpenTelemetry data flows through the collector and is exported back to
Prometheus on `otel-collector:9464`. Traces are exported from the collector to
Tempo.

This mirrors the `blueswen/fastapi-observability` layout at the infrastructure
level: Grafana, Prometheus, Loki and Tempo are wired together, and Prometheus is
started with exemplar storage enabled so metric samples can link to traces when
the exporter provides exemplars.

## Signal Correlation

Grafana provisions:

- Prometheus exemplar links to Tempo.
- Loki derived fields for `trace_id` and `traceid`.
- Tempo trace-to-logs links back to Loki.

For trace ids to appear in logs, start Python services with
`OTEL_PYTHON_LOG_CORRELATION=true`. Structured `structlog` output may need an
extra processor later if we want every JSON log to carry `trace_id` and `span_id`
as dedicated fields.

## Dashboards

Grafana provisions these dashboards automatically:

- Backend Overview
- Telegram Bot Overview
- Frontend Overview
- Docker / Containers Overview

## Logging

Promtail discovers Docker containers through the Docker socket and sends logs to
Loki with low-cardinality labels:

- `service`
- `container`
- `compose_project`
- `environment`
- `stream`

Do not add personal data, request ids, user ids, chat ids, tokens, raw paths with
IDs, message text or payment data as Loki labels.

## Alerts

Base Prometheus rules live in `monitoring/prometheus/rules/` and currently cover:

- backend scrape failure
- Telegram bot scrape failure
- backend 5xx error rate
