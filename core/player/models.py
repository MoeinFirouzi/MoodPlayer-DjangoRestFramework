from django.db import models
from django.urls import reverse


class Music(models.Model):
    CHOICES = (
        ("Too Negative", "Too Negative"),
        ("Negative", "Negative"),
        ("Neutral", "Neutral"),
        ("Positive", "Positive"),
        ("Too Positive", "Too Positive"),
    )

    title = models.CharField(max_length=250, blank=True, null=True)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE,
                               related_name="musics", blank=True, null=True)
    album = models.ForeignKey('Album', on_delete=models.CASCADE,
                              related_name="musics", blank=True, null=True)
    genre = models.CharField(max_length=250, blank=True, null=True)
    energy = models.CharField(choices=CHOICES, blank=True,
                              max_length=50, null=True)
    valence = models.CharField(choices=CHOICES, blank=True,
                               max_length=50, null=True)
    song_image = models.ImageField(upload_to='music/images/',
                                   blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    address = models.FileField(upload_to='music/files/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.title:
            self.title = self.title.lower()
        if self.genre:
            self.genre = self.genre.lower()
        return super(Music, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title

    def get_artist_id(self):
        return self.artist.id

    def get_album_id(self):
        return self.album.id

    def get_album_absolute_url(self):
        return self.album.get_absolute_url()
    
    def get_artist_absolute_url(self):
        return self.album.get_absolute_url()
    
    def get_absolute_url(self):
        return reverse("music_RUD", kwargs={"pk": self.pk})

        


class Artist(models.Model):
    name = models.CharField(max_length=250, unique=True)
    artist_image = models.ImageField(upload_to='artist/images/',
                                     blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        return super(Artist, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("artist_RUD", kwargs={"pk": self.pk})


class Album(models.Model):
    name = models.CharField(max_length=250, unique=True)
    album_image = models.ImageField(upload_to='album/images/',
                                    blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.lower()
        return super(Album, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("album_RUD", kwargs={"pk": self.pk})

    def __str__(self) -> str:
        return self.name
