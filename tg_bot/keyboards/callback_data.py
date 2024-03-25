from aiogram.filters.callback_data import CallbackData


class BlockUserCallback(CallbackData, prefix='blocked'):
    user_id: int
    block: bool


class UserIsActiveCallback(CallbackData, prefix='is_active'):
    is_active: bool


