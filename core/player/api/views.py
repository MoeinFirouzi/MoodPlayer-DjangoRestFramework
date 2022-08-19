from django.shortcuts import redirect
from django.urls import reverse
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import (AlbumSerializer, MusicSerializer, MusicListSerializer,
                          ArtistSerializer, Album)
from ..models import Music, Artist, Album


class UploadMusic(generics.GenericAPIView):
    serializer_class = MusicSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'message': "Music has uploaded successfully",
                    'id': serializer.data.get('id')}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class GetMusicDataList(generics.ListAPIView):
    """
    Return list of Musics in Database.
    If 'id' parameter exists, then it will return list of objects
    that their id are in 'id' parameter.
    """
    serializer_class = MusicListSerializer

    def get_queryset(self):
        ids = self.request.GET.get('id')
        if ids:
            id_list = list(map(int, ids.split(',')))
            queryset = Music.objects.filter(id__in=id_list)

        else:
            queryset = Music.objects.all()

        return queryset


class MusicRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MusicSerializer
    queryset = Music.objects.all()


class GetArtistList(generics.ListAPIView):
    """
    Return list of Artists in Database.
    If 'id' parameter exists, then it will return a list of objects
    that their id are in 'id' parameter.
    """
    serializer_class = ArtistSerializer

    def get_queryset(self):
        ids = self.request.GET.get('id')
        if ids:
            id_list = list(map(int, ids.split(',')))
            queryset = Artist.objects.filter(id__in=id_list)

        else:
            queryset = Artist.objects.all()

        return queryset


class GetAlbumList(generics.ListAPIView):
    """
    Return list of Albums in Database.
    If 'id' parameter exists, then it will return a list of objects
    that their id are in 'id' parameter.
    """
    serializer_class = AlbumSerializer

    def get_queryset(self):
        ids = self.request.GET.get('id')
        if ids:
            id_list = list(map(int, ids.split(',')))
            queryset = Album.objects.filter(id__in=id_list)

        else:
            queryset = Album.objects.all()

        return queryset


class SearchMusicByName(generics.ListAPIView):
    serializer_class = MusicListSerializer

    def get_queryset(self):
        search_phrase = self.request.GET.get('search')
        if search_phrase:
            queryset = Music.objects.filter(title__contains=search_phrase)

        else:
            queryset = Album.objects.all()

        return queryset

    def get(self, request, *args, **kwargs):
        search_phrase = self.request.GET.get('search')
        if search_phrase:
            return self.list(request, *args, **kwargs)
        else:
            return redirect(reverse('music_list'))