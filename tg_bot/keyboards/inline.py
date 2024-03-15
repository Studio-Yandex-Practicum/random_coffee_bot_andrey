from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_callback_btns(
        *,
        btns: dict[str, str],
        sizes: tuple[int] = (2,)):
    keyboard = InlineKeyboardBuilder()

    for btn_name, data in btns.items():
        keyboard.add(
            InlineKeyboardButton(
                text=btn_name,
                callback_data=data
            )
        )
    return keyboard.adjust(*sizes).as_markup()
