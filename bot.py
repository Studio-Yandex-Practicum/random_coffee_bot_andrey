import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from tg_bot.loader import bot, dp
from tg_bot.misc.mailing import test_mailing
from tg_bot.config import MEETING_TIME, MEETING_DAY


async def main():
    logging.info('Начало работы бота.')
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        test_mailing,
        trigger='cron',
        day_of_week=MEETING_DAY,
        hour=MEETING_TIME,
        minute=17,  # минуты пока оставлены для тестирования
    )
    scheduler.start()
    print(test_mailing)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
