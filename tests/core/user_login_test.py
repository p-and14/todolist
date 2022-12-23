import pytest


@pytest.mark.django_db
def test_user_login(client, user_factory):
    password = "test_password"
    user = user_factory.create()
    user.set_password(password)
    user.save()

    data = {
        "username": user.username,
        "password": password
    }

    response = client.post(f"/core/login", data=data, content_type="application/json")

    assert response.status_code == 201
    assert client.cookies.get("csrftoken")
