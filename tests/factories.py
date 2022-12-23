import factory

from core.models import User
from goals.models import Goal, Board, GoalCategory, BoardParticipant


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("first_name")
    password = "test_password"
    email = factory.Faker("ascii_free_email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    is_active = True


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker("first_name")
    is_deleted = False


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    role = BoardParticipant.Role.owner


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Faker("first_name")
    user = factory.SubFactory(UserFactory)
    is_deleted = False
    board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Faker("first_name")
    description = factory.Faker("first_name")
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    status = Goal.Status.to_do
    priority = Goal.Priority.medium
