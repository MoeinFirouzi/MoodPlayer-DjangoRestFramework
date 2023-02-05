from rest_framework import serializers


class RecommendationSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    first_sequence = serializers.IntegerField()
    last_sequence = serializers.IntegerField()
    recommendation_id = serializers.IntegerField()