from django.contrib import admin

from .models import Mailing, TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'enter_full_name',
        'full_name',
        'username',
        'is_active',
        'is_unblocked',
        'bot_unblocked',
    )

    def has_add_permission(self, request, obj=None):
        """Убирает возможность создания пользователей через админку"""
        return False


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'text',
        'date_mailing',
        'is_sent',
    )
    readonly_fields = ('is_sent',)


from .models import Meeting
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'partner',
    )
