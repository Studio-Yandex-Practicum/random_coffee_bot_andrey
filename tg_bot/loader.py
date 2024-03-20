import os
import django

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from admin_panel.django_settings.settings import TIME_ZONE
from tg_bot.config import BOT_TOKEN, DEBUG
from tg_bot.misc import mailing


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "admin_panel.django_settings.settings"
    )
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


def include_all_routers():
    """ Добавление роутеров. """
    from tg_bot.handlers import all_routers
    dp.include_routers(*all_routers)


setup_django()
bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
scheduler = AsyncIOScheduler(timezone=TIME_ZONE)  # 'Europe/Moscow'  timezone=TIME_ZONE
scheduler.add_job(mailing, trigger='cron',
                  day_of_week='tue', hour=00, minute=48,
                  kwargs={'bot': bot})
scheduler.start()

if DEBUG:
    storage = MemoryStorage()
else:
    storage = RedisStorage(Redis())

dp = Dispatcher()
include_all_routers()
