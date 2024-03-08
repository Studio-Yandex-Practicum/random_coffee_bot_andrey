import asyncio

from tg_bot.config import logger
from tg_bot.loader import bot, dp
from tg_bot.handlers.default import router


async def main():
    logger.debug('Начало работы бота')
    dp.include_routers(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
