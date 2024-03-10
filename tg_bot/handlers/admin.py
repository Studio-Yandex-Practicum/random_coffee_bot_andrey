from aiogram import types, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

admin_router = Router()


class AdminRegistration(StatesGroup):
    last_name = State()
    first_name = State()


@admin_router.message(StateFilter(None), Command('admin'))
async def admin_message(message: types.Message, state: FSMContext):
    """Ввести фамилию"""
    await message.answer('Введите фамилию:')
    await state.set_state(AdminRegistration.last_name)


@admin_router.message(AdminRegistration.last_name, F.text)
async def admin_message(message: types.Message, state: FSMContext):
    """Ввести имя"""
    if message.text.isalpha():
        await state.update_data(last_name=message.text.capitalize())
        await message.answer('Введите имя:')
        await state.set_state(AdminRegistration.first_name)
    else:
        await message.answer('Фамилия должна состоять только из букв')


@admin_router.message(AdminRegistration.first_name, F.text)
async def admin_message(message: types.Message, state: FSMContext):
    """Вывод Фамилии и имени пользователю"""
    if message.text.isalpha():
        await state.update_data(first_name=message.text.capitalize())
        data = await state.get_data()
        await message.answer(f"Администратор: {data['first_name']} {data['last_name']} зарегистрирован.")
        await state.clear()
    else:
        await message.answer('Имя должно состоять только из букв')
