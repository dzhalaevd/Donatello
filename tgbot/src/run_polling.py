import asyncio
import contextlib

from bot import create_bot, create_dispatcher, on_shutdown, on_startup
from config import load_config
from infra.logging import configure_logging


async def main() -> None:
    configure_logging()
    config = load_config(".env")

    bot = await create_bot(config)
    dp = create_dispatcher(config)

    try:
        await on_startup(bot, config.tg_bot.admin_ids)
        await dp.start_polling(bot)
    finally:
        await on_shutdown(bot)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(main())
