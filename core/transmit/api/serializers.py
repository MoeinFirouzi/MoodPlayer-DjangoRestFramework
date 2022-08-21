from rest_framework import serializers
from ..models import MusicState, SensorState, Session


class MusicStateSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    class Meta:
        
        model = MusicState
        fields = '__all__'

    def get_user_id(self, obj):
        return obj.get_session_user_id()
    
    
class SensorStateSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    class Meta:
        
        model = SensorState
        fields = '__all__'

    def get_user_id(self, obj):
        return obj.get_session_user_id()
    
    
class SessionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Session
        fields = ['id']