import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from tg_bot.db.db_commands import (
    search_tg_user,
    user_id_block_unblock,
    get_tg_user
)
from tg_bot.keyboards.inline import get_callback_btns
from tg_bot.middlewares.admin import AdminMiddleware
from tg_bot.misc.utils import delete_message
from tg_bot.states.all_states import Admin

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())
admin_router.callback_query.middleware(AdminMiddleware())

USER_NOT_EXIST = (
    'Такого пользователя не существует!'
    '\nВозможно, не правильно ввели почту.'
    '\nПопробуйте ещё раз.'
)


@admin_router.message(Command('admin'))
async def admin_message(message: Message, state: FSMContext):
    """Предложение ввести почту."""
    msg = await message.answer('Введите электронный адрес пользователя:')
    await state.set_state(Admin.get_email)
    await delete_message(msg)


@admin_router.message(Admin.get_email)
async def get_name(message: Message):
    """Поиск пользователя в БД по введённой электронной почте."""

    tg_model = await search_tg_user(message.text.lower())

    if tg_model:
        about_user = (
            '💼<b>ДАННЫЕ ПОЛЬЗОВАТЕЛЯ:</b>💼'
            '\n__________________________________'
            f'\n🔉<b>имя и фамилия:</b> {tg_model.enter_full_name}'
            f'\n🔉<b>никнейм:</b> {tg_model.username}'
            f'\n🔉<b>полное имя в тг:</b> {tg_model.full_name}'
        )
        button = '🛑 Заблокировать' if tg_model.is_unblocked else '✅ Разблокировать'

        msg = await message.answer(
            text=about_user, reply_markup=get_callback_btns(
                btns={f'{button}': f'blocked_{tg_model.id}'}))
        await delete_message(msg)

    else:
        msg = await message.answer(
            text=USER_NOT_EXIST, reply_markup=get_callback_btns(
                btns={'⛔ Отмена': 'cancel'}))
        await delete_message(msg)


@admin_router.callback_query(F.data.startswith('cancel'))
async def stop(callback: CallbackQuery, state: FSMContext):
    """Отмена."""
    await callback.answer()
    msg = await callback.message.answer("Вы отменили текущее действие")
    await state.clear()
    await delete_message(msg)


@admin_router.callback_query(F.data.startswith('blocked_'))
async def unblock(callback: CallbackQuery, state: FSMContext):
    """Разблокировать/заблокировать пользователя."""
    user_id = int(callback.data.split('_')[-1])
    tg_model = await get_tg_user(user_id)
    button = '✅ Разблокировать' if tg_model.is_unblocked else '🛑 Заблокировать'
    msg = 'заблокирован' if tg_model.is_unblocked else 'разблокирован'
    await user_id_block_unblock(user_id)
    await callback.answer()
    await callback.message.edit_text(
        text=(
            '💼<b>ДАННЫЕ ПОЛЬЗОВАТЕЛЯ:</b>💼'
            '\n__________________________________'
            f'\n🔉<b>имя и фамилия:</b> {tg_model.enter_full_name}'
            f'\n🔉<b>никнейм:</b> {tg_model.username}'
            f'\n🔉<b>полное имя в тг:</b> {tg_model.full_name}'
        ),
        reply_markup=get_callback_btns(
            btns={
                f'{button}': f'blocked_{tg_model.id}'
            }
        )
    )
    msg = await callback.message.answer(
        f'Пользователь {tg_model.enter_full_name} {msg}'
    )
    await state.clear()
    await delete_message(msg)
