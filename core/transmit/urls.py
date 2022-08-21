from django.urls import path
from .api.views import MusicStateCreateAPIView, SensorStateCreateAPIView
urlpatterns = [
    path('music/', MusicStateCreateAPIView.as_view(), name='music_state_create'),
    path('sensor/', SensorStateCreateAPIView.as_view(), name='sensor_state_create'),
]
