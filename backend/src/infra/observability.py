import os

TRUTHY = {"1", "true", "yes", "on", "enabled"}
FALSY = {"0", "false", "no", "off", "disabled"}
OBSERVABILITY_ENVIRONMENTS = {"prod", "production", "staging"}


def is_observability_enabled() -> bool:
    value = os.getenv("OBSERVABILITY_ENABLED")
    if value is not None:
        normalized = value.strip().lower()
        if normalized in TRUTHY:
            return True
        if normalized in FALSY:
            return False

    app_env = os.getenv("APP_ENV") or os.getenv("ENVIRONMENT") or "local"
    return app_env.strip().lower() in OBSERVABILITY_ENVIRONMENTS


def otlp_endpoint() -> str:
    return os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "localhost:4317")


def service_name(default: str) -> str:
    return os.getenv("OTEL_SERVICE_NAME", default)
