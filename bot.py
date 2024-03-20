import asyncio
import logging

# from apscheduler.schedulers.background import BackgroundScheduler
# from admin_panel.django_settings import settings
# from django.conf import settings

# from admin_panel.django_settings.settings import TIME_ZONE
from tg_bot.loader import bot, dp


async def main():
    logging.info('Начало работы бота.')
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
