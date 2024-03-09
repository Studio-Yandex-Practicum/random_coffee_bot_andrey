import asyncio
import logging

from tg_bot.loader import bot, dp


async def main():
    logging.info('Начало работы бота.')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
