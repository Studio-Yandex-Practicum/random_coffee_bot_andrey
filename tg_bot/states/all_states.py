from aiogram.fsm.state import State, StatesGroup


class StepsRegister(StatesGroup):
    GET_NAME = State()
    GET_EMAIL = State()
