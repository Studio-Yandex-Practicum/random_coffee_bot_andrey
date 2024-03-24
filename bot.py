import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tg_bot.loader import bot, dp
from tg_bot.misc.creating_unique_pairs import start_random_cofee
from tg_bot.config import MEETING_TIME, MEETING_DAY


async def main():
    logging.info('Начало работы бота.')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        start_random_cofee,
        trigger='cron',
        day_of_week=MEETING_DAY,
        hour=MEETING_TIME,
        minute=16,  # минуты пока оставлены для тестирования
    )
    scheduler.start()
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
