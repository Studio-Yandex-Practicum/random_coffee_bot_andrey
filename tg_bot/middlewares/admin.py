from aiogram import BaseMiddleware


class CheckRulesAdminMiddleware(BaseMiddleware):
    """ Проверка админ-прав пользователя """
    async def __call__(self, handler, event, data):
        if event.from_user.is_bot:
            return
        user_id = event.from_user.id
        admin_id = 457161780  # Временная заглушка(мой ID типа я админ)

        if user_id != admin_id:
            await event.answer(
                text='Вы не администратор.',
                show_alert=True
            )
            return

        await handler(event, data)
