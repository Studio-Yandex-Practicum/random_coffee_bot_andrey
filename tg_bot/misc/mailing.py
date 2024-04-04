import asyncio
import logging

from aiogram import exceptions, types

from admin_panel.telegram.models import TgUser
from tg_bot.db.db_commands import (
    get_unblocked_users, get_unsent_mailings, save_model,
    get_users_meetings_this_week,
)
from tg_bot.keyboards.inline import question_about_meeting
from tg_bot.loader import bot


async def send_message(
        user: TgUser,
        text: str,
        reply_markup: types.InlineKeyboardMarkup = None
):
    """
    Отправляет сообщение указанному пользователю Telegram.

    Параметры:
    - user: Пользователь, которому отправляем сообщение.
    - text: Текст сообщения.
    """
    try:
        return await bot.send_message(
            chat_id=user.id,
            text=text,
            reply_markup=reply_markup,
        )
    except exceptions.TelegramForbiddenError as e:
        if e.message == 'Forbidden: bot was blocked by the user':
            logging.info(f'Пользователь {user.id} заблокировал бота')
            user.bot_unblocked = False
            await save_model(user)
        else:
            logging.warning(e)
    except exceptions.TelegramRetryAfter as e:
        logging.warning(
            f'Flood limit is exceeded. Sleep {e.retry_after} seconds.')
        await asyncio.sleep(e.retry_after)
        return await send_message(user, text, reply_markup)
    except (exceptions.TelegramAPIError, exceptions.TelegramBadRequest):
        pass


async def mailing_date() -> None:
    """
    Выполняет рассылку сообщений пользователям, которые не заблокировали бота.

    Функция извлекает из базы данных все непосланные рассылки и список всех
    пользователей, которые не заблокировали бота. Для каждой такой рассылки
    отправляет сообщение каждому из незаблокированных пользователей.
    После успешной отправки сообщений обновляет статус рассылки is_sent=True.
    """
    unsent_mailings = await get_unsent_mailings()
    unblocked_users = await get_unblocked_users()

    for mail in unsent_mailings:
        for user in unblocked_users:
            await send_message(user, mail.text)
        mail.is_sent = True
        await save_model(mail)


async def mailing_question():
    """Опрос участников встречи"""
    users = await get_users_meetings_this_week()
    text = 'Удалось ли уже встретиться с коллегой и выпить чашечку кофе?☕️'
    for user in users:
        await send_message(
            user=user,
            text=text,
            reply_markup=question_about_meeting(),
        )

