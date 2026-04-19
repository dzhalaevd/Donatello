from typing import (
    Any,
)

from aiogram.dispatcher.middlewares import (
    BaseMiddleware,
)
from aiogram.types.base import (
    TelegramObject,
)
from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler,
)
from bot_types import (
    Handler,
)


class SchedulerMiddleware(BaseMiddleware):
    def __init__(self, scheduler: AsyncIOScheduler) -> None:
        super().__init__()
        self.scheduler = scheduler

    def __call__(
        self,
        handler: Handler,
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        data["appscheduler"] = self.scheduler
        return handler(event, data)
