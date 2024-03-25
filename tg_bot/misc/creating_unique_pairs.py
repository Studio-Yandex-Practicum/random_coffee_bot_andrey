import random

from admin_panel.telegram.models import Meeting, TgUser
from tg_bot.db.db_commands import (create_meeting, get_active_users,
                                   get_partners_ids)
from tg_bot.misc.mailing import mailing


async def create_pair(
        user: TgUser,
        available_partners: list[TgUser],
        users: set[TgUser],
        meeting_list: list[Meeting],
) -> None:
    """
    Выбирает случайного партнера из списка доступных для текущего,
    удаляет его из множества активных пользователей создаёт экземпляры
    встреч и добавляет их в список встреч.

    Args:
        user: Текущий пользователь, для которого ищется партнер.
        available_partners: Список доступных партнеров.
        users: Множество активных пользователей.
        meeting_list: Список созданных встреч.
    """
    partner = random.choice(available_partners)
    users.remove(partner)
    meeting_list.append(await create_meeting(user=user, partner=partner))
    meeting_list.append(await create_meeting(user=partner, partner=user))


async def create_meetings_for_last_user(
        user: TgUser,
        partners: tuple[TgUser, TgUser],
        meeting_list: list[Meeting],
) -> None:
    """
    Асинхронно создает встречи между указанным пользователем и партнерами.
    Созданные встречи добавляются в список встреч.

    Args:
        user: Текущий пользователь, для которого нужно создать встречи.
        partners: Кортеж партнеров, с каждым из которых нужно создать встречу.
        meeting_list: Список созданных встреч.
    """
    for partner in partners:
        meeting_list.append(await create_meeting(user=user, partner=partner))
        meeting_list.append(await create_meeting(user=partner, partner=user))


async def generate_unique_pairs() -> list[Meeting]:
    """
    Генерирует уникальные пары пользователей, учитывая предыдущие встречи и
    ограничивая повторение пар, если с момента их последней встречи прошло
    не менее полугода.

    Returns:
        List[Meeting]: Список созданных встреч.
    """

    users = await get_active_users()
    meeting_list = []

    while len(users) > 1:
        user = users.pop()
        partners_ids = await get_partners_ids(user)
        available_partners = [
            partner for partner in users
            if partner.id not in partners_ids
        ]

        if not available_partners:
            old_partners_ids = await get_partners_ids(user, old=True)
            available_partners = [
                partner for partner in users
                if partner.id in old_partners_ids
            ]

        if available_partners:
            await create_pair(user, available_partners, users, meeting_list)

    if len(users) == 1:
        user = users.pop()
        partners_ids = await get_partners_ids(user)
        available_meetings = [
            meeting for meeting in meeting_list
            if meeting.user_id not in partners_ids
            and meeting.partner_id not in partners_ids
        ]

        if not available_meetings:
            old_partners_ids = await get_partners_ids(user, old=True)
            available_meetings = [
                meeting for meeting in meeting_list
                if meeting.user_id in old_partners_ids
                and meeting.partner_id in old_partners_ids
            ]

        if available_meetings:
            chosen_meeting = random.choice(available_meetings)
            await create_meetings_for_last_user(
                user,
                (chosen_meeting.user, chosen_meeting.partner),
                meeting_list,
            )

    return meeting_list


async def create_data_for_mailing(meeting_list: list[Meeting]):
    """Функция для создания данных для рассылки.
    Принимает на вход список list[Meeting],
    возвращает словарь dict[TgUser, str] """
    data_mailing = {}
    for user in meeting_list:
        data_mailing[user] = (
            f'Ваш партнер для кофе\n'
            f'Имя и Фамилия: {user.partner.enter_full_name}\n'
            f'Почта: {user.partner.email}\n'
            f'Никнейм в телеграмме: ' + (
                f'@{user.partner.username}' if user.partner.username else '')
        )
    return data_mailing


async def start_random_cofee():
    """Функция для зупуска через AsyncIOScheduler в файле bot.py"""
    meeting_list = await generate_unique_pairs()
    data_mailing = await create_data_for_mailing(meeting_list)
    await mailing(data_mailing)
