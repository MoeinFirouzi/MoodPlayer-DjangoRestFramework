from rest_framework import generics
from .serializers import MusicStateSerializer, SensorStateSerializer


class MusicStateCreateAPIView(generics.CreateAPIView):
    serializer_class = MusicStateSerializer
    

class SensorStateCreateAPIView(generics.CreateAPIView):
    serializer_class = SensorStateSerializer