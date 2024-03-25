import asyncio
from aiogram import exceptions
import logging

from admin_panel.telegram.models import TgUser
from tg_bot.db.db_commands import save_model

from tg_bot.loader import bot


async def mailing(data_mailing: dict[TgUser, str]):
    """Функция рассылки сообщений.
    Плучает на вод словарь dict[TgUser, str],
    бот выполняет рассылку пользователям"""
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
