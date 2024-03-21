from aiogram.exceptions import SceneException

from admin_panel.telegram.models import TgUser, Meeting
from tg_bot.loader import bot


async def mailing(data_mailing: dict[TgUser, str]):
    for user, text in data_mailing.items():
        try:
            await bot.send_message(user.id, text)
        except SceneException:
            user.bot_unblocked = False
            user.save()
            partner = Meeting.objects.filter(partner=user).first()
            if partner:
                try:
                    await bot.send_message(
                        partner.user.id,
                        'Ваш партнер заблокировал бота и не был уведомлен о встрече.') # noqa
                except SceneException:
                    pass


async def test_mailing():  # Читай докстринг!
    """Функция- заглушка для функции mailing.
Удалить после того как будет готова функция, возвращающая dict[TgUser, str]."""
    users = TgUser.objects.all()
    data_mailing = {}
    for user in users:
        data_mailing[user] = 'текстовое сообщение'
    await mailing(data_mailing)
