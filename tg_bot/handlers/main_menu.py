from aiogram import Router, F
from aiogram.types import Message

menu_router = Router()


@menu_router.message(F.text == 'Приостановить участие')
async def suspend_participation(message: Message):
    """Приостановление участия."""
    await message.answer('Если вы передумали принимать участие в какую-либо '
                         'неделю или уходите в отпуск, то можно '
                         'приостановить участие в проекте.')
