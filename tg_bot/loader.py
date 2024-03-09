from aiogram import Bot, Dispatcher

from tg_bot.config import BOT_TOKEN
from tg_bot.handlers.default import default_router


bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()
dp.include_routers(
    default_router,
)
