import pytest

from core.models import User


@pytest.mark.django_db
def test_user_update_password(client, user_factory):
    password = "test_password"
    user = user_factory.create()
    user.set_password(password)
    user.save()

    data = {
        "old_password": password,
        "new_password": "new_password"
    }
    client.force_login(user)
    response = client.put(f"/core/update_password", data=data, content_type="application/json")
    user = User.objects.filter(username=user.username).first()

    assert response.status_code == 200
    assert user.check_password("new_password")
