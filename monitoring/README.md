# Local Monitoring

This directory contains the local development observability stack for DatingBot.

## Stack

- Grafana for dashboards
- Prometheus for metrics and alert rules
- OpenTelemetry Collector for OTLP metrics and traces
- Tempo for distributed traces
- Loki for logs
- Promtail for Docker log collection
- cAdvisor for container CPU, memory, and network metrics

## Run

Regular local development does not require this stack. Start the full local topology from the repository root when you
need metrics, traces, dashboards, or log search:

```bash
docker compose --env-file deploy/local/.env -f deploy/local/docker-compose-full.yml up -d
```

Then open:

- Grafana: http://localhost:3000
- Prometheus: http://localhost:9090
- OpenTelemetry Collector OTLP gRPC: http://localhost:4317
- OpenTelemetry Collector OTLP HTTP: http://localhost:4318
- OpenTelemetry Collector Prometheus export: http://localhost:9464/metrics
- Tempo: http://localhost:3200
- cAdvisor: http://localhost:8081

Grafana credentials come from `deploy/local/.env`:

```dotenv
GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=
```

## Application Metrics

Prometheus scrapes:

- `otel-collector:9464/metrics`
- `backend:8000/metrics`
- `cadvisor:8080/metrics`

The backend exposes:

- `GET /api/v1/healthcheck/`
- `GET /metrics` when observability is enabled

If the backend runs outside Docker, update `monitoring/prometheus/prometheus.yml` or make the process reachable under the
configured service name.

## OpenTelemetry Instrumentation

Observability is disabled by default for local development. It is enabled when:

- `OBSERVABILITY_ENABLED=true`, or
- `APP_ENV` / `ENVIRONMENT` is `prod`, `production`, or `staging`.

Set `OBSERVABILITY_ENABLED=false` to force-disable it in any environment. Inside Docker Compose, use the collector
endpoint:

```dotenv
OBSERVABILITY_ENABLED=true
APP_ENV=dev
OTEL_SERVICE_NAME=backend
OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
OTEL_EXPORTER_OTLP_PROTOCOL=grpc
OTEL_METRICS_EXPORTER=otlp
OTEL_TRACES_EXPORTER=otlp
OTEL_LOGS_EXPORTER=none
OTEL_PROPAGATORS=tracecontext,baggage
OTEL_RESOURCE_ATTRIBUTES=deployment.environment=dev
OTEL_PYTHON_LOG_CORRELATION=true
OTEL_PYTHON_EXCLUDED_URLS=/metrics,/api/v1/healthcheck
```

For local runs outside Docker, point `OTEL_EXPORTER_OTLP_ENDPOINT` at `http://localhost:4317`.

The direct `/metrics` endpoint remains available for Prometheus scraping, while OTLP data flows through the collector.
The collector exports metrics on `otel-collector:9464` and traces to Tempo. Avoid enabling duplicate instruments through
both paths.

## Signal Correlation

Grafana provisions:

- Prometheus exemplar links to Tempo;
- Loki derived fields for `trace_id` and `traceid`;
- Tempo trace-to-logs links back to Loki.

For trace IDs to appear in logs, use `OTEL_PYTHON_LOG_CORRELATION=true`. Structured `structlog` output may require an
additional processor before every JSON event carries `trace_id` and `span_id` as dedicated fields.

## Dashboards

Grafana provisions these dashboards automatically:

- Backend Overview
- Frontend Overview
- Docker / Containers Overview

Frontend application telemetry is not implemented; its dashboard uses container metrics and logs.

## Logging

Promtail discovers Docker containers through the Docker socket and sends logs to Loki with low-cardinality labels:

- `service`
- `container`
- `compose_project`
- `environment`
- `stream`

Do not add personal data, request IDs, user or chat IDs, tokens, raw paths with IDs, message text, or payment data as
Loki labels.

## Alerts

Base Prometheus rules live in `monitoring/prometheus/rules/` and currently cover:

- backend scrape failure;
- backend 5xx error rate.
