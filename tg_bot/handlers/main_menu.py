from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from tg_bot.db import db_commands as db
from tg_bot.keyboards.inline import kb_yes_or_no
from tg_bot.middlewares.blocking import BlockingMiddleware
from tg_bot.keyboards.reply import kb_main_menu
from tg_bot.misc.utils import delete_message

main_menu_router = Router()
main_menu_router.message.middleware(BlockingMiddleware())
main_menu_router.callback_query.middleware(BlockingMiddleware())


MSG_SUSPEND = (
    'Если вы передумали принимать участие\n'
    'в какую-либо неделю или уходите в отпуск,\n'
    'то можно приостановить участие в проекте.\n'
    '\n'
    'Хотите приостановить участие?'
)

APPLY_SUSPEND = 'Вы успешно приостановили участие'
RESUME_PARTICIPATION = 'Вы успешно возобновили участие'

MSG_REVIEW = (
    '<b>Милена Мелкова, Cпециалист по продукту.</b>\n'
    '«Кофе вслепую» - отличная возможность познакомиться с коллегами '
    'из других отделов, в том числе с менеждерами и Директорами, которые '
    'тоже участвуют в проекте.\n'
    '\n'
    '<b>Анастасия Родкина, Младший менеджер по работе с ключевыми '
    'клиентами.</b>\n'
    'Крутая возможность пообщаться, лучше узнать новых сотрудников, '
    'наладить неформальный контакт в условиях удаленной работы… '
    'Поделиться своим опытом и получить заряд позитива! В крупных '
    'компаниях как наша - это необходимо! Спасибо за классный проект!\n'
    '\n'
    '<b>Анна Борисевич, Старший специалист по цифровому контенту.</b>\n'
    'Мне безумно нравится эта инициатива! Уникальная возможность '
    'быстро познакомиться с коллегами, узнать что-то новое и зарядиться '
    'позитивной энергией на весь день 🤩Всем новичкам и бывалым искренне '
    'советую попробовать поучаствовать и получить приятные впечатления 🥰'
)

GREETING_TEXT = (
    'Что умеет этот бот?\n'
    '☕️Мы продолжаем нашу прекрасную традицию знакомиться за чашечкой '
    'горячего кофе или чая.\n'
    '🗓️ С кем ты разделишь капучино - решает случай. Каждый понедельник '
    'в этом боте будет происходить рассылка с именем коллеги, '
    'с кем вам нужно организовать встречу.\n'
    '🔁Участники выбираются случайным образом, поэтому вы сможете выпить '
    'кофе с теми, с кем еще не пересекались по работе.\n'
    'Добро пожаловать🥰')

ABOUT_TEXT = '''
В нашей компании есть прекрасная традиция знакомиться за чашечкой горячего кофе в Microsoft Teams или в офисе.
Раз в неделю будет автоматически приходить имя и фамилия коллеги в этот чат-бот, вам остается договориться
о дате и времени встречи в удобном для вас формате.
«Кофе вслепую»- это всегда:
    - Прекрасная компания;
    - Приятный и неожиданный сюрприз;
    - Помощь новым коллегам в адаптации;
    - Новые знакомства.
''' # noqa


async def main_menu(message: Message):
    """Главное меню"""
    user = await db.get_tg_user(message.from_user.id)
    user_is_active = user.is_active
    if user_is_active:
        await message.answer(
            GREETING_TEXT,
            reply_markup=kb_main_menu(include_resume_button=True)
        )
    else:
        await message.answer(
            GREETING_TEXT,
            reply_markup=kb_main_menu(include_resume_button=False)
        )


@main_menu_router.message(F.text == 'О проекте')
async def about_project(message: Message):
    """ Раздел о проекте """
    await message.answer(ABOUT_TEXT)


@main_menu_router.message(F.text == 'Приостановить участие')
async def suspend_participation(message: Message):
    """Приостановление участия."""
    msg = await message.answer(MSG_SUSPEND, reply_markup=kb_yes_or_no())
    await delete_message(msg)


@main_menu_router.message(F.text == 'Возобновить участие')
async def resume_participation(message: Message):
    """Возобновление участия."""
    user = await db.get_tg_user(message.from_user.id)
    user.is_active = True
    await db.save_model(user)
    msg = await message.answer(RESUME_PARTICIPATION)
    await delete_message(msg)


@main_menu_router.callback_query(F.data.in_({'yes', 'no'}))
async def answer_suspend_participation(callback: CallbackQuery):
    """Приостановление участия."""
    await callback.message.delete()
    user = await db.get_tg_user(callback.from_user.id)
    if callback.data == 'yes':
        user.is_active = False
        await db.save_model(user)
        msg = await callback.message.answer(APPLY_SUSPEND)
        await delete_message(msg)


@main_menu_router.message(F.text == 'Наши коллеги про проект «Кофе вслепую»')
async def reviews(message: Message):
    """Сообщение о проекте."""
    await message.answer(MSG_REVIEW)
