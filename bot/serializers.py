from rest_framework import serializers

from bot.models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(
        read_only=True,
        slug_field="username",
        source="user_id"
    )

    class Meta:
        model = TgUser
        fields = ("id", "username", "user_id", "verification_code")
        read_only_fields = ("id", "username", "user_id")
