import re

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.config import ALLOWED_DOMAIN
from tg_bot.db.db_commands import create_tg_user
from tg_bot.handlers.main_menu import main_menu
from tg_bot.misc.utils import get_entered_name
from tg_bot.states.all_states import Register


registration_router = Router()


async def start_registration(message: Message, state: FSMContext):
    """Старт регистрации"""
    await message.answer('Введите свои имя и фамилию')
    await state.set_state(Register.get_name)


@registration_router.message(Register.get_name)
async def get_name(message: Message, state: FSMContext):
    """Получение имени и фамилии"""
    full_name = await get_entered_name(message.text)

    if not full_name:
        await message.answer('Введите, свои имя и фамилию, состоящие только '
                             'из букв и разделенные пробелом.')
        return

    await message.answer('Теперь введите свой e-mail')
    await state.update_data(full_name=full_name)
    await state.set_state(Register.get_email)


@registration_router.message(Register.get_email)
async def get_email(message: Message, state: FSMContext):
    """ Получение почты """
    email = message.text.lower()
    pattern = rf'^[a-zA-Z0-9._]+' \
              rf'{re.escape(ALLOWED_DOMAIN)}\.' \
              rf'[a-zA-Z0-9._]'
    if not re.match(pattern, email):
        await message.answer(
            'Кажется, что указана не та почта, '
            'пожалуйста, для регистрации укажите именно рабочую почту'
        )
    else:
        context_data = await state.get_data()
        full_name = context_data.get('full_name')
        await create_tg_user(
            user=message.from_user,
            email=email,
            enter_full_name=full_name
        )
        await message.answer(
            'Вы зарегистрированы.')
        await main_menu(message)
        await state.clear()
