import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('BOT_TOKEN'))

dp = Dispatcher()

@dp.message(Command('start'))
async def bot_start(message: types.Message):
    await message.answer("Кофебот приветствует тебя!")

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
