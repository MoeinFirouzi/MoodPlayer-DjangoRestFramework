from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    last_recommend_id = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f"User id '{self.user.id}' Session '{self.id}'"


class SensorState(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    session = models.ForeignKey("Session", on_delete=models.CASCADE, null=True)
    sequence = models.IntegerField(null=True, blank=True)
    date_time = models.CharField(max_length=250, null=True, blank=True)
    acceleration_x = models.FloatField(null=True, blank=True)
    acceleration_y = models.FloatField(null=True, blank=True)
    acceleration_z = models.FloatField(null=True, blank=True)
    acceleration_length = models.FloatField(null=True, blank=True)
    pressure_hecto_pascal = models.FloatField(null=True, blank=True)
    heading_magnetic_north = models.FloatField(null=True, blank=True)
    location_update_time = models.CharField(max_length=250, null=True, blank=True)
    location_latitude = models.FloatField(null=True, blank=True)
    location_longitude = models.FloatField(null=True, blank=True)
    location_altitude = models.FloatField(null=True, blank=True)
    location_accuracy = models.FloatField(null=True, blank=True)
    location_vertical_accuracy = models.FloatField(null=True, blank=True)
    location_speed = models.FloatField(null=True, blank=True)
    location_course_true_north = models.FloatField(null=True, blank=True)
    location_is_from_mock_provider = models.BooleanField(null=True, blank=True)
    location_altitude_reference_system = models.CharField(
        max_length=250, null=True, blank=True
    )
    angular_velocity_x = models.FloatField(null=True, blank=True)
    angular_velocity_y = models.FloatField(null=True, blank=True)
    angular_velocity_z = models.FloatField(null=True, blank=True)
    angular_velocity_length = models.FloatField(null=True, blank=True)
    magnetic_field_x = models.FloatField(null=True, blank=True)
    magnetic_field_y = models.FloatField(null=True, blank=True)
    magnetic_field_z = models.FloatField(null=True, blank=True)
    magnetic_field_length = models.FloatField(null=True, blank=True)
    orientation_x = models.FloatField(null=True, blank=True)
    orientation_y = models.FloatField(null=True, blank=True)
    orientation_z = models.FloatField(null=True, blank=True)
    orientation_w = models.FloatField(null=True, blank=True)
    orientation_length = models.FloatField(null=True, blank=True)
    orientation_is_identity = models.BooleanField(null=True, blank=True)

    def get_session_user_id(self):
        if self.session:
            return self.session.user.id
        else:
            return None

    def __str__(self):
        return f"Record '{self.id}'"


class MusicState(models.Model):
    user_id = models.IntegerField(null=True, blank=True)
    session = models.ForeignKey("Session", on_delete=models.CASCADE, null=True)
    sequence = models.IntegerField(null=True, blank=True)
    date_time = models.CharField(max_length=250, null=True, blank=True)
    muted = models.BooleanField(null=True, blank=True)
    position = models.CharField(max_length=250, null=True, blank=True)
    state = models.CharField(max_length=250, null=True, blank=True)
    volume = models.IntegerField(null=True, blank=True)
    playlist_count = models.IntegerField(null=True, blank=True)
    repeat_mode = models.CharField(max_length=250, null=True, blank=True)
    shuffle_mode = models.CharField(max_length=250, null=True, blank=True)
    media_type = models.CharField(max_length=250, null=True, blank=True)
    music_id = models.IntegerField(null=True, blank=True)
    album = models.CharField(max_length=250, null=True, blank=True)
    artist = models.CharField(max_length=250, null=True, blank=True)
    duration = models.CharField(max_length=250, null=True, blank=True)
    genre = models.CharField(max_length=250, null=True, blank=True)
    energy = models.CharField(max_length=250, null=True, blank=True)
    valence = models.CharField(max_length=250, null=True, blank=True)
    title = models.CharField(max_length=250, null=True, blank=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)

    def get_session_user_id(self):
        if self.session:
            return self.session.user.id
        else:
            return None

    def __str__(self):
        return f"Record '{self.id}'"
