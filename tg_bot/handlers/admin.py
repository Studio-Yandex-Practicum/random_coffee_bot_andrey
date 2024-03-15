import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.db.db_commands import search_tg_user
from tg_bot.misc.utils import delete_message
from tg_bot.states.all_states import Admin
from tg_bot.middlewares.admin import AdminMiddleware

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())
admin_router.callback_query.middleware(AdminMiddleware())


@admin_router.message(Command('admin'))
async def admin_message(message: Message, state: FSMContext):
    """Предложение ввести почту."""
    msg = await message.answer('Введите электронный адрес пользователя:')
    await state.set_state(Admin.get_email)
    await asyncio.create_task(delete_message(msg))


@admin_router.message(Admin.get_email)
async def get_name(message: Message):
    """Поиск пользователя в БД по введённой электронной почте."""
    tg_model = await search_tg_user(message.text.lower())
    if tg_model:
        await message.answer(
            '<b>ДАННЫЕ ПОЛЬЗОВАТЕЛЯ:</b>'
            f'\n<b>ИМЯ И ФАМИЛИЯ:</b> {tg_model.enter_full_name}'
            f'\n<b>НИКНЕЙМ:</b> {tg_model.username} '
            f'\n<b>ПОЛНОЕ ИМЯ В ТГ:</b> {tg_model.full_name} '
        )
    else:
        await message.answer('Такого пользователя не существует')
