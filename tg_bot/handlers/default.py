from aiogram import Bot, Router
from aiogram.filters import Command
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


@default_router.message(Command('start'))
async def get_start(message: Message):
    """Ввод команды /start"""
    await message.answer(
        f'Привет {message.from_user.full_name}, Что умеет этот бот?\n'
        f'☕️ Мы продолжаем нашу прекрасную традицию знакомиться за '
        f'чашечкой горячего кофе или чая.\n'
        f'🗓️ С кем ты разделишь капучино - решает случай. Каждый понедельник '
        f'в этом боте будет происходить рассылка с именем коллеги, с кем вам '
        f'нужно организовать встречу.\n'
        f'🔁 Участники выбираются случайным образом, поэтому вы сможете выпить '
        f'кофе с теми, с кем еще не пересекались по работе.\n'
        f'Добро пожаловать🥰'
    )
