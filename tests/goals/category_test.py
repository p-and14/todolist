import pytest

from goals import serializers
from goals.models import BoardParticipant, GoalCategory


@pytest.mark.django_db
def test_category_create(client, user_factory, board_factory, board_participant_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    data = {
        "title": "test",
        "board": board.pk,
    }

    client.force_login(user)
    response = client.post("/goals/goal_category/create", data=data, content_type="application/json")
    category = GoalCategory.objects.filter(user=user).first()
    expected_response = serializers.GoalCategoryCreateSerializer(category).data

    assert response.status_code == 201
    assert response.data == expected_response
    assert response.data["title"] == "test"
    assert response.data["board"] == board.pk


@pytest.mark.django_db
def test_category_list(client, user_factory, board_factory,
                       board_participant_factory, category_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    categories = category_factory.create_batch(2, board=board, user=user)

    expected_response = serializers.GoalCategorySerializer(categories, many=True).data
    client.force_login(user)
    response = client.get("/goals/goal_category/list", {"ordering": "id"})

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_category_read(client, user_factory, board_factory,
                       board_participant_factory, category_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    category = category_factory.create(board=board, user=user)

    expected_response = serializers.GoalCategorySerializer(category).data
    client.force_login(user)
    response = client.get(f"/goals/goal_category/{category.pk}")

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_category_update(client, user_factory, board_factory,
                     board_participant_factory, category_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    category = category_factory.create(board=board, user=user)

    data = {
        "title": "test_2",
    }

    client.force_login(user)
    response = client.put(f"/goals/goal_category/{category.pk}", data=data, content_type="application/json")
    category = GoalCategory.objects.filter(pk=category.pk).first()
    expected_response = serializers.GoalCategorySerializer(category).data

    assert response.status_code == 200
    assert response.data == expected_response
    assert response.data["title"] == "test_2"


@pytest.mark.django_db
def test_category_partial_update(client, user_factory, board_factory,
                             board_participant_factory, category_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    category = category_factory.create(board=board, user=user)

    data = {
        "title": "test_3",
    }

    client.force_login(user)
    response = client.patch(f"/goals/goal_category/{category.pk}", data=data, content_type="application/json")
    category = GoalCategory.objects.filter(pk=category.pk).first()
    expected_response = serializers.GoalCategorySerializer(category).data

    assert response.status_code == 200
    assert response.data == expected_response
    assert response.data["title"] == "test_3"


@pytest.mark.django_db
def test_category_delete(client, user_factory, board_factory,
                             board_participant_factory, category_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    category = category_factory.create(board=board, user=user)

    client.force_login(user)
    response = client.delete(f"/goals/goal_category/{category.pk}")
    category = GoalCategory.objects.filter(pk=category.pk).first()

    assert response.status_code == 204
    assert category.is_deleted
    assert len(GoalCategory.objects.filter(user=user)) == 1
