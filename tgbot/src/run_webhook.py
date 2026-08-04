import asyncio
import contextlib

import uvicorn
from infra.logging import configure_logging
from infra.webhook.app import create_app


async def main() -> None:
    configure_logging()
    app = create_app()

    config = uvicorn.Config(
        app=app,
        host="0.0.0.0",  # ruff: ignore[hardcoded-bind-all-interfaces]
        port=8000,
        reload=False,
        log_level="info",
    )

    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
