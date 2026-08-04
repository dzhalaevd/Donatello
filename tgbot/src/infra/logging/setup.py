import logging
import sys
from typing import TYPE_CHECKING

import structlog
from structlog.processors import CallsiteParameter, CallsiteParameterAdder

from .processors import get_render_processor

if TYPE_CHECKING:
    from structlog.typing import Processor

DEFAULT_EXCLUDED_ACCESS_LOG_PATHS = ("/metrics",)


class EndpointFilter(logging.Filter):
    """Filters noisy Uvicorn access logs before structlog renders them."""

    def __init__(self, excluded_paths: tuple[str, ...] = DEFAULT_EXCLUDED_ACCESS_LOG_PATHS) -> None:
        super().__init__()
        self.excluded_paths = excluded_paths

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage()
        return not any(_contains_access_log_path(message, path) for path in self.excluded_paths)


def configure_logging(
    log_level: int = logging.INFO,
    render_json_logs: bool = False,
) -> None:
    """Настраивает систему логирования приложения.

    Вдохновился: https://gist.github.com/nkhitrov/38adbb314f0d35371eba4ffb8f27078f.

    :param render_json_logs: Выводить логи в json или нет
    :param log_level: Уровень логирования.
    """
    colors = not render_json_logs

    for logger_name in ("sqlalchemy", "sqlalchemy.engine"):
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.propagate = True

    common_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.ExtraAdder(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=False),
        CallsiteParameterAdder(
            {
                CallsiteParameter.LINENO,
                CallsiteParameter.PROCESS_NAME,
                CallsiteParameter.THREAD_NAME,
            },
        ),
    ]

    structlog_processors: list[Processor] = [
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=common_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            get_render_processor(
                render_json_logs=render_json_logs,
                colors=colors,
            ),
        ],
    )

    handlers: list[logging.Handler] = []

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    logging.basicConfig(handlers=handlers, level=log_level)
    configure_access_log_filter()

    structlog.configure(
        processors=common_processors + structlog_processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # На случай, если какая-нибудь библиотека будет шуметь, то вместо None, можно прописать
    # типа "uvicorn.error"
    for name in [None]:
        if name:
            logging.getLogger(name).setLevel(logging.WARNING)


def configure_access_log_filter(
    excluded_paths: tuple[str, ...] = DEFAULT_EXCLUDED_ACCESS_LOG_PATHS,
) -> None:
    access_logger = logging.getLogger("uvicorn.access")
    if not any(
        isinstance(existing_filter, EndpointFilter) and existing_filter.excluded_paths == excluded_paths
        for existing_filter in access_logger.filters
    ):
        access_logger.addFilter(EndpointFilter(excluded_paths))


def _contains_access_log_path(message: str, path: str) -> bool:
    return f" {path} " in message or f" {path}?" in message
