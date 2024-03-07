import asyncio
import logging

from aiogram import types
from aiogram.filters.command import Command

from tg_bot.loader import bot, dp


@dp.message(Command('start'))
async def bot_start(message: types.Message):
    """ Метод запуска бота. """
    await message.answer("Кофебот приветствует тебя!")


async def main():
    logging.info('Начало работы бота.')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
