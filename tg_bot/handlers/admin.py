from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.states.all_states import Admin

admin_router = Router()


@admin_router.message(Command('admin'))
async def admin_message(message: Message, state: FSMContext):
    """Ввести фамилию"""
    await message.answer('Введите свои имя и фамилию:')
    await state.set_state(Admin.get_name)


@admin_router.message(Admin.get_name)
async def get_name(message: Message):
    """Получение имени и фамилии"""
    name_parts = message.text.strip().split(' ')

    if len(name_parts) != 2 or not all(part.isalpha() for part in name_parts):
        await message.answer('Введите, свои имя и фамилию, состоящие только '
                             'из букв и разделенные пробелом.')
        return

    full_name = ' '.join(part.capitalize() for part in name_parts)
    await message.answer(f'{full_name}')
