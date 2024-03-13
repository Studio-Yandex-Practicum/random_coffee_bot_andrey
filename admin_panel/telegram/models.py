from django.db import models


class TgUser(models.Model):
    """Модель пользователя"""
    id = models.BigIntegerField(
        verbose_name='ID пользователя в Telegram', primary_key=True)
    email = models.EmailField(verbose_name='Почта', unique=True)
    enter_full_name = models.CharField(
        verbose_name='Введенное пользователем имя и фамилия',
        max_length=100,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=32,
        null=True,
        blank=True
    )
    full_name = models.CharField(verbose_name='Полное имя', max_length=100)
    bot_unblocked = models.BooleanField(
        verbose_name='Бот разблокирован пользователем', default=True)
    is_unblocked = models.BooleanField(
        verbose_name='Пользователь разблокирован', default=True)
    is_admin = models.BooleanField(
        verbose_name='Права администратора', default=False)
    is_active = models.BooleanField(
        verbose_name='Пользователь активен', default=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.id} {self.enter_full_name}'
