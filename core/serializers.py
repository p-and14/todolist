from django.contrib.auth import password_validation
from rest_framework import serializers

from core.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[password_validation.validate_password])
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "password", "password_repeat"]

    def validate(self, data):
        password = data.get("password")
        password_repeat = data.pop("password_repeat")
        if password != password_repeat:
            raise serializers.ValidationError("Passwords don't match")
        return data

    def create(self, validated_data):
        password = self.initial_data.get("password")
        user = User.objects.create(**validated_data)

        user.set_password(password)
        user.save()
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[password_validation.validate_password])

    class Meta:
        model = User
        fields = ["old_password", "new_password"]

    def is_valid(self, *, raise_exception=False):
        self._old_password = self.initial_data.get("old_password")
        self._new_password = self.initial_data.get("new_password")
        return super().is_valid(raise_exception=raise_exception)

    def validate(self, data):
        if not self.instance.check_password(self._old_password):
            raise serializers.ValidationError("The old password is wrong")
        return data

    def update(self, instance, validated_data):
        instance.set_password(self._new_password)
        instance.save()
        return instance
