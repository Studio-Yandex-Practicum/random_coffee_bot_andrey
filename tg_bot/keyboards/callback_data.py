from aiogram.filters.callback_data import CallbackData


class BlockUserCallback(CallbackData, prefix='blocked'):
    user_id: int
    block: bool


class ActiveUserCallback(CallbackData, prefix='active'):
    user_id: int
    is_active: bool

