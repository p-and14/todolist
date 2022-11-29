from django.contrib.auth import login, authenticate, logout
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import UserRegistrationSerializer, UserProfileSerializer, UserPasswordUpdateSerializer


class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class UserLogin(generics.GenericAPIView):
    def post(self, request):
        username = request.data["username"]
        password = request.data["password"]

        user = authenticate(request, username=username, password=password)
        if not user:
            raise AuthenticationFailed

        login(request, user)
        response = {"username": username, "password": password}

        return JsonResponse(response, status=status.HTTP_201_CREATED)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePassword(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
