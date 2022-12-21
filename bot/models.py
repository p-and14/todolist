from django.db import models


class TgUser(models.Model):
    telegram_chat_id = models.PositiveIntegerField(verbose_name="id чата")
    telegram_user_id = models.PositiveIntegerField(verbose_name="id пользователя")
    verification_code = models.CharField(verbose_name="Код верификации", max_length=20)
    command = models.CharField(verbose_name="Текущая команда", max_length=20, null=True)
    user = models.ForeignKey(
        "core.User", on_delete=models.PROTECT, verbose_name="Пользователь", related_name="user", null=True
    )
