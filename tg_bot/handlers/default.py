from aiogram import F, types, Router
from aiogram.filters.command import Command


router = Router()


@router.message(Command('start'))
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


@router.message(F.text.lower() == 'да, хочу!')
async def with_puree(message: types.Message):
    await message.reply('Держи кофе')


@router.message(F.text.lower() == 'кофе для слабаков! только минералка!')
async def without_puree(message: types.Message):
    await message.answer('Здесь только кофе!')
