from django.contrib.auth import get_user_model
from django.db import models

USER_MODEL = get_user_model()


class TgUser(models.Model):
    telegram_chat_id = models.PositiveIntegerField(verbose_name="id чата")
    telegram_user_id = models.PositiveIntegerField(verbose_name="id пользователя")
    verification_code = models.CharField(verbose_name="Код верификации", max_length=20)
    command = models.CharField(verbose_name="Текущая команда", max_length=20, null=True)
    user_id = models.ForeignKey(
        USER_MODEL, on_delete=models.PROTECT, verbose_name="Пользователь", related_name="user", null=True
    )
