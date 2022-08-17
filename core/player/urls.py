from django.urls import path
from .api.views import UploadMusic

urlpatterns = [
    path('upload-music/', UploadMusic.as_view(), name="upload_music"),
]
