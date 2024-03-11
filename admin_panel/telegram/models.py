from django.db import models


class TgUser(models.Model):
    """Модель пользователя"""
    id = models.BigIntegerField(unique=True)
    email = models.EmailField('Почта', null=True, blank=True)
    enter_full_name = models.CharField('Введенное пользователем имя',
                                       max_length=100,
                                       null=True,
                                       blank=True)
    username = models.CharField('Имя пользователя',
                                max_length=32,
                                null=True,
                                blank=True)
    full_name = models.CharField('Полное имя', max_length=100)
    bot_unblocked = models.BooleanField('Бот разблокирован пользователем',
                                        default=True)
    is_unblocked = models.BooleanField('Пользователь разблокирован',
                                       default=True)
    is_admin = models.BooleanField('Права администратора', default=False)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        f'{self.id} {self.enter_full_name}'
