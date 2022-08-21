from rest_framework import generics
from ..models import Session
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (MusicStateSerializer, SensorStateSerializer,
                          SessionSerializer)


class MusicStateCreateAPIView(generics.CreateAPIView):
    serializer_class = MusicStateSerializer


class SensorStateCreateAPIView(generics.CreateAPIView):
    serializer_class = SensorStateSerializer


class SessionCreateAPIView(generics.CreateAPIView):
    serializer_class = SessionSerializer

    def post(self, request, *args, **kwargs):
        instance = Session.objects.create(user=request.user)
        instance.is_active = True
        instance.save()
        data = {'id': instance.id, 'active': instance.is_active}
        return Response(data, status=status.HTTP_201_CREATED)


class SessionDeactivateAPIView(generics.UpdateAPIView):
    serializer_class = SessionSerializer

    def put(self, request, *args, **kwargs):
        session_id = self.kwargs.get('pk')
        instance = get_object_or_404(Session, id=session_id)
        instance.is_active = False
        instance.save()
        data = {'id': instance.id, 'active': instance.is_active}
        return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
