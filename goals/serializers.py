from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from core.serializers import UserProfileSerializer
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant

User = get_user_model()


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(
        required=True,
        choices=BoardParticipant.Role.choices[1:]
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all(), required=True
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True, required=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        owner = validated_data.pop("user")
        new_participants = validated_data.pop("participants")
        new_with_user_id = {participant["user"].id: participant for participant in new_participants}
        old_participants = instance.participants.exclude(user=owner)

        with transaction.atomic():
            for old_participant in old_participants:
                if old_participant.user_id not in new_with_user_id:
                    old_participant.delete()
                else:
                    old_participant.role = new_with_user_id.pop(old_participant.user_id)["role"]
                    old_participant.save()

            for new_participant in new_with_user_id.values():
                if owner == new_participant.get("user"):
                    raise serializers.ValidationError(
                        {"participants":
                             {"user": f"Can't change the role for the user {owner.username}"}})
                BoardParticipant.objects.create(
                    board=instance,
                    **new_participant)

        if title := validated_data.get("title"):
            instance.title = title
            instance.save()
        return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    board = serializers.SlugRelatedField(
        slug_field="id",
        queryset=Board.objects.all(),
        required=True
    )

    class Meta:
        model = GoalCategory
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    board = BoardSerializer()

    class Meta:
        model = GoalCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "board")


class GoalCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    description = serializers.CharField(allow_blank=True, required=False, allow_null=True)

    class Meta:
        model = Goal
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError("not allowed in deleted category")
        return value


class GoalSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")


class GoalCommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        read_only_fields = ("id", "created", "updated", "user")
        fields = "__all__"


class GoalCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    goal = serializers.SlugRelatedField(
        slug_field="id",
        read_only=True
    )

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")
