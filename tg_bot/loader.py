from aiogram import Bot, Dispatcher

from tg_bot.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()
