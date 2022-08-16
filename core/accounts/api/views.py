from rest_framework import generics
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import EmailLoginSerializer, UsernameLoginSerializer

User = get_user_model()


class EmailLogin(generics.GenericAPIView):
    serializer_class = EmailLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = get_object_or_404(User, email=email)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                data = {'token': token.key,
                        'user_id': user.pk, 'created': created}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {'message': "password is incorrect."}
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsernameLogin(generics.GenericAPIView):
    serializer_class = UsernameLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = get_object_or_404(User, username=username)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                data = {'token': token.key,
                        'user_id': user.pk, 'created': created}
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {'message': "password is incorrect."}
                return Response(data, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
