import random

from admin_panel.telegram.models import Meeting, TgUser
from tg_bot.db.db_commands import (create_meeting, get_active_users,
                                   get_partners_ids)


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

        if available_partners:
            await create_pair(
                user, available_partners, users, meeting_list)

        else:
            old_partners_ids = await get_partners_ids(user, old=True)
            available_old_partners = [
                partner for partner in users
                if partner.id in old_partners_ids
            ]

            if available_old_partners:
                await create_pair(
                    user, available_old_partners, users, meeting_list)

    return meeting_list
