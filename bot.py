import asyncio
import logging

from tg_bot.loader import bot, dp


async def main():
    logging.info('Начало работы бота.')
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
