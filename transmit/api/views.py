from rest_framework import generics
from ..models import Session
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import MusicStateSerializer, SensorStateSerializer, SessionSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models import SensorState, MusicState
from .utilize import CSVConvertor, ZipConvertor, FileCleaner
from django.http import HttpResponse, FileResponse


class MusicStateCreateAPIView(generics.CreateAPIView):
    serializer_class = MusicStateSerializer
    permission_classes = [IsAuthenticated]


class SensorStateCreateAPIView(generics.CreateAPIView):
    serializer_class = SensorStateSerializer
    permission_classes = [IsAuthenticated]


class SessionCreateAPIView(generics.CreateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        instance = Session.objects.create(user=request.user)
        instance.is_active = True
        instance.save()
        data = {"id": instance.id, "active": instance.is_active}
        return Response(data, status=status.HTTP_201_CREATED)


class SessionDeactivateAPIView(generics.UpdateAPIView):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        session_id = self.kwargs.get("pk")
        instance = get_object_or_404(Session, id=session_id)
        instance.is_active = False
        instance.save()
        data = {"id": instance.id, "active": instance.is_active}
        return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)


class GetSensorState(generics.ListAPIView):
    serializer_class = SensorStateSerializer
    permission_classes = [IsAdminUser]
    queryset = SensorState.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        payload = {"data": serializer.data}
        return Response(payload)


class GetMusicState(generics.ListAPIView):
    serializer_class = MusicStateSerializer
    permission_classes = [IsAdminUser]
    queryset = MusicState.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        payload = {"data": serializer.data}
        return Response(payload)


class GetSessionData(generics.GenericAPIView):
    # permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, *args, **kwargs):
        session_id = kwargs.get("pk", None)

        convertor = CSVConvertor(f'sensor_{session_id}')
        query_set = SensorState.objects.filter(session=session_id)
        convertor.convert(query_set)

        convertor = CSVConvertor(f'music_{session_id}')
        query_set = MusicState.objects.filter(session=session_id)
        convertor.convert(query_set)

        zip_convertor = ZipConvertor(session_id=session_id)
        zip_convertor.convert()

        try:
            return FileResponse(
                open(zip_convertor.path, 'rb'),
                as_attachment=True,
                filename=f'{session_id}.zip'
            )
        except:
            pass
        finally:
            cleaner = FileCleaner(session_id)
            cleaner.clean()
