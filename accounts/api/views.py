from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    EmailLoginSerializer,
    UsernameLoginSerializer,
    UserSignUpSerializer,
    UserLogOutSerializer,
    GetUsersSerializer,
)

User = get_user_model()


class EmailLogin(generics.GenericAPIView):
    """
    Login users with Email.
    Returns token if successful with 200 status code,
    else returns errors with 400 status code.
    """

    serializer_class = EmailLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = get_object_or_404(User, email=email)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                data = {"token": token.key, "user_id": user.pk, "created": created}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"message": "password is incorrect."}
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsernameLogin(generics.GenericAPIView):
    """
    Login users with Username.
    Returns token if successful with 200 status code,
    else returns errors with 400 status code.
    """

    serializer_class = UsernameLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = get_object_or_404(User, username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                data = {"token": token.key, "user_id": user.pk, "created": created}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {"message": "password is incorrect."}
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUp(generics.GenericAPIView):
    """
    Create a user by giving 'username', 'email' and 'password',
    then returns its auth token.
    """

    serializer_class = UserSignUpSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user = get_object_or_404(User, email=serializer.validated_data["email"])
            token, created = Token.objects.get_or_create(user=user)
            data = {"token": token.key, "user_id": user.pk, "created": created}
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogOut(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserLogOutSerializer

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetUsers(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = GetUsersSerializer