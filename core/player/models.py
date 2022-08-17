from django.db import models


class Music(models.Model):
    CHOICES = (
        ("Too Negative", "Too Negative"),
        ("Negative", "Negative"),
        ("Neutral", "Neutral"),
        ("Positive", "Positive"),
        ("Too Positive", "Too Positive"),
    )

    title = models.CharField(max_length=250, blank=True)
    artist = models.ForeignKey(
        'Artist', on_delete=models.CASCADE, related_name="musics", blank=True)
    album = models.ForeignKey(
        'Album', on_delete=models.CASCADE, related_name="musics", blank=True)
    genre = models.CharField(max_length=250, blank=True)
    energy = models.CharField(choices=CHOICES, blank=True, max_length=50)
    valence = models.CharField(choices=CHOICES, blank=True, max_length=50)
    song_image = models.ImageField(upload_to='music/images/', blank=True)
    year = models.PositiveSmallIntegerField(blank=True)
    address = models.FileField(upload_to='music/files/', blank=True)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        self.genre = self.genre.lower()
        return super(Music, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title


class Artist(models.Model):
    name = models.CharField(max_length=250, unique=True)
    artist_image = models.ImageField(upload_to='artist/images/', blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Artist, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Album(models.Model):
    name = models.CharField(max_length=250, unique=True)
    album_image = models.ImageField(upload_to='album/images/', blank=True)

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Album, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
