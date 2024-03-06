import os

import django
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis

from tg_bot.config import BOT_TOKEN, redis_host, redis_port, bot_logger


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "admin_panel.django_settings.settings"
    )
    os.environ.update({"DJANGO_ALLOW_ASYNC_UNSAFE": "true"})
    django.setup()


def include_all_routers():
    from tg_bot.handlers.default import default_router
    dp.include_router(default_router)


bot_logger.info("Logger initialized")
setup_django()
bot = Bot(BOT_TOKEN, parse_mode='HTML')

if redis_host and redis_port:
    storage = RedisStorage(Redis(host=redis_host, port=redis_port))
else:
    storage = MemoryStorage()

dp = Dispatcher(storage=storage)
include_all_routers()
