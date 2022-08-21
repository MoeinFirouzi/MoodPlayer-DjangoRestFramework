from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import (AlbumSerializer, MusicSerializer,
                          ArtistSerializer)
from ..models import Music, Artist, Album
from rest_framework.permissions import IsAuthenticated


class ListCreateMusic(generics.ListCreateAPIView):
    """
    Return list of Musics in Database.
    If 'id' parameter exists, then it will return list of objects
    that their id are in 'id' parameter.
    """
    serializer_class = MusicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ids = self.request.GET.get('id')
        if ids:
            id_list = list(map(int, ids.split(',')))
            queryset = Music.objects.filter(id__in=id_list)

        else:
            queryset = Music.objects.all()

        return queryset

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'message': "Music has uploaded successfully",
                    'id': serializer.data.get('id')}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MusicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MusicSerializer
    queryset = Music.objects.all()
    permission_classes = [IsAuthenticated]


class ArtistListCreateAPIView(generics.ListCreateAPIView):
    """
    'POST':
    Return list of Artists in Database.
    If 'id' parameter exists, then it will return a list of objects
    that their id are in 'id' parameter.

    'POST':
    Create an Artist instance.
    """
    serializer_class = ArtistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ids = self.request.GET.get('id')
        if ids:
            id_list = list(map(int, ids.split(',')))
            queryset = Artist.objects.filter(id__in=id_list)

        else:
            queryset = Artist.objects.all()

        return queryset


class AlbumListCreateAPIView(generics.ListCreateAPIView):
    """
    'GET':
    Return list of Albums in Database.
    If 'id' parameter exists, then it will return a list of objects
    that their id are in 'id' parameter.

    'POST':
    Create an Album instance.
    """
    serializer_class = AlbumSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ids = self.request.GET.get('id')
        if ids:
            id_list = list(map(int, ids.split(',')))
            queryset = Album.objects.filter(id__in=id_list)

        else:
            queryset = Album.objects.all()

        return queryset


class SearchMusicByName(generics.ListAPIView):
    serializer_class = MusicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search_phrase = self.request.GET.get('search')
        if search_phrase:
            queryset = Music.objects.filter(title__contains=search_phrase)
            print(queryset)

        else:
            queryset = Album.objects.all()

        return queryset

    def get(self, request, *args, **kwargs):
        search_phrase = self.request.GET.get('search')
        if search_phrase:
            return self.list(request, *args, **kwargs)
        else:
            return redirect(reverse('music_list_create'))


class AlbumRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    permission_classes = [IsAuthenticated]


class ArtistRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    permission_classes = [IsAuthenticated]
