from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.misc.utils import get_entered_name
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
    full_name = await get_entered_name(message.text)

    if not full_name:
        await message.answer('Введите, свои имя и фамилию, состоящие только '
                             'из букв и разделенные пробелом.')
        return

    await message.answer(f'{full_name}')
