import os
from pathlib import Path

from environ import environ
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from bot.models import TgUser
from bot.serializers import TgUserSerializer
from bot.tg.client import TgClient

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

tg_client = TgClient(env("TELEGRAM_BOT_API"))


class BotVerifyView(generics.GenericAPIView):
    serializer_class = TgUserSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        verification_code = request.data.get("verification_code")
        user = request.user
        if telegram_user := TgUser.objects.filter(
                verification_code=verification_code
        ).first():
            telegram_user.user = user
            telegram_user.save()

            text = "Верификация успешна пройдена. " \
                   "Доступные команды:\n" \
                   "/goals (Посмотреть список целей)\n" \
                   "/create (Создать цель)"
            tg_client.send_message(
                chat_id=telegram_user.telegram_chat_id,
                text=text,
            )

            serializer = self.get_serializer(telegram_user)
            return Response(serializer.data, status=200)
        else:
            raise NotFound("Неправильный код верификации")
