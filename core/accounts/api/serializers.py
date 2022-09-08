from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class UsernameLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        email = validated_data["email"]
        username = validated_data["username"]
        password = validated_data["password"]
        user = User.objects.create_user(
            email=email, username=username, password=password
        )
        user.save()

        return user


class UserLogOutSerializer(serializers.Serializer):
    pass
