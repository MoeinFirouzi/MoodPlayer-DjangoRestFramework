from django.urls import path
from .api.views import (ListCreateMusic, ArtistListCreateAPIView,
                        AlbumListCreateAPIView, SearchMusicByName,
                        MusicRetrieveUpdateDestroyAPIView, AlbumRetrieveUpdateDestroyAPIView,
                        ArtistRetrieveUpdateDestroyAPIView)

urlpatterns = [
    path('music/<int:pk>/',
         MusicRetrieveUpdateDestroyAPIView.as_view(), name="music_RUD"),
    path('music/', ListCreateMusic.as_view(), name="music_list_create"),
    path('artist/', ArtistListCreateAPIView.as_view(), name="artist_list_create"),
    path('album/', AlbumListCreateAPIView.as_view(), name="album_list_create"),
    path('music/search/', SearchMusicByName.as_view(), name="search_music"),
    path('artist/<int:pk>/', ArtistRetrieveUpdateDestroyAPIView.as_view(),
         name="artist_RUD"),
    path('album/<int:pk>/', AlbumRetrieveUpdateDestroyAPIView.as_view(),
         name="album_RUD"),
]
