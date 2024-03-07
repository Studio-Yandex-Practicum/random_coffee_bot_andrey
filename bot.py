import asyncio
import logging

from tg_bot.loader import bot, dp
from tg_bot.handlers import default


async def main():
    logging.info('Начало работы бота.')
    dp.include_routers(default.default_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
