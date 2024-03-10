from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    get_name = State()
    get_email = State()
