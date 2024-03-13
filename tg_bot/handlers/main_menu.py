from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from tg_bot.config import GREETING_TEXT
from tg_bot.middlewares.blocking import BlockingMiddleware
from tg_bot.keyboards.reply import kb_main_menu


main_router = Router()
main_router.message.middleware(BlockingMiddleware())
main_router.callback_query.middleware(BlockingMiddleware())


@main_router.message(Command('start'))
async def main_menu(message: Message):
    """Ввод команды /start"""
    await message.answer(
        GREETING_TEXT,
        reply_markup=kb_main_menu())
