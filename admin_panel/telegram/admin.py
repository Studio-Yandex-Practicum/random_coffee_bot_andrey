from django.contrib import admin

from .models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = (
        'enter_full_name',
        'full_name',
        'username',
        'is_unblocked',
        'bot_unblocked',
    )

    def has_add_permission(self, request, obj=None):
        """Убирает возможность создания пользователей через админку"""
        return False
