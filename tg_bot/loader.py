from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from tg_bot.config import BOT_TOKEN
from tg_bot.handlers import all_handlers


def include_all_routers():
    """ Добавление роутеров. """
    for handler in all_handlers:
        dp.include_routers(handler)


bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
storage = RedisStorage(Redis())
dp = Dispatcher(storage=storage)
include_all_routers()
