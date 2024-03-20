import random
from datetime import date, timedelta

from admin_panel.telegram.models import TgUser


def create_pair(
        user: TgUser,
        available_partners: list[TgUser],
        users: set[TgUser],
        pairs: list[tuple[TgUser, TgUser]],
) -> None:
    """
    Выбирает случайного партнера из списка доступных для текущего,
    удаляет его из множества активных пользователей и добавляет
    пару в список пар.

    Args:
        user: Текущий пользователь, для которого ищется партнер.
        available_partners: Список доступных партнеров.
        users: Общий набор активных пользователей.
        pairs: Список созданных пар пользователей.
    """
    partner = random.choice(available_partners)
    users.remove(partner)
    pairs.append((user, partner))


def generate_unique_pairs() -> list[tuple[TgUser, TgUser]]:
    """
    Генерирует уникальные пары пользователей, учитывая предыдущие встречи и
    ограничивая повторение пар, если с момента их последней встречи прошло
    не менее полугода.

    Returns:
        List[Tuple[TgUser, TgUser]]: Список уникальных пар пользователей.
    """
    half_year_ago = date.today() - timedelta(days=180)

    users = set(TgUser.objects.filter(
        is_active=True,
        is_unblocked=True,
        bot_unblocked=True,
    ))
    pairs: list[tuple[TgUser, TgUser]] = []

    while len(users) > 1:
        user = users.pop()
        partners_ids = set(
            user.user_meetings.values_list('partner', flat=True)
        )
        available_partners = [
            partner for partner in users
            if partner.id not in partners_ids
        ]

        if available_partners:
            create_pair(user, available_partners, users, pairs)

        else:
            old_partners_ids = set(user.user_meetings.filter(
                date__lt=half_year_ago
            ).values_list('partner', flat=True))
            available_old_partners = [
                partner for partner in users
                if partner.id in old_partners_ids
            ]

            if available_old_partners:
                create_pair(user, available_old_partners, users, pairs)

    return pairs
