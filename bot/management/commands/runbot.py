import os
from pathlib import Path

from environ import environ

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.utils import generate_verification_code

from goals.models import Goal, GoalCategory

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

offset = 0
tg_client = TgClient(env("TELEGRAM_BOT_API"))

while True:
    res = tg_client.get_updates(offset=offset)

    for item in res.result:
        offset = item.update_id + 1
        if not item.message:
            continue

        telegram_chat_id = item.message.chat.id
        telegram_user_id = item.message.from_.id
        tg_user = TgUser.objects.filter(telegram_user_id=telegram_user_id).first()

        if not tg_user:
            welcome_text = f"Здравствуйте, {item.message.chat.first_name}! " \
                           f"Бот умеет показывать все цели" \
                           f" и создавать новую." \

            tg_client.send_message(
                chat_id=telegram_chat_id,
                text=welcome_text
            )
            tg_user = TgUser.objects.create(
                telegram_chat_id=telegram_chat_id,
                telegram_user_id=telegram_user_id,
            )

        if not tg_user.user:
            verification_code = generate_verification_code(10)
            welcome_text = f"Для начала, подтвердите, пожалуйста, свой аккаунт. " \
                           f"Для подтверждения необходимо ввести код: " \
                           f"{verification_code} на сайте"

            tg_client.send_message(
                chat_id=telegram_chat_id,
                text=welcome_text
            )
            tg_user.verification_code = verification_code
            tg_user.save()
        else:
            categories = GoalCategory.objects.filter(
                board__participants__user=tg_user.user_id,
                is_deleted=False
            )
            categories = [category.title for category in categories.all()]
            message_text = item.message.text

            if message_text == "/cancel":
                tg_user.command = None
                tg_user.save()
                tg_client.send_message(chat_id=telegram_chat_id, text="Отмена. Введите новую команду")
            elif tg_user.command == "create":
                if message_text in categories:
                    tg_client.send_message(chat_id=telegram_chat_id, text="Введите название цели")
                    tg_user.command = message_text
                    tg_user.save()
                else:
                    tg_client.send_message(chat_id=telegram_chat_id, text="Неправильная категория")

            elif tg_user.command in categories:
                category = GoalCategory.objects.get(title=tg_user.command)
                goal = Goal.objects.create(
                    title=item.message.text,
                    category=category,
                    user=tg_user.user,
                )
                tg_user.command = None
                tg_user.save()
                tg_client.send_message(chat_id=telegram_chat_id, text=f'Цель "{goal.title}" создана')

            elif message_text == "/goals":
                goals = Goal.objects.filter(
                    category__board__participants__user=tg_user.user, status__in=Goal.Status.values[:3])
                text = "\n".join([goal.title for goal in goals.all()])
                if not text:
                    text = "Целей не найдено"
                tg_client.send_message(chat_id=telegram_chat_id, text=text)

            elif message_text == "/create":
                text = ("Выберите категорию:\n" +
                        "\n".join(categories))
                if not categories:
                    tg_client.send_message(chat_id=telegram_chat_id, text="Категорий не найдено")
                    continue

                tg_client.send_message(chat_id=telegram_chat_id, text=text)
                tg_user.command = "create"
                tg_user.save()
            else:
                tg_client.send_message(chat_id=telegram_chat_id, text="Неизвестная команда")
