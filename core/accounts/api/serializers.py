from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
