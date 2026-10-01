# Monitoring Agent Guide

## Scope

These instructions apply to `monitoring/`. This directory owns the local observability configuration; service lifecycle,
ports, image versions, volumes, and mounts are owned by `deploy/local/docker-compose-full.yml`.

Read `../ARCHITECTURE.md` for the real telemetry flow and known application gaps, `README.md` for operator-facing usage,
and the emitting application code before changing a metric, label, trace attribute, or log field. Executable code and
configuration take precedence over stale README examples.

## Signal Flow and Ownership

```text
application OTLP -> OpenTelemetry Collector -> Tempo and Prometheus exporter
application /metrics ------------------------> Prometheus
Docker logs -> Promtail -> Loki
container metrics -> cAdvisor -> Prometheus
Prometheus + Loki + Tempo -------------------> Grafana
```

- `otel-collector/` owns OTLP receivers, processors, and exporters.
- `prometheus/` owns scrape targets and alert rules.
- `loki/` owns local log storage; `promtail/` owns Docker discovery, labels, and shipping.
- `tempo/` owns local trace storage and trace-derived metrics settings.
- `grafana/provisioning/` owns data-source and dashboard provisioning.
- `grafana/dashboards/` contains the version-controlled dashboard definitions. Preserve stable dashboard and data-source
  UIDs so links, exemplars, and provisioning remain connected.

This is a single-node development stack with local filesystem storage and short-lived data. Do not infer production
retention, availability, authentication, or capacity guarantees from it.

## Current Contracts and Known Gaps

- The backend exposes `/metrics` only when observability is enabled and health at `/api/v1/healthcheck/`.
- Prometheus currently scrapes `backend:8000`, `otel-collector:9464`, and `cadvisor:8080`.
- Frontend application telemetry is not implemented. Its dashboard currently uses container metrics and logs only.
- Grafana correlation depends on consistent `trace_id`/`traceid` fields and the provisioned data-source UIDs.

When an application contract changes, update the emitter, scrape/export configuration, dashboards, alerts,
`README.md`, and `../ARCHITECTURE.md` together as applicable.

## Telemetry Design Rules

- Prefer a small stable set of signals tied to an operator action. Every alert should describe a real failure mode and
  every dashboard panel should answer a concrete question.
- Keep metric and log labels low-cardinality and bounded. Allowed Docker discovery labels are currently `service`,
  `container`, `compose_project`, `environment`, and `stream`.
- Never add personal data, user or chat IDs, identity subjects, request IDs, tokens, raw paths containing identifiers,
  message text, payment data, exception messages, or arbitrary URLs as labels.
- Sensitive values do not belong in metric samples, log bodies, trace attributes, dashboard variables, annotations, or
  alert text.
- Use normalized route templates for HTTP metrics. Preserve metric names and label keys consumed by dashboards and
  alerts, or update every consumer in the same change.
- Keep the collector's `memory_limiter` before batching, and retain batching for exported signals unless a measured
  problem justifies a change.
- Avoid duplicate ingestion: distinguish direct Prometheus scraping from OTLP metrics exported through the collector
  before enabling both for the same instrument.
- Promtail reads the Docker socket and host log paths; treat that access as privileged and local-only.

## Dashboards and Alerts

- Edit provisioned JSON files, not only a live Grafana instance. UI changes are ephemeral unless exported back to the
  repository and reviewed.
- Keep PromQL and LogQL selectors consistent with configured `job`, `service`, and `environment` labels.
- Preserve units, legends, query windows, and thresholds unless the task intentionally changes their meaning.
- Alert expressions must use metrics that are actually emitted. Include an actionable summary and description, and
  choose a `for` duration that avoids transient startup noise.
- Do not silence a broken scrape or missing signal by weakening an alert. Fix the producer/target or document the known
  gap.

## Validation

At minimum after a change:

1. Parse every edited YAML or JSON file.
2. Render the Compose configuration from the repository root:

   ```bash
   docker compose --env-file deploy/local/.env -f deploy/local/docker-compose-full.yml config
   ```

3. Check that scrape targets, ports, service names, data-source UIDs, metric names, and dashboard label selectors agree
   across all affected files.

When Docker and credentials are available and runtime behavior is in scope, start only the affected observability
services, inspect their logs/readiness, load Prometheus rules, and confirm the relevant Grafana query returns the
expected series. Do not claim live validation when only syntax or static cross-checks were performed. Never delete
monitoring volumes to repair a configuration problem without explicit user authorization.
