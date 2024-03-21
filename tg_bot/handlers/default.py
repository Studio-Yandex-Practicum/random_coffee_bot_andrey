from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from tg_bot.db.db_commands import get_tg_user
from tg_bot.handlers.main_menu import main_menu
from tg_bot.handlers.registration import start_registration
from tg_bot.middlewares.blocking import BlockingMiddleware

default_router = Router()
default_router.message.middleware(BlockingMiddleware())
default_router.callback_query.middleware(BlockingMiddleware())


@default_router.message(Command('start'))
async def command_start(message: Message, state: FSMContext):
    """Ввод команды /start"""
    user_id = message.from_user.id
    user = await get_tg_user(user_id)
    if user:
        await main_menu(message)
    else:
        await start_registration(message, state)


@default_router.message(Command('test'))
async def command_test(message: Message, state: FSMContext):
    from admin_panel.telegram.models import TgUser
    from tg_bot.misc.creating_unique_pairs import generate_unique_pairs
    for i in range(1, 6):
        username = f"user{i}"
        email = f"user{i}@groupeseb.ru"
        full_name = f"User {i} Full Name"
        enter_full_name = f"User {i} Enter Full Name"

        # Проверяем существование пользователя с таким email
        if TgUser.objects.filter(email=email).exists():
            print(
                f"Пользователь с адресом {email} уже существует, пропускаем создание.")
            continue

        # Создаем пользователя в базе данных
        user = TgUser.objects.create(
            id=i,
            email=email,
            enter_full_name=enter_full_name,
            username=username,
            full_name=full_name
        )
        print(f"Создан пользователь: {user.email}")

    await generate_unique_pairs()
