# Deployment Agent Guide

## Scope

These instructions apply to `deploy/`. The current deployment artifact is
`deploy/local/docker-compose-full.yml`, a local integration topology. It is not a production deployment design.

Read `../ARCHITECTURE.md` before changing service relationships and `../DEVELOPMENT.md` before changing developer setup.
Also inspect the Dockerfile and environment/config loader of every affected application. The Compose file and actual
application code are authoritative when prose is stale.

## Local Topology

The Compose project contains:

- applications: `front` and `backend`;
- state and messaging: `backend-db`, `zitadel-db`, `redis`, and NATS JetStream;
- identity: `zitadel`;
- observability: `grafana`, `prometheus`, `otel-collector`, `tempo`, `loki`, `promtail`, and `cadvisor`.

All services share the `datingbot-local` network. Application build contexts are repository directories, while
monitoring configuration is mounted read-only from `monitoring/`.

## Change Rules

- Keep local-only assumptions explicit. Published ports, disabled TLS, development credentials, privileged cAdvisor,
  and Docker socket/host mounts must not be presented as production-safe defaults.
- Preserve service-name DNS contracts used by applications and monitoring. Renaming a service requires updating every
  dependent endpoint, scrape target, dashboard query, and document.
- Keep health checks aligned with real endpoints and runtime tools available in the image. `depends_on` readiness must
  not point at a nonexistent or unauthenticated endpoint.
- Keep application images built from their own directories. Do not copy source trees between services or share Python
  virtual environments.
- Add new persistent state as a named volume. Do not bind-mount secret files or developer home directories.
- Pin new third-party image versions. Do not silently upgrade existing images as part of an unrelated change.
- When changing ports, environment variables, health checks, volumes, or service dependencies, update
  `../DEVELOPMENT.md`, `../ARCHITECTURE.md`, and `../monitoring/README.md` where they describe the changed contract.
- Do not add a service merely because a placeholder module or unused adapter exists. A running dependency needs a
  concrete application use case.

## Environment and Secret Safety

- `deploy/local/.env.example` documents required variable names with empty or harmless placeholder values.
- `deploy/local/.env` is ignored and may contain real credentials. Never print, copy into output, commit, or rewrite its
  values.
- Preserve Compose required-value guards such as `${NAME:?message}` for credentials needed at startup.
- Use separate development passwords and a 32-character Zitadel master key. Never add fallback secrets to make Compose
  validation pass.
- Frontend build artifacts may contain only public configuration. Secrets belong in server-side runtime environments.

## Supported Workflows

Run commands from the repository root. Start only ordinary development infrastructure with:

```bash
make infra-up
make infra-logs
make infra-down
```

Start the complete local stack only when integration or observability behavior is in scope:

```bash
docker compose --env-file deploy/local/.env -f deploy/local/docker-compose-full.yml up -d
```

`make infra-down` intentionally preserves named volumes. Never use `down -v`, prune Docker resources, or remove database
volumes unless the user explicitly requests data deletion and the exact target has been verified.

## Validation

After editing Compose, render and validate the merged configuration without starting services:

```bash
docker compose --env-file deploy/local/.env -f deploy/local/docker-compose-full.yml config
```

If no populated local environment exists, do not invent credentials; report that interpolation validation could not be
completed. When the task requires a runtime check, build or start only the affected services, inspect their health and
logs, and stop them without deleting volumes. Report image pulls, unavailable ports, missing credentials, or host-mount
limitations as environment constraints rather than weakening the configuration.
