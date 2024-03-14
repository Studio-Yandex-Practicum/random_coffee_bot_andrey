from asgiref.sync import sync_to_async

from aiogram import BaseMiddleware

from admin_panel.telegram.models import TgUser


class AdminMiddleware(BaseMiddleware):
    """ Проверка админ-прав пользователя """
    async def __call__(self, handler, event, data):
        if event.from_user.is_bot:
            return
        user_admin = await sync_to_async(
            TgUser.objects.filter(
                id=event.from_user.id,
                is_admin=True,
            ).exists
        )()

        if not user_admin:
            await event.answer(
                text='Вы не администратор.',
                show_alert=True
            )
            return

        await handler(event, data)
