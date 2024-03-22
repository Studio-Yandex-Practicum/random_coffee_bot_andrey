from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.db.db_commands import get_tg_user
from tg_bot.handlers.main_menu import main_menu
from tg_bot.handlers.registration import start_registration
from tg_bot.middlewares.blocking import BlockingMiddleware


default_router = Router()
default_router.message.middleware(BlockingMiddleware())
default_router.callback_query.middleware(BlockingMiddleware())


@default_router.message(Command('start')) # После ввода старт уставновить поле bot_unblocked== True
async def command_start(message: Message, state: FSMContext):
    """Ввод команды /start"""
    user_id = message.from_user.id
    user = await get_tg_user(user_id)
    if user:
        await main_menu(message)
    else:
        await start_registration(message, state)
