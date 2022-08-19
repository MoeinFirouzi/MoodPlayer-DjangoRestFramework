from django.urls import path
from .api.views import UploadMusic, GetMusicDataList

urlpatterns = [
    path('upload-music/', UploadMusic.as_view(), name="upload_music"),
    path('music/list/', GetMusicDataList.as_view(), name="music_list"),
]
