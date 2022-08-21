from django.urls import path
from .api.views import MusicStateCreateAPIView
urlpatterns = [
    path('music/', MusicStateCreateAPIView.as_view(), name='music_state_create'),
]
