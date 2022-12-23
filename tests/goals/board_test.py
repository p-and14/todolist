import pytest

from goals import serializers
from goals.models import BoardParticipant, Board


@pytest.mark.django_db
def test_board_create(client, user_factory):
    user = user_factory.create()
    data = {
        "title": "test",
        "is_deleted": False
    }

    client.force_login(user)
    response = client.post("/goals/board/create", data=data)

    assert response.status_code == 201
    assert response.data["title"] == "test"
    assert not response.data["is_deleted"]

    empty_data = {}
    response = client.post("/goals/board/create", data=empty_data)
    assert response.status_code == 400
    assert response.data["title"][0] == "This field is required."


@pytest.mark.django_db
def test_board_list(client, user_factory, board_factory, board_participant_factory):
    users = user_factory.create_batch(2)
    boards = board_factory.create_batch(2)
    for board in boards:
        board_participant_factory.create(board=board, user=users[0], role=BoardParticipant.Role.owner)

    expected_response = serializers.BoardListSerializer(boards, many=True).data

    client.force_login(users[0])
    response = client.get("/goals/board/list", {"ordering": "id"})

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_board_read(client, user_factory, board_factory, board_participant_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(board=board, user=user)

    expected_response = serializers.BoardSerializer(board).data

    client.force_login(user)
    response = client.get(f"/goals/board/{board.pk}")

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_board_update(client, user_factory, board_factory, board_participant_factory):
    users = user_factory.create_batch(2)
    board = board_factory.create()
    board_participant_factory.create(board=board, user=users[0])

    # add participants
    data = {
        "participants": [{
            "user": users[1].username,
            "role": BoardParticipant.Role.reader
        }],
        "title": "new title"
    }
    client.force_login(users[0])
    response = client.put(f"/goals/board/{board.pk}", data=data, content_type="application/json")

    assert response.status_code == 200
    assert response.data["title"] == "new title"
    assert len(response.data["participants"]) == 2
    assert response.data["participants"][1]["role"] == 3
    assert response.data["participants"][1]["user"] == users[1].username

    # change participants
    data = {
        "participants": [{
            "user": users[1].username,
            "role": BoardParticipant.Role.writer
        }],
        "title": "new title"
    }

    response = client.put(f"/goals/board/{board.pk}", data=data, content_type="application/json")

    assert response.data["participants"][1]["role"] == 2

    # delete participants
    data = {
        "participants": [],
        "title": "new title"
    }

    response = client.put(f"/goals/board/{board.pk}", data=data, content_type="application/json")

    assert len(response.data["participants"]) == 1


@pytest.mark.django_db
def test_board_partial_update(client, user_factory, board_factory, board_participant_factory):
    users = user_factory.create_batch(2)
    board = board_factory.create()
    board_participant_factory.create(board=board, user=users[0])

    # add participants
    add_data = {
        "participants": [{
            "user": users[1].username,
            "role": BoardParticipant.Role.reader
        }],
        "title": "new title"
    }
    client.force_login(users[0])
    response = client.patch(f"/goals/board/{board.pk}", data=add_data, content_type="application/json")

    assert response.status_code == 200
    assert response.data["title"] == "new title"
    assert len(response.data["participants"]) == 2
    assert response.data["participants"][1]["role"] == 3
    assert response.data["participants"][1]["user"] == users[1].username

    # change participants
    change_data = {
        "participants": [{
            "user": users[1].username,
            "role": BoardParticipant.Role.writer
        }],
        "title": "new title"
    }

    response = client.patch(f"/goals/board/{board.pk}", data=change_data, content_type="application/json")

    assert response.data["participants"][1]["role"] == 2

    # delete participants
    delete_data = {
        "participants": [],
        "title": "new title"
    }

    response = client.patch(f"/goals/board/{board.pk}", data=delete_data, content_type="application/json")

    assert len(response.data["participants"]) == 1


@pytest.mark.django_db
def test_board_delete(client, user_factory, board_factory, board_participant_factory):
    user = user_factory.create()
    board = board_factory.create()
    board_participant_factory.create(board=board, user=user)

    client.force_login(user)
    response = client.delete(f"/goals/board/{board.pk}")
    board = Board.objects.filter(pk=board.pk).first()

    assert response.status_code == 204
    assert board.is_deleted
    assert len(Board.objects.filter(participants__user=user)) == 1
