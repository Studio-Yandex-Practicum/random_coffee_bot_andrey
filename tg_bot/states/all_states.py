from aiogram.fsm.state import State, StatesGroup


class Admin(StatesGroup):
    get_name = State()


class Register(StatesGroup):
    get_name = State()
    get_email = State()
