from django.contrib import admin
from .models import Session, MusicState, SensorState

admin.site.register(Session)
admin.site.register(MusicState)
admin.site.register(SensorState)
