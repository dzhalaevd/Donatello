import logging

from aiogram import (
    Bot,
    exceptions,
    types,
)

logger = logging.getLogger(__name__)


async def set_user_commands(bot: Bot, user_id: int, commands: list[types.BotCommand]) -> None:
    try:
        await bot.set_my_commands(commands=commands, scope=types.BotCommandScopeChat(chat_id=user_id))
    except exceptions.TelegramAPIError:
        logger.exception("%s: Commands are not installed", user_id)


async def set_default_commands(bot: Bot, _admin_ids: list[int]) -> None:
    default_commands = [
        types.BotCommand(command="start", description="🟢 Запустить бота"),
    ]

    await bot.set_my_commands(default_commands, scope=types.BotCommandScopeDefault())
