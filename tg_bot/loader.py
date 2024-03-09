from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import Redis, RedisStorage

from tg_bot.config import BOT_TOKEN
from tg_bot.handlers import all_routers

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
storage = RedisStorage(Redis())
dp = Dispatcher(storage=storage)
dp.include_routers(*all_routers)
