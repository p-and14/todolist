import pytest

from goals import serializers
from goals.models import Goal, BoardParticipant


@pytest.mark.django_db
def test_goal_create(client, user_factory, board_factory, board_participant_factory, category_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    cat = category_factory.create(board=board, user=user)
    data = {
        "category": cat.pk,
        "title": "test",
        "description": "test",
        "due_date": "2022-12-22",
        "status": Goal.Status.to_do,
        "priority": Goal.Priority.medium
    }

    client.force_login(user)
    response = client.post("/goals/goal/create", data=data, content_type="application/json")
    goal = Goal.objects.filter(user=user).first()
    expected_response = serializers.GoalCreateSerializer(goal).data

    assert response.status_code == 201
    assert response.data == expected_response
    assert response.data["title"] == "test"
    assert response.data["description"] == "test"
    assert response.data["status"] == Goal.Status.to_do
    assert response.data["category"] == cat.pk


@pytest.mark.django_db
def test_goal_list(client, user_factory, board_factory,
                   board_participant_factory, category_factory, goal_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    cat = category_factory.create(board=board, user=user)
    goals = goal_factory.create_batch(2, category=cat, user=user)

    expected_response = serializers.GoalSerializer(goals, many=True).data
    client.force_login(user)
    response = client.get("/goals/goal/list", {"ordering": "id"})

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_goal_read(client, user_factory, board_factory,
                   board_participant_factory, category_factory, goal_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    cat = category_factory.create(board=board, user=user)
    goal = goal_factory.create(category=cat, user=user)

    expected_response = serializers.GoalSerializer(goal).data
    client.force_login(user)
    response = client.get(f"/goals/goal/{goal.pk}")

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_goal_update(client, user_factory, board_factory,
                     board_participant_factory, category_factory, goal_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    cat = category_factory.create(board=board, user=user)
    goal = goal_factory.create(category=cat, user=user)

    data = {
        "category": cat.pk,
        "title": "test_2",
        "description": "test_2",
        "due_date": "2022-12-22",
        "status": Goal.Status.in_progress,
        "priority": Goal.Priority.low
    }

    client.force_login(user)
    response = client.put(f"/goals/goal/{goal.pk}", data=data, content_type="application/json")
    goal = Goal.objects.filter(pk=goal.pk).first()
    expected_response = serializers.GoalSerializer(goal).data

    assert response.status_code == 200
    assert response.data == expected_response
    assert response.data["category"] == cat.pk
    assert response.data["title"] == "test_2"
    assert response.data["description"] == "test_2"
    assert response.data["status"] == Goal.Status.in_progress
    assert response.data["priority"] == Goal.Priority.low


@pytest.mark.django_db
def test_goal_partial_update(client, user_factory, board_factory,
                             board_participant_factory, category_factory, goal_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    cat = category_factory.create(board=board, user=user)
    goal = goal_factory.create(category=cat, user=user)

    data = {
        "category": cat.pk,
        "title": "test_3",
        "description": "test_3",
        "due_date": "2022-12-22",
        "status": Goal.Status.done,
        "priority": Goal.Priority.high
    }

    client.force_login(user)
    response = client.patch(f"/goals/goal/{goal.pk}", data=data, content_type="application/json")
    goal = Goal.objects.filter(pk=goal.pk).first()
    expected_response = serializers.GoalSerializer(goal).data

    assert response.status_code == 200
    assert response.data == expected_response
    assert response.data["category"] == cat.pk
    assert response.data["title"] == "test_3"
    assert response.data["description"] == "test_3"
    assert response.data["status"] == Goal.Status.done
    assert response.data["priority"] == Goal.Priority.high


@pytest.mark.django_db
def test_goal_delete(client, user_factory, board_factory,
                             board_participant_factory, category_factory, goal_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(user=user, board=board, role=BoardParticipant.Role.owner)
    cat = category_factory.create(board=board, user=user)
    goal = goal_factory.create(category=cat, user=user)

    client.force_login(user)
    response = client.delete(f"/goals/goal/{goal.pk}")
    goal = Goal.objects.filter(pk=goal.pk).first()

    assert response.status_code == 204
    assert goal.status == Goal.Status.archived
    assert len(Goal.objects.filter(user=user)) == 1
