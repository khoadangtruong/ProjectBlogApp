from django.contrib.auth import login, logout
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from .user_serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
)

class RegisterView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

class LoginView(CreateAPIView):

    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user = user)
        if created:
            return Response(
            {
                'user': user.username,
                'token': token.key, 
            },
            status = status.HTTP_201_CREATED)
        else:
            token.delete()
            token = Token.objects.create(user = user)
            return Response(
            {
                'user': user.username,
                'token': token.key,
            },
            status = status.HTTP_201_CREATED)


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response('User logged out successfully')