import structlog
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from infra.ioc import create_container
from module.auth.infra.oidc import (
    AuthError,
    IdentityConflict,
    IdentityNotFound,
    InvalidCredentials,
    LastIdentityRemoval,
    UserForbidden,
)
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from .controllers import auth_router, healthcheck_router
from .middlewares.logging import logging_middleware
from .middlewares.metrics import PrometheusMiddleware, metrics_router

logger = structlog.get_logger(__name__)


async def unknown_exception_handler(_request: Request, err: Exception) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        {"detail": "Internal server error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def auth_error_handler(_request: Request, err: AuthError) -> ORJSONResponse:
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(err, InvalidCredentials):
        status_code = status.HTTP_401_UNAUTHORIZED
    elif isinstance(err, UserForbidden):
        status_code = status.HTTP_403_FORBIDDEN
    elif isinstance(err, (IdentityConflict, LastIdentityRemoval)):
        status_code = status.HTTP_409_CONFLICT
    elif isinstance(err, IdentityNotFound):
        status_code = status.HTTP_404_NOT_FOUND

    return ORJSONResponse({"detail": str(err)}, status_code=status_code)


def setup_routes(app: FastAPI, *, observability_enabled: bool = False) -> None:
    prefix = "/api/v1"

    setup_dishka(create_container(), app)
    app.include_router(auth_router, prefix=f"{prefix}/auth", tags=["Authorization"])
    app.include_router(healthcheck_router, prefix=f"{prefix}/healthcheck", tags=["Healthcheck"])
    if observability_enabled:
        app.add_route("/metrics", metrics_router)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AuthError, auth_error_handler)
    app.add_exception_handler(Exception, unknown_exception_handler)


def setup_middlewares(app: FastAPI, *, observability_enabled: bool = False) -> None:
    app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
    if observability_enabled:
        app.add_middleware(PrometheusMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_otlp(app: FastAPI, app_name: str, endpoint: str, log_correlation: bool = True) -> None:
    resource = Resource.create(attributes={"service.name": app_name})

    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    tracer.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True)))

    if log_correlation:
        LoggingInstrumentor().instrument(set_logging_format=True)

    FastAPIInstrumentor.instrument_app(app, tracer_provider=tracer)


__all__ = (
    "setup_exception_handlers",
    "setup_middlewares",
    "setup_otlp",
    "setup_routes",
)
