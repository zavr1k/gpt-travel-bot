import asyncio
import logging
import sys

from src.chat_bot.bot import bot, dp
from src.chat_bot.handlers import register_main_handlers


async def main() -> None:
    register_main_handlers(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
