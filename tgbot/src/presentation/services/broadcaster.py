import asyncio
import logging

from aiogram import Bot, exceptions
from aiogram.types import InlineKeyboardMarkup

logger = logging.getLogger(__name__)


async def send_message(
    bot: Bot,
    user_id: int | str,
    text: str,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
) -> bool:
    """Safe messages sender.

    :param bot: Bot instance.
    :param user_id: user id. If str - must contain only digits.
    :param text: text of the message.
    :param disable_notification: disable notification or not.
    :param reply_markup: reply markup.

    Returns:
        Whether the message was sent successfully.
    """
    try:
        await bot.send_message(
            user_id,
            text,
            disable_notification=disable_notification,
            reply_markup=reply_markup,
        )
    except exceptions.TelegramBadRequest:
        logger.exception("Telegram server says - Bad Request: chat not found")
    except exceptions.TelegramForbiddenError:
        logger.exception("Target [ID:%s]: got TelegramForbiddenError", user_id)
    except exceptions.TelegramRetryAfter as e:
        logger.exception("Target [ID:%s]: Flood limit is exceeded. Sleep %s seconds.", user_id, e.retry_after)
        await asyncio.sleep(e.retry_after)
        return await send_message(bot, user_id, text, disable_notification, reply_markup)  # Recursive call
    except exceptions.TelegramAPIError:
        logger.exception("Target [ID:%s]: failed", user_id)
    else:
        logger.info("Target [ID:%s]: success", user_id)
        return True
    return False


async def broadcast(
    bot: Bot,
    users: list[str | int],
    text: str,
    disable_notification: bool = False,
    reply_markup: InlineKeyboardMarkup = None,
) -> int:
    """Simple broadcaster.
    :param bot: Bot instance.
    :param users: List of users.
    :param text: Text of the message.
    :param disable_notification: Disable notification or not.
    :param reply_markup: Reply markup.

    Returns:
        Number of messages sent successfully.
    """
    count = 0
    try:
        for user_id in users:
            if await send_message(bot, user_id, text, disable_notification, reply_markup):
                count += 1
            await asyncio.sleep(0.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        logger.info("%s messages successfully sent.", count)

    return count
