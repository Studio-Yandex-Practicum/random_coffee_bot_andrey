from aiogram import BaseMiddleware


class BlockingMiddleware(BaseMiddleware):
    """Middleware для проверки заблокированных пользователей"""
    async def __call__(self, handler, event, data):
        if event.from_user.is_bot:
            return

        user_id = event.from_user.id
        # Костыль, для проверки введите свой telegram_id
        blocked_id = 455343976

        if user_id == blocked_id:
            await event.answer(
                    text='Вы заблокированы.',
                    show_alert=True
                )
            return

        await handler(event, data)
