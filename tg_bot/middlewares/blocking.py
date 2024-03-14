from asgiref.sync import sync_to_async

from aiogram import BaseMiddleware

from admin_panel.telegram.models import TgUser


class BlockingMiddleware(BaseMiddleware):
    """Middleware для проверки заблокированных пользователей"""
    async def __call__(self, handler, event, data):
        if event.from_user.is_bot:
            return

        user_blocked = await sync_to_async(
            TgUser.objects.filter(
                id=event.from_user.id,
                is_unblocked=False,
            ).exists
        )()

        if user_blocked:
            await event.answer(
                    text='Вы заблокированы.',
                    show_alert=True
                )
            return

        await handler(event, data)
