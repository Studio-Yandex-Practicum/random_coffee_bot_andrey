from aiogram import Bot, Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from tg_bot.config import ADMIN_ID

default_router = Router()


@default_router.startup()
async def start_bot(bot: Bot):
    """Сообщение админу при запуске бота"""
    await bot.send_message(ADMIN_ID, text='Бот запущен')


@default_router.shutdown()
async def stop_bot(bot: Bot):
    """Сообщение админу при остановке бота"""
    await bot.send_message(ADMIN_ID, text='Бот остановлен')


@default_router.message(CommandStart())
async def get_start(message: Message):
    """Ввод команды /start"""
    await message.answer(
        'Что умеет этот бот?\n'
        '☕️ Мы продолжаем нашу прекрасную традицию знакомиться за '
        'чашечкой горячего кофе или чая.\n'
        '🗓️ С кем ты разделишь капучино - решает случай. Каждый понедельник '
        'в этом боте будет происходить рассылка с именем коллеги, с кем вам '
        'нужно организовать встречу.\n'
        '🔁 Участники выбираются случайным образом, поэтому вы сможете выпить '
        'кофе с теми, с кем еще не пересекались по работе.\n'
        'Добро пожаловать🥰'
    )
