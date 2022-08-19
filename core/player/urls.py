from django.urls import path
from .api.views import (UploadMusic, GetMusicDataList, GetArtistList,
                        GetAlbumList, SearchMusicByName,
                        MusicRetrieveUpdateDestroyAPIView)
urlpatterns = [
    path('upload-music/', UploadMusic.as_view(), name="upload_music"),
    path('music/<int:pk>/',
         MusicRetrieveUpdateDestroyAPIView.as_view(), name="music_api"),
    path('music/list/', GetMusicDataList.as_view(), name="music_list"),
    path('artist/list/', GetArtistList.as_view(), name="artist_list"),
    path('album/list/', GetAlbumList.as_view(), name="album_list"),
    path('music/search/', SearchMusicByName.as_view(), name="search_music"),
]
