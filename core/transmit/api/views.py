from rest_framework import generics
from .serializers import MusicStateSerializer


class MusicStateCreateAPIView(generics.CreateAPIView):
    serializer_class = MusicStateSerializer
    
