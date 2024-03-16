from aiogram.filters.callback_data import CallbackData


class BlockUserCallback(CallbackData, prefix='blocked_'):
    user_id: int  # id пользователя в телеграмме
