import re

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.states.all_states import Register
from tg_bot.config import ALLOWED_DOMAIN

default_router = Router()


@default_router.message(Command('start'))
async def bot_start(message: Message):
    """Ввод команды /start"""
    await message.answer("Кофе-бот приветствует тебя!")


@default_router.message(Command('name'))
async def command_name(message: Message, state: FSMContext):
    """Ввод команды /name"""
    await message.answer('Введите свои имя и фамилию')
    await state.set_state(Register.get_name)


@default_router.message(Register.get_name)
async def get_name(message: Message, state: FSMContext):
    """Получение имени"""
    name_parts = message.text.strip().split(' ')

    if len(name_parts) != 2 or not all(part.isalpha() for part in name_parts):
        await message.answer('Введите, свои имя и фамилию, состоящие только '
                             'из букв и разделенные пробелом.')
        return

    full_name = ' '.join(part.capitalize() for part in name_parts)
    await message.answer('Теперь введите свой e-mail')
    await state.update_data(full_name=full_name)
    await state.set_state(Register.get_email)


@default_router.message(Register.get_email)
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
        await message.answer(
            f'Ваши данные\n'
            f'Полное имя: {full_name}\n'
            f'Рабочая почта: {email}')
        await state.clear()
