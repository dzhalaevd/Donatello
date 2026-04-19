from aiogram.filters import (
    BaseFilter,
)
from aiogram.types import (
    Message,
)


class ChatTypeFilter(BaseFilter):
    def __init__(self, chat_type: str | list[str]) -> None:
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:
        if isinstance(self.chat_type, str):
            return bool(message.chat.type == self.chat_type)
        return bool(message.chat.type in self.chat_type)
