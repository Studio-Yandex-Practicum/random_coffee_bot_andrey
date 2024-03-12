from asgiref.sync import sync_to_async
from aiogram.types.user import User

from admin_panel.telegram.models import TgUser


@sync_to_async
def create_tg_user(user: User, email: str, enter_full_name: str):
    tg_user = TgUser.objects.create(
        id=user.id,
        email=email,
        enter_full_name=enter_full_name,
        username=user.username,
        full_name=user.full_name
    )
    return tg_user


@sync_to_async
def search_tg_user(enter_full_name: str):
    return TgUser.objects.filter(enter_full_name=enter_full_name)
