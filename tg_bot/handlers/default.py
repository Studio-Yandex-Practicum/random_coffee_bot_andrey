from aiogram import types, Router
from aiogram.filters import Command

default_router = Router()


@default_router.message(Command('start'))
async def start_handler(message: types.Message) -> None:
    await message.answer('Старт бота')


@default_router.message(Command("dice"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")


@default_router.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer(message.text)
