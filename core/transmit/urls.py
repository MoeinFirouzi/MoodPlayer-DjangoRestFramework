from django.urls import path
from .api.views import (MusicStateCreateAPIView, SensorStateCreateAPIView,
                        SessionCreateAPIView, SessionDeactivateAPIView)
urlpatterns = [
    path('music/', MusicStateCreateAPIView.as_view(), name='music_state_create'),
    path('sensor/', SensorStateCreateAPIView.as_view(), name='sensor_state_create'),
    path('session/', SessionCreateAPIView.as_view(), name='session_start'),
    path('session/<int:pk>/', SessionDeactivateAPIView.as_view(), name='session_halt'),
]
