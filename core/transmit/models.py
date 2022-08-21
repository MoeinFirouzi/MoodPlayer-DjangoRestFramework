from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Session(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sessions")
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)


class SensorState(models.Model):
    session = models.ForeignKey('Session', on_delete=models.CASCADE, null=True)
    date_time = models.CharField(
        max_length=250, null=True, blank=True)
    acceleration_x = models.FloatField(null=True, blank=True)
    accelerationY = models.FloatField(null=True, blank=True)
    accelerationZ = models.FloatField(null=True, blank=True)
    accelerationLength = models.FloatField(null=True, blank=True)
    pressureHectoPascal = models.FloatField(null=True, blank=True)
    headingMagneticNorth = models.FloatField(null=True, blank=True)
    locationUpdateTime = models.DateTimeField(null=True, blank=True)
    locationLatitude = models.FloatField(null=True, blank=True)
    locationLongitude = models.FloatField(null=True, blank=True)
    locationAltitude = models.FloatField(null=True, blank=True)
    locationAccuracy = models.FloatField(null=True, blank=True)
    locationVerticalAccuracy = models.FloatField(null=True, blank=True)
    locationSpeed = models.FloatField(null=True, blank=True)
    locationCourseTrueNorth = models.FloatField(null=True, blank=True)
    locationIsFromMockProvider = models.BooleanField(null=True, blank=True)
    locationAltitudeRefrenceSystem = models.CharField(
        max_length=250, null=True, blank=True)
    angularVelocityX = models.FloatField(null=True, blank=True)
    angularVelocityY = models.FloatField(null=True, blank=True)
    angularVelocityZ = models.FloatField(null=True, blank=True)
    angularVelocityLength = models.FloatField(null=True, blank=True)
    magneticFieldX = models.FloatField(null=True, blank=True)
    magneticFieldY = models.FloatField(null=True, blank=True)
    magneticFieldZ = models.FloatField(null=True, blank=True)
    magneticFieldLength = models.FloatField(null=True, blank=True)
    orientationX = models.FloatField(null=True, blank=True)
    orientationY = models.FloatField(null=True, blank=True)
    orientationZ = models.FloatField(null=True, blank=True)
    orientationW = models.FloatField(null=True, blank=True)
    orientationLength = models.FloatField(null=True, blank=True)
    orientationIsIdentity = models.BooleanField(null=True, blank=True)


class MusicState(models.Model):
    session_id = models.ForeignKey(
        'Session', on_delete=models.CASCADE, null=True)
    date_time = models.CharField(
        max_length=250, null=True, blank=True)
    muted = models.BooleanField(null=True, blank=True)
    position = models.CharField(
        max_length=250, null=True, blank=True)
    state = models.CharField(
        max_length=250, null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    playlist_count = models.IntegerField(null=True, blank=True)
    repeatMode = models.CharField(
        max_length=250, null=True, blank=True)
    shuffle_mode = models.CharField(
        max_length=250, null=True, blank=True)
    media_type = models.CharField(
        max_length=250, null=True, blank=True)
    music_id = models.IntegerField(null=True, blank=True)
    album = models.CharField(
        max_length=250, null=True, blank=True)
    artist = models.CharField(
        max_length=250, null=True, blank=True)
    duration = models.CharField(
        max_length=250, null=True, blank=True)
    genre = models.CharField(
        max_length=250, null=True, blank=True)
    energy = models.CharField(
        max_length=250, null=True, blank=True)
    valence = models.CharField(
        max_length=250, null=True, blank=True)
    title = models.CharField(
        max_length=250, null=True, blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
