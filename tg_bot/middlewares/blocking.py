from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message


class BlockingMiddleware(BaseMiddleware):
    """Middleware для проверки заблокированных пользователей"""
    async def __call__(self, handler, event, data):
        if event.from_user.is_bot:
            return

        user_id = event.from_user.id
        # Костыль, для проверки введите свой telegram_id
        blocked_id = 455343976

        if user_id == blocked_id:
            if isinstance(event, Message):
                await event.answer('Вы заблокированы.')
            elif isinstance(event, CallbackQuery):
                await event.message.answer('Вы заблокированы.')
            return

        await handler(event, data)
