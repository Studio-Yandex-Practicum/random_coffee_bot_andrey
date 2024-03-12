from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kb_main_menu():
    reply_keyboard = ReplyKeyboardBuilder()

    reply_keyboard.button(text='О проекте')
    reply_keyboard.button(text='Наши коллеги про проект «Кофе вслепую»')
    reply_keyboard.button(text='Приостановить участие')
    reply_keyboard.button(text='Возобновить участие')
    reply_keyboard.adjust(2, 2)
    return reply_keyboard.as_markup(
        resize_keyboard=True,
        input_field_placeholder='Выберите кнопку'
    )
