from aiogram.exceptions import SceneException

from admin_panel.telegram.models import TgUser, Meeting
from tg_bot.loader import bot


async def mailing(messages: dict[TgUser, str]):
    for user, text in messages.items():
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
