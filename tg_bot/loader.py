from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis

from tg_bot.config import BOT_TOKEN


def include_all_routers():
    """ Добавление роутеров. """
    from tg_bot.handlers import all_routers
    dp.include_routers(*all_routers)


bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
storage = RedisStorage(Redis())
dp = Dispatcher(storage=storage)
include_all_routers()
