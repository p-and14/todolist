import pytest


@pytest.mark.django_db
def test_user_logout(client, user_factory):
    password = "test_password"
    user = user_factory.create()
    user.set_password(password)
    user.save()

    client.force_login(user)
    response = client.delete(f"/core/profile")

    assert response.status_code == 204
    assert not client.cookies.get("csrftoken")
