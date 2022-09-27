from django.urls import path
from .api.views import (
    MusicStateCreateAPIView,
    SensorStateCreateAPIView,
    SessionCreateAPIView,
    SessionDeactivateAPIView,
    GetSensorState,
    GetMusicState,GetSessionData
)

urlpatterns = [
    path("music/", MusicStateCreateAPIView.as_view(), name="music_state_create"),
    path("sensor/", SensorStateCreateAPIView.as_view(), name="sensor_state_create"),
    path("session/", SessionCreateAPIView.as_view(), name="session_start"),
    path("session/<int:pk>/", SessionDeactivateAPIView.as_view(), name="session_halt"),
    path("sensor/data/", GetSensorState.as_view(), name="get_sensor_data"),
    path("music/data/", GetMusicState.as_view(), name="get_music_data"),
    path("session/<int:pk>/get_data/",GetSessionData.as_view(), name="get_session_data"),
]
