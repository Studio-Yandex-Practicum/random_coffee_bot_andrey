from django.db import models


class TgUser(models.Model):
    """Модель пользователя"""
    id = models.BigIntegerField(unique=True)
    email = models.EmailField(null=True, blank=True)
    enter_full_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=32, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    bot_unblocked = models.BooleanField(default=True)
    is_unblocked = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f"{self.full_name} ({self.email})"
