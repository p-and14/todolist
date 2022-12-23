import pytest

from core import serializers
from core.models import User


@pytest.mark.django_db
def test_user_signup(client):
    data = {
        "username": "test_user",
        "first_name": "test_user",
        "last_name": "test_user",
        "email": "test@mail.ru",
        "password": "test_password",
        "password_repeat": "test_password"
    }
    expected_response = serializers.UserRegistrationSerializer(data).data

    response = client.post(f"/core/signup", data=data, content_type="application/json")
    del response.data["id"]

    assert response.status_code == 201
    assert response.data == expected_response
    assert User.objects.filter(username=data["username"]).exists()
