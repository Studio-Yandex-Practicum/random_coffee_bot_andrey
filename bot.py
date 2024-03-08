import asyncio
# import logging
import os

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

# from tg_bot.config import logger

load_dotenv()

# Включаем логирование, чтобы не пропустить важные сообщения
# logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token=os.getenv('BOT_TOKEN'))  # "12345678:AaBbCcDdEeFfGgHh")
# Диспетчер
dp = Dispatcher()


# Хэндлер на команду /start
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text='Да, хочу!'),
            types.KeyboardButton(text='Кофе для слабаков! Только минералка!')
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder='Хотите провести встречу за чашечкой кофе?'
    )
    await message.answer('Дратуйте', reply_markup=keyboard)
#    await message.answer('Дратуйте!')


@dp.message(F.text.lower() == 'да, хочу!')
async def with_puree(message: types.Message):
    await message.reply('Держи кофе')


@dp.message(F.text.lower() == 'кофе для слабаков! только минералка!')
async def without_puree(message: types.Message):
    await message.answer('Здесь только кофе!')
# Запуск процесса поллинга новых апдейтов\


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
