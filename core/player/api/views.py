from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .serializers import UploadMusicSerializer


class UploadMusic(generics.GenericAPIView):
    serializer_class = UploadMusicSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'message': "Music has uploaded successfully", 'id': serializer.data.get('id')}
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# class GetMusicDataList(generics.ListAPIView):
#     serializer_class = 