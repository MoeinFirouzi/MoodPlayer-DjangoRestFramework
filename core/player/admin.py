from django.contrib import admin
from .models import Album, Artist, Music

admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Music)