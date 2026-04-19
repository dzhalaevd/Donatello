import asyncio
import contextlib
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI
from infra.logging import configure_logging
from infra.observability import is_observability_enabled, otlp_endpoint, service_name
from presentation.rest import setup_exception_handlers, setup_middlewares, setup_otlp, setup_routes

logger = structlog.stdlib.get_logger()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    yield


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(
        title="DatingBot Backend",
        version="0.1.0",
        swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"},
        lifespan=lifespan,
        docs_url="/",
    )

    observability_enabled = is_observability_enabled()

    setup_middlewares(app, observability_enabled=observability_enabled)
    setup_exception_handlers(app)
    setup_routes(app, observability_enabled=observability_enabled)

    if observability_enabled:
        setup_otlp(app, service_name("backend"), otlp_endpoint())
        logger.info("Observability enabled", otlp_endpoint=otlp_endpoint())
    else:
        logger.info("Observability disabled")

    return app


async def start_server(app: FastAPI) -> None:
    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",  # noqa: S104
        port=8000,
        reload=True,
        use_colors=True,
        log_level="debug",
        forwarded_allow_ips="*",
    )
    server = uvicorn.Server(config=config)
    logger.info("Starting server")
    await server.serve()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        application = create_app()
        with asyncio.Runner() as runner:
            runner.run(start_server(application))
