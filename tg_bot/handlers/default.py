from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

default_router = Router()


@default_router.message(Command('start'))
async def bot_start(message: Message):
    """ Ввод команды 'start' """
    await message.answer("Кофебот приветствует тебя!")
