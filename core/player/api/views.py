from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import UploadMusicSerializer, MusicListSerializer, ArtistSerializer
from ..models import Music, Artist


class UploadMusic(generics.GenericAPIView):
    serializer_class = UploadMusicSerializer

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
