from rest_framework import serializers
from ..models import MusicState, SensorState, Session


class MusicStateSerializer(serializers.ModelSerializer):

    class Meta:

        model = MusicState
        fields = "__all__"


class SensorStateSerializer(serializers.ModelSerializer):
    class Meta:

        model = SensorState
        fields = "__all__"


class SessionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Session
        fields = ["id"]
