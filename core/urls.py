from django.urls import path

from core.views import UserCreateView, UserLogin, UserProfileView, UpdatePassword

urlpatterns = [
    path("signup", UserCreateView.as_view(), name="user_signup"),
    path("login", UserLogin.as_view(), name="user_login"),
    path("profile", UserProfileView.as_view(), name="user_profile"),
    path("update_password", UpdatePassword.as_view(), name="user_password_update")
]
