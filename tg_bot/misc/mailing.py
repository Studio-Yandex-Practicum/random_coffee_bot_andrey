import asyncio
import logging
from typing import Optional

from aiogram import exceptions

from admin_panel.telegram.models import TgUser
from tg_bot.db.db_commands import (get_unblocked_users, get_unsent_mailings,
                                   save_model)
from tg_bot.loader import bot


async def mailing(
        data_mailing: Optional[dict[TgUser, str]] = None,
        text: Optional[str] = None,
        users: Optional[list[TgUser]] = None,
) -> None:
    """
    Выполняет рассылку сообщений пользователям Telegram.

    Может быть использована одна из двух схем:
    1. Рассылка индивидуального сообщения каждому пользователю. В этом случае
       необходимо передать `data_mailing` — словарь, где ключом является объект
       пользователя (TgUser), а значением — текст сообщения.
    2. Рассылка общего сообщения для списка пользователей. Требует передачи
       `users` — списка пользователей и `text` — текста сообщения, которое
       будет отправлено каждому из них.

    Параметры:
    - data_mailing: Словарь для индивидуальной рассылки.
    - text: Текст общего сообщения для рассылки.
    - users: Список пользователей для общей рассылки.

    Важно: Должен быть передан либо `data_mailing`, либо оба `text` и `users`.
    """
    if data_mailing is None:
        data_mailing = {user: text for user in users}
    for user, text in data_mailing.items():
        try:
            await bot.send_message(user.id, text)
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
            return await mailing({user: text})
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
        await mailing(users=unblocked_users, text=mail.text)
        mail.is_sent = True
        await save_model(mail)
