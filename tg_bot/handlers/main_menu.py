from aiogram import Router
from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
from aiogram.types import Message

# from tg_bot.config import ALLOWED_DOMAIN
# from tg_bot.db.db_commands import create_tg_user
from tg_bot.middlewares.blocking import BlockingMiddleware
# from tg_bot.misc.utils import get_entered_name
# from tg_bot.states.all_states import Register
from tg_bot.keyboards.reply import reply_keyboard


main_router = Router()
main_router.message.middleware(BlockingMiddleware())
main_router.callback_query.middleware(BlockingMiddleware())


@main_router.message(Command('start'))
async def main_menu(message: Message):
    """Ввод команды /start"""
    await message.answer('Кофе-бот приветствует тебя!',
                         reply_markup=reply_keyboard)
